import json
import os
import shutil
import tempfile
import threading
import time
from collections import defaultdict, deque

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile, WebSocket
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel

from sentinel.asr import transcribe
from sentinel.engine import analyze_image, investigate
from sentinel.live import LiveSession
from sentinel.segment import evidence_boxes

app = FastAPI(title="Sentinel")


# =====================================================================
# Rate limit: per-visitor limits so one person or bot can't drain credits
# =====================================================================

LIMITS = {"check": (20, 3600), "live": (5, 3600)}   # 20 checks and 5 live calls per hour per visitor
_hits: dict = defaultdict(deque)
_hits_lock = threading.Lock()


def _client_ip(conn) -> str:
    fwd = conn.headers.get("x-forwarded-for")       # Render puts the real visitor IP here
    return fwd.split(",")[0].strip() if fwd else (conn.client.host if conn.client else "unknown")


def _allow(kind: str, ip: str) -> bool:
    if ip in ("127.0.0.1", "::1", "localhost"):     # never limit local development
        return True
    limit, window = LIMITS[kind]
    with _hits_lock:
        q, now = _hits[(kind, ip)], time.time()
        while q and now - q[0] > window:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        return True


def rate_limit(request: Request):
    if not _allow("check", _client_ip(request)):
        raise HTTPException(429, "You've reached the hourly limit for checks. Please try again later.")


# =====================================================================
# Helpers
# =====================================================================

class TextIn(BaseModel):
    text: str
    language: str = "English"


def _save_upload(f: UploadFile, suffix: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    shutil.copyfileobj(f.file, tmp)
    tmp.close()
    return tmp.name


def _cleanup(path: str):
    try:
        os.remove(path)
    except OSError:
        pass          # Windows can briefly lock files; temp files are cleared later anyway


@app.exception_handler(Exception)
async def upstream_error(request: Request, exc: Exception):
    return JSONResponse(status_code=502,
                        content={"detail": "The check couldn't finish. Try again in a moment.",
                                 "error": str(exc)})


# =====================================================================
# API
# =====================================================================

@app.post("/api/analyze/text", dependencies=[Depends(rate_limit)])
def analyze_text_endpoint(body: TextIn):
    if not body.text.strip():
        raise HTTPException(400, "Paste a message to check.")
    return investigate(body.text, user_language=body.language)


@app.post("/api/analyze/message", dependencies=[Depends(rate_limit)])
def analyze_message_endpoint(text: str = Form(""), language: str = Form("English"),
                             file: UploadFile | None = File(None)):
    if not text.strip() and file is None:
        raise HTTPException(400, "Paste a message or add a screenshot.")
    path = None
    if file is not None:
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in (".png", ".jpg", ".jpeg"):
            raise HTTPException(400, "Use a PNG or JPG image.")
        path = _save_upload(file, ext)
    try:
        return investigate(text, user_language=language, image_path=path)
    finally:
        if path:
            _cleanup(path)


@app.post("/api/analyze/image", dependencies=[Depends(rate_limit)])
def analyze_image_endpoint(file: UploadFile = File(...), language: str = Form("English")):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in (".png", ".jpg", ".jpeg"):
        raise HTTPException(400, "Upload a PNG or JPG screenshot.")
    path = _save_upload(file, ext)
    try:
        v = analyze_image(path, user_language=language)
        boxes = evidence_boxes(path, v.get("suspicious_regions", []))
        with Image.open(path) as im:
            w, h = im.size
        v["evidence"] = {"width": w, "height": h, "boxes": boxes}
        return v
    finally:
        _cleanup(path)


@app.post("/api/analyze/audio", dependencies=[Depends(rate_limit)])
def analyze_audio_endpoint(file: UploadFile = File(...), language: str = Form("English")):
    if not (file.filename or "").lower().endswith(".wav"):
        raise HTTPException(400, "Upload a WAV recording.")
    path = _save_upload(file, ".wav")
    try:
        t = transcribe(path)
        v = investigate(t["transcript"], user_language=language, audio_path=path)
        v["transcript"] = t["transcript"]
        v["turns"] = t.get("turns", [])
        return v
    finally:
        _cleanup(path)


@app.websocket("/ws/live")
async def live_endpoint(ws: WebSocket, language: str = "English"):
    await ws.accept()

    async def send(msg: dict):
        try:
            await ws.send_json(msg)
        except Exception:
            pass                                  # browser already closed

    if not _allow("live", _client_ip(ws)):
        await send({"type": "error",
                    "message": "You've reached the hourly limit for live calls. Please try again later."})
        await ws.close()
        return

    async def audio_source():
        while True:
            msg = await ws.receive()
            if msg.get("type") == "websocket.disconnect":
                return
            if msg.get("bytes"):
                yield msg["bytes"]
            elif msg.get("text") and json.loads(msg["text"]).get("type") == "end":
                return

    try:
        await LiveSession(language, send).run(audio_source())
    except Exception:
        await send({"type": "error",
                    "message": "Live protection stopped. Check your connection and start again."})
    finally:
        try:
            await ws.close()
        except Exception:
            pass


# The web app is served from /web. Keep this LAST so it doesn't hide the API.
os.makedirs("web", exist_ok=True)
app.mount("/", StaticFiles(directory="web", html=True), name="web")
import os, re, requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from sentinel.engine import upload_file

load_dotenv()
KEY = os.getenv("MODEL_API_KEY")

BOX_RE = re.compile(
    r"<\|box;x1=([\d.]+);y1=([\d.]+);x2=([\d.]+);y2=([\d.]+);w=([\d.]+);h=([\d.]+)\|>"
)


def segment(path: str, prompt: str) -> list[dict]:
    """Ask SAM 3.1 to find `prompt` in the image; return boxes in the image's own pixels."""
    fid = upload_file(path)
    r = requests.post(
        "https://api.meta.ai/v1/responses",
        headers={"Authorization": f"Bearer {KEY}"},
        json={
            "model": "sam-3.1",
            "input": [{"type": "message", "role": "user", "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "file_id": fid},
            ]}],
            "stream": False,
            "metadata": {"mask_encoding": "one_bit"},
        },
        timeout=120,
    )
    r.raise_for_status()
    text = "".join(c.get("text", "")
                   for item in r.json().get("output", []) if item.get("type") == "message"
                   for c in item.get("content", []))

    img_w, img_h = Image.open(path).size
    boxes = []
    for x1, y1, x2, y2, w, h in BOX_RE.findall(text):
        sx, sy = img_w / float(w), img_h / float(h)   # scale to the real image size
        boxes.append({"label": prompt, "box": [round(float(x1) * sx), round(float(y1) * sy),
                                               round(float(x2) * sx), round(float(y2) * sy)]})
    return boxes


def _overlap(a, b) -> float:
    """Fraction of box a that lies inside box b."""
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area = max(1, (a[2] - a[0]) * (a[3] - a[1]))
    return ix * iy / area


def evidence_boxes(path: str, regions: list[dict]) -> list[dict]:
    """SAM refines objects near Muse Wonder's estimate; text uses Wonder's box directly."""
    img_w, img_h = Image.open(path).size
    boxes = []
    for reg in regions:
        label = reg.get("label", "suspicious")
        guess = None
        if reg.get("box") and len(reg["box"]) == 4:
            x1, y1, x2, y2 = reg["box"]
            guess = [round(x1 * img_w / 1000), round(y1 * img_h / 1000),
                     round(x2 * img_w / 1000), round(y2 * img_h / 1000)]

        if reg.get("kind") == "object" and reg.get("sam_prompt"):
            found = segment(path, reg["sam_prompt"])
            if guess:                                   # keep only matches near Wonder's estimate
                found = [f for f in found if _overlap(f["box"], guess) > 0.3
                         or _overlap(guess, f["box"]) > 0.3]
            if found:
                best = max(found, key=lambda f: _overlap(f["box"], guess) if guess else 0)
                boxes.append({"label": label, "box": best["box"], "source": "sam-3.1"})
                continue
        if guess:
            boxes.append({"label": label, "box": guess, "source": "muse-wonder"})
    return boxes


def highlight(path: str, boxes: list[dict], out_path: str) -> str:
    """Draw red boxes with numbered tags; the number matches the evidence list order."""
    img = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(img)
    width = max(3, img.width // 200)
    try:
        font = ImageFont.truetype("arial.ttf", max(16, img.width // 35))
    except OSError:
        font = ImageFont.load_default()
    for i, b in enumerate(boxes, 1):
        x1, y1, x2, y2 = b["box"]
        draw.rectangle([x1, y1, x2, y2], outline=(230, 30, 30), width=width)
        tag = str(i)
        tw, th = draw.textbbox((0, 0), tag, font=font)[2:]
        ty = y1 - th - 8 if y1 - th - 8 > 0 else y1
        draw.rectangle([x1, ty, x1 + tw + 10, ty + th + 8], fill=(230, 30, 30))
        draw.text((x1 + 5, ty + 2), tag, fill="white", font=font)
    img.save(out_path)
    return out_path
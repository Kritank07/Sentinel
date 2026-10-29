"""Sentinel evaluation.

Runs every case in eval/cases.json through the real product path (the investigate agent),
saves results after each case (so a crash or Ctrl+C never loses progress), then prints metrics.

Usage (from F:\\Sentinel):
    python -m eval.run_eval --limit 5     # quick trial on 5 cases
    python -m eval.run_eval               # full run (skips cases already done)
    python -m eval.run_eval --summary     # only print metrics from saved results
    python -m eval.run_eval --fresh       # discard saved results and start over
"""
import argparse, json, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

from sentinel.engine import investigate

HERE = Path(__file__).parent
CASES = HERE / "cases.json"
RESULTS = HERE / "results.json"
FLAGGED = {"SCAM", "SUSPICIOUS"}          # anything that warns the user counts as "flagged"
lock = Lock()


def load_results() -> dict:
    if RESULTS.exists():
        return {r["id"]: r for r in json.loads(RESULTS.read_text(encoding="utf-8"))}
    return {}


def save_results(results: dict):
    RESULTS.write_text(json.dumps(list(results.values()), indent=2, ensure_ascii=False), encoding="utf-8")


def run_case(case: dict) -> dict:
    start = time.time()
    try:
        v = investigate(case["text"], user_language="English")
        return {**case, "pred": v.get("verdict", "ERROR"), "score": v.get("threat_score"),
                "scam_type_pred": v.get("scam_type"), "seconds": round(time.time() - start, 1)}
    except Exception as e:
        return {**case, "pred": "ERROR", "error": str(e)[:300], "seconds": round(time.time() - start, 1)}


def summarize(results: list[dict]):
    done = [r for r in results if r["pred"] != "ERROR"]
    errors = [r for r in results if r["pred"] == "ERROR"]
    scams = [r for r in done if r["label"] == "SCAM"]
    safes = [r for r in done if r["label"] == "SAFE"]

    caught = [r for r in scams if r["pred"] in FLAGGED]
    caught_strict = [r for r in scams if r["pred"] == "SCAM"]
    false_alarms = [r for r in safes if r["pred"] in FLAGGED]
    correct = len(caught) + (len(safes) - len(false_alarms))

    pct = lambda a, b: f"{100 * a / b:.1f}%" if b else "n/a"
    print("\n" + "=" * 56)
    print(f" SENTINEL EVAL   {len(done)} cases scored, {len(errors)} errors")
    print("=" * 56)
    print(f" Accuracy (flagged vs safe) : {pct(correct, len(done))}  ({correct}/{len(done)})")
    print(f" Scams caught (recall)      : {pct(len(caught), len(scams))}  ({len(caught)}/{len(scams)})")
    print(f"   ...as a firm SCAM verdict: {pct(len(caught_strict), len(scams))}")
    print(f" False alarms on genuine    : {pct(len(false_alarms), len(safes))}  ({len(false_alarms)}/{len(safes)})")
    if done:
        print(f" Average time per check     : {sum(r['seconds'] for r in done) / len(done):.1f}s")

    by_lang = defaultdict(lambda: [0, 0])
    for r in done:
        ok = (r["pred"] in FLAGGED) == (r["label"] == "SCAM")
        by_lang[r["lang"]][0] += ok
        by_lang[r["lang"]][1] += 1
    print("\n Accuracy by language:")
    for lang, (ok, n) in sorted(by_lang.items()):
        print(f"   {lang:<10} {pct(ok, n):>7}  ({ok}/{n})")

    misses = [r for r in scams if r["pred"] not in FLAGGED]
    if misses or false_alarms:
        print("\n Mistakes to review:")
        for r in misses:
            print(f"   MISSED SCAM  {r['id']} [{r['lang']}] {r['category']}: predicted {r['pred']} ({r.get('score')})")
        for r in false_alarms:
            print(f"   FALSE ALARM  {r['id']} [{r['lang']}] {r['category']}: predicted {r['pred']} ({r.get('score')})")
    for r in errors:
        print(f"   ERROR        {r['id']}: {r.get('error', '')[:120]}")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="only run this many new cases")
    ap.add_argument("--workers", type=int, default=3, help="parallel checks (keep low to avoid rate limits)")
    ap.add_argument("--summary", action="store_true", help="only print metrics from saved results")
    ap.add_argument("--fresh", action="store_true", help="discard saved results first")
    args = ap.parse_args()

    if args.fresh and RESULTS.exists():
        RESULTS.unlink()
    results = load_results()

    if not args.summary:
        cases = json.loads(CASES.read_text(encoding="utf-8"))
        # Re-run cases that errored before; skip ones already scored.
        todo = [c for c in cases if c["id"] not in results or results[c["id"]]["pred"] == "ERROR"]
        if args.limit:
            todo = todo[:args.limit]
        print(f"Running {len(todo)} cases ({len(results)} already saved)...")

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run_case, c): c for c in todo}
            for i, fut in enumerate(as_completed(futures), 1):
                r = fut.result()
                with lock:
                    results[r["id"]] = r
                    save_results(results)
                mark = "ok " if (r["pred"] in FLAGGED) == (r["label"] == "SCAM") else "XX "
                if r["pred"] == "ERROR":
                    mark = "ERR"
                print(f"[{i}/{len(todo)}] {mark} {r['id']} {r['label']:<4} -> {r['pred']:<10} {r['seconds']}s")

    summarize(list(results.values()))


if __name__ == "__main__":
    main()
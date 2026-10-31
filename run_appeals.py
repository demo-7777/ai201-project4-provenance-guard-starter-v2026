#!/usr/bin/env python3
"""
Criterion 2 — the appeal path, three trials.

run_eval.py only calls /submit, so the appeal criterion is tested here:

    python app.py                               # in one terminal
    python run_appeals.py --label before        # in another

Each trial submits 5 texts, appeals each real content_id, checks the response
says under_review and that GET /log holds a matching appeal entry, then sends
one appeal with a content_id that was never submitted and checks for a 404
with no appeal entry added.

Target (criteria.md #2): 5 of 5 real appeals confirmed and logged, and the
unknown id gets a 404 with no appeal entry — in every trial.
"""

import argparse
import datetime as dt
import json
import uuid

import requests

import config
import scenarios

URL = f"http://{config.HOST}:{config.PORT}"


def appeal_entries(content_id):
    entries = requests.get(f"{URL}/log", timeout=10).json()["entries"]
    return [e for e in entries
            if e.get("content_id") == content_id and e.get("event") == "appeal"]


def run_trial(trial):
    results = []
    for i, text in enumerate(scenarios.HUMAN_PRE_2020[:5], 1):
        # Own creator_id per submission keeps the rate limiter out of the way.
        submit = requests.post(f"{URL}/submit", timeout=90, json={
            "text": text, "creator_id": f"eval_appeal_t{trial}_{i}"}).json()
        cid = submit["content_id"]
        reasoning = f"I wrote this myself (eval trial {trial}, appeal {i})."
        response = requests.post(f"{URL}/appeal", timeout=10, json={
            "content_id": cid, "reasoning": reasoning})
        logged = appeal_entries(cid)
        results.append({
            "content_id": cid,
            "status_code": response.status_code,
            "response": response.json(),
            "log_entry": logged[-1] if logged else None,
            "passed": (response.status_code == 200
                       and response.json().get("status") == "under_review"
                       and len(logged) == 1
                       and logged[0]["status"] == "under_review"
                       and logged[0]["reasoning"] == reasoning),
        })

    fake = f"never-submitted-{uuid.uuid4()}"
    response = requests.post(f"{URL}/appeal", timeout=10, json={
        "content_id": fake, "reasoning": "This id does not exist."})
    unknown = {
        "content_id": fake,
        "status_code": response.status_code,
        "response": response.json(),
        "appeal_entries_added": len(appeal_entries(fake)),
    }
    unknown["passed"] = (response.status_code == 404
                         and unknown["appeal_entries_added"] == 0)
    return results, unknown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    lines = [f"# Appeal path (criterion 2){f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `run_appeals.py::main`",
             f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for trial in range(1, args.trials + 1):
        results, unknown = run_trial(trial)
        ok = sum(r["passed"] for r in results)
        print(f"trial {trial}: {ok}/5 appeals confirmed and logged; "
              f"unknown id -> {unknown['status_code']}, "
              f"{unknown['appeal_entries_added']} appeal entries "
              f"({'pass' if unknown['passed'] else 'FAIL'})")
        lines += [f"## Trial {trial}: {ok}/5 real appeals passed, "
                  f"unknown id {'passed' if unknown['passed'] else 'FAILED'}", "",
                  "```json", json.dumps({"appeals": results, "unknown_id": unknown},
                                        indent=2, ensure_ascii=False), "```", ""]

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeals_{stamp}{label}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()

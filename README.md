# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a small backend service a writing site could plug into. A piece of writing goes in; a guess, a confidence score, a plain-English label, and a way to appeal come back.

1. **The writer sends JSON `{text, creator_id}` to `POST /submit`** (`app.py::submit`). The route refuses missing, empty, whitespace-only, non-string, or over-9999-character text with a 400 before any signal runs, and logs the refusal.
2. **Signal one** (`detector.py::model_signal`) runs gpt2 locally and scores how predictable the text is (perplexity), 0–1, higher = more likely AI.
3. **Signal two** (`stylometry.py::style_signal`) scores the text's shape — sentence length spread, word variety, punctuation — 0–1, higher = more likely AI.
4. **The combining rule** (`scoring.py::combine_signals`) averages the two 50/50. If they disagree by more than 0.4, the result is held in the unsure band.
5. **The label mapping** (`scoring.py::score_to_label`) turns the combined score into a guess (`human` / `unsure` / `ai`) and the sentence the writer sees, using the thresholds in `config.py`.
6. **The decision is logged** (`audit.py::log_decision` → `logs/audit.jsonl`): timestamp, content_id, creator_id, guess, both signal scores, the combined score, the label, and status `decided`.
7. **The route responds** with `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`, and `status`. The writer sees the label.

If the writer thinks the label is wrong, they send their `content_id` and reasoning to **`POST /appeal`** (`app.py::appeal`). The route checks the content_id exists (404 if not), appends the appeal to the log next to the original decision, sets the status to `under_review`, and confirms. A person then reviews it; nothing is re-scored automatically.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** perplexity — how predictable the submitted text is, word by word, to the gpt2 language model (first ~400 tokens). Low perplexity scores closer to 1 (more likely AI).

**Why that might differ between human and AI writing:** A language model writes by repeatedly picking a likely next word, so its output tends to be easy for another model to predict (low perplexity). Human writing makes more surprising choices — odd words, abrupt turns, specific details — which raises perplexity.

**What it can't see:** Predictability is not authorship. Plain writers, second language writers, younger writers, or anyone using common words in short sentences can score as AI — a false positive on real work. The reverse also happens: dense prose full of rare words, or AI text with unusual words swapped in, can score as human.

### Signal two — the style signal

**What it measures:** surface statistics of the submitted text itself — how much sentence lengths vary, the share of words that are unique, and how much punctuation is used — combined into one 0–1 score where closer to 1 means more likely AI.

**Why that might differ between human and AI writing:** AI writing tends to have consistent, predictable sentence length and a preference for a certain set of words over others. On the other hand, human writing and sentence structure tends to be more volatile and with word choice changing depending on the context or writer's feelings at the moment.

**What it can't see:** It only counts, but doesn't comprehend the text. A writer may try to bypass the signal by inserting or removing certain punctuation or word choices that would signal AI writing. Word variety is also measured within one text, while AI's preference for certain words mostly shows up across many texts — in testing, the AI paragraph actually had the *most* varied vocabulary (0.95), which is why that measure carries the least weight.

**How the three measures combine** (`stylometry.py::style_signal`): each measure is flipped onto a 0–1 AI scale between two anchors, then weighted:

| Measure | Reads fully AI at | Reads fully human at | Weight |
|---|---|---|---|
| Sentence length spread (stdev ÷ mean words per sentence) | 0.20 | 0.60 | 0.4 |
| Word variety (unique ÷ total words, 50-word moving windows) | 0.70 | 0.85 | 0.2 |
| Punctuation (`; : — – ( ) ! ? " …` per 100 words) | 0.0 | 4.0 | 0.4 |

A one-sentence text gets 0.5 on spread, since there is nothing to measure.

**A change to signal one:** I moved the perplexity midpoint in `detector.py::model_signal` from 45 to 25 (the perplexity that scores 0.5). At 45, no human test text scored below about 0.6 on signal one, so the high confidence human label was unreachable. 25 was the smallest change that made all three labels reachable while still catching lightly edited AI.

### The combining rule

**The rule:** A weighted average of the two signals. If the two signals are more than 0.4 apart, the result is held inside the unsure band, so neither "AI" nor "human" can be reached on one signal's say-so — two methods disagreeing is itself uncertainty.

**The numbers:**
- `combined = 0.5 × model_score + 0.5 × style_score`
- If `|model_score − style_score| > 0.4`, `combined` is clamped to 0.36–0.64 (inside the unsure band)
- Label thresholds: ≤ 0.35 human, ≥ 0.65 AI, unsure in between
- All in `config.py`: `WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`, `DISAGREEMENT_GAP`, `HUMAN_THRESHOLD`, `AI_THRESHOLD`

Equal weights because I had no evidence yet that one signal deserves more trust than the other; the disagreement rule handles the cases where they split instead.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

A 2015 NASA news release about the New Horizons Pluto flyby (human-written). Signal one scored it 0.53 — formal news prose is predictable to gpt2, and an article this widely published may even be in its training data. Signal two scored it 0.00 — uneven sentence lengths and lots of quotes and dashes. The gap is 0.53, over the 0.4 limit, so the rule holds the result in the unsure band: combined 0.36, label **unsure**. Without the rule, the average would be 0.27 — "human" — on the strength of signal two alone.

Calibration results (midpoint 25):

| Text | model | style | combined | label |
|---|---|---|---|---|
| Clearly AI (generated, unedited) | 0.74 | 0.80 | 0.77 | ai |
| Lightly-edited AI (typos, a few words changed) | 0.56 | 0.80 | 0.68 | ai |
| Human — NASA 2015 news release | 0.53 | 0.00 | 0.36 | unsure |
| Plain human — FTC press release | 0.38 | 0.18 | 0.28 | human |
| Reflective, AI-sounding "between" text | 0.70 | 0.51 | 0.60 | unsure |

Typos alone raised the edited AI's perplexity from 12.9 to 21.3 — signal one's blind spot in action. Signal two didn't move at all, because the edits didn't change sentence lengths or punctuation.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | Human: Your submission appears to be human written. |
| unsure | above 0.35, below 0.65 | Mixed: Your submission is difficult to tell if it was AI generated or human written. |
| high-confidence AI | 0.65 – 1.00 | AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal]. |

*Unit 8: the AI threshold was raised from 0.65 to 0.75 as my one improvement, so unsure now covers above 0.35 to below 0.75 and high-confidence AI covers 0.75–1.00. The label text is unchanged. See The Improvement.*

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->
Other AI detection tools online have used the term "Mixed" to refer to a submission they are unsure of. In the context of this system, a submission may lead to unsure because it has a mixture of elements that suggest both AI or human generated text.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

`para.txt` contains this human-written NOAA article excerpt:

> His name might not sound familiar to you, but George Pollard was a whaling captain from Nantucket, Massachusetts, in the 19th century. His previous whaling vessel, the Essex, had been rammed by a whale and sunk. Pollard’s story — which included drifting on the open ocean and, eventually, cannibalism — found its way to Herman Melville, who used the incident as fodder for his classic novel, Moby Dick. Years later and in control of the vessel Two Brothers, Pollard gained notoriety again when his ship hit a shallow reef off French Frigate Shoals in Hawaii on the night of Feb. 11, 1823. Fearing a repeat of his harrowing experience with the Essex, Pollard hesitated about what to do but his crew persuaded him to abandon ship. They all spent a long night clinging to small boats for survival and were rescued the next morning by a passing ship. As for the Two Brothers, it was lost beneath the ocean for 188 years. Until 2008. That year, during a NOAA-led expedition to study marine archaeology in the Northwestern Hawaiian Islands, Two Brothers was found again, 600 miles northwest of Honolulu, in Papahānaumokuākea Marine National Monument.

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" \
  -d "$(python -c 'import json; print(json.dumps({"text": open("para.txt").read(), "creator_id": "u1"}))')"
```

```json
{
  "confidence": 0.4037,
  "content_id": "483ee8b7-4f23-4844-8be4-e97d60b755c4",
  "guess": "unsure",
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "model_score": 0.4928,
  "status": "decided",
  "style_score": 0.3146
}
```

**An appeal**

First with a content_id that doesn't exist, then with the real one from the submission above:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" \
  -d '{"content_id": "PASTE-ID", "reasoning": "I wrote this myself."}'
```

```json
{
  "error": "not_found",
  "message": "No submission with content_id PASTE-ID."
}
```

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" \
  -d '{"content_id": "483ee8b7-4f23-4844-8be4-e97d60b755c4", "reasoning": "I wrote this myself."}'
```

```json
{
  "content_id": "483ee8b7-4f23-4844-8be4-e97d60b755c4",
  "message": "Your appeal has been recorded. A person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

The original decision, the rejected appeal on the unknown id, and the real appeal — appended after the decision, which stays unchanged:

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.4037,
      "content_id": "483ee8b7-4f23-4844-8be4-e97d60b755c4",
      "creator_id": "u1",
      "guess": "unsure",
      "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
      "model_score": 0.4928,
      "status": "decided",
      "style_score": 0.3146,
      "timestamp": "2026-10-24T22:22:02+00:00"
    },
    {
      "attempted_content_id": "PASTE-ID",
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "appeal_unknown_content_id",
      "status": "rejected",
      "timestamp": "2026-10-24T22:22:15+00:00"
    },
    {
      "content_id": "483ee8b7-4f23-4844-8be4-e97d60b755c4",
      "creator_id": "u1",
      "event": "appeal",
      "reasoning": "I wrote this myself.",
      "status": "under_review",
      "timestamp": "2026-10-24T22:23:23+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked the AI to write `test_signals.sh` so I could paste in test paragraphs (clearly AI, lightly-edited AI, two human news releases, and an in-between text) and see both signal scores, the combined score, and the label side by side.
- *What came back:* The table showed no input could reach the "human" label. Signal one never scored a human text below about 0.6, so the combined score couldn't get under 0.35 without the two signals disagreeing by more than 0.4, which my disagreement rule sends to "unsure". The AI suggested moving the detector's perplexity midpoint and showed the labels at 45, 25, 20, 18 and 15.
- *What I changed:* I moved the midpoint from 45 to 25, the smallest change that made all three labels reachable while lightly-edited AI was still caught. I chose it over 20, which let the edited AI slip to "unsure".

**Moment 2**

- *What I asked for:* I asked the AI to build the three style measures in `stylometry.py` (sentence length spread, word variety, punctuation) and run them on my test paragraphs.
- *What came back:* Word variety ran the opposite way from the lab's hypothesis — the AI paragraph had the *most* varied vocabulary (0.95 vs 0.86–0.88 for the human texts), so with equal weights that measure read every text as human and added nothing. The AI suggested to either drop it, flip its direction, or keep it and report it as a measure that doesn't discriminate.
- *What I changed:* I kept my hypothesis that AI draws on a smaller set of words, so the direction stayed the same, but I cut its weight from 1/3 to 0.2 and raised sentence length spread and punctuation to 0.4 each. The AI pointed out that a single text can't show AI's preference for certain words, since that appears across many texts, so I added that to signal two's blind spot.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 9 per minute, 99 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`)

**Why those numbers and not others:**
A real writer submits their own work a few times an hour at most. 9 a minute still leaves room for a burst — fixing a typo and resubmitting, or posting a few short pieces back to back — without ever hitting the limit. 99 a day is far more than any one person writes in a day.

A script trying to map my thresholds needs hundreds or thousands of variations to find where 0.35 and 0.65 sit. At 9 a minute, 1,000 probes take nearly two hours instead of seconds, and the 99 a day cap stops it after 99 no matter how patient it is. Every rejected request is logged, so the probing shows up in the log instead of disappearing.

**What a caller counts as:** per `creator_id`, falling back to the caller's address when a request has no usable `creator_id` (`app.py::rate_limit_key`). This stops one writer account flooding the service, but a script that makes up a new `creator_id` for every request looks like many different callers and isn't limited at all. Per-address limiting would catch that script, but would also lump together everyone sharing one network (a household or a school).

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
15 submissions as 'flood_tester' against http://127.0.0.1:5000

200 200 200 200 200 200 200 200 200 429 429 429 429 429 429

6 of 15 were rate limited.
Wrote results/flood_2026-10-31_1801.md
```

The rejections land in the audit log (`GET /log`):

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "9 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-10-31T22:01:40+00:00"
}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Produced by `run_attacks.py::main` → `results/attack_run_2026-11-04_2104_before.md` (56 attacks).

**How I marked them:**
- **AI text breaks only if it is labeled human.** (Evasion EV01–EV10, and the prompt injections built on AI text: PI01, PI02, PI03, PI05.) `unsure` holds — the system didn't vouch for it.
- **Human text breaks only if it is labeled AI.** (False positives FP01–FP08, the injections built on human text — PI04, PI06 — and MF07, which is real Arabic writing.) `unsure` holds — the same rule as criterion 3.
- **Junk input** (MF03–MF06, not writing at all) breaks on a 5xx or a confident `ai`/`human` label; a 400 or `unsure` holds.
- **Malformed requests** hold on a 4xx. **Flood rows** hold if the limiter lets the first 9 through and returns 429 after.

**Totals: 39 held, 17 broke.**

| Family | Held | Broke |
|---|---|---|
| Evasion | 6 | 4 |
| False positive | 2 | **6** |
| Prompt injection | 2 | 4 |
| Malformed (text + requests) | 17 | 3 |
| Flood same creator | 12 | 0 |

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.435 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | human | 0.217 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | human | 0.309 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.590 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.217 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.373 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | human | 0.281 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.415 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.507 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.877 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.494 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.696 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.665 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.666 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.767 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.675 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | ai | 0.672 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.362 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.326 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.135 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | human | 0.310 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | human | 0.246 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | human | 0.269 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.468 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.360 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.502 | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.797 | BROKE |
| MF06 | malformed | text is emoji only | 200 | ai | 0.896 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.795 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

**An earlier run that crashed.** My first attack run (`results/attack_run_2026-11-04_2056_before.md`) came back with 37 failures: EV01 timed out, and every scored request after EV02 returned 500 with `RuntimeError: Tensor.item() cannot be called on meta tensors`. The inputs weren't the cause — the server had just been restarted, so the model loaded on the first request, and that load outlasted the runner's 90-second timeout. The next request arrived while the model was still loading and started a second load in parallel; the two loads collided and left a broken model in memory, so every later submission crashed. I kept that run as evidence, restarted, warmed the model up with one submission, and ran the set again with no code changes — the table above is that second run. (Diagnosed below.)

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl` (read through `GET /log`):

```json
{"timestamp": "2026-11-05T02:03:41+00:00", "content_id": "532bd4c2-5625-4a3a-9ef3-ad425d6e42b4", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.6173, "style_score": 0.7126, "combined_score": 0.6649, "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].", "status": "decided"}
{"timestamp": "2026-11-05T02:03:44+00:00", "content_id": "440d0ca6-f28c-439e-8ad4-0eb05537fecf", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.6104, "style_score": 0.9231, "combined_score": 0.7668, "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].", "status": "decided"}
{"timestamp": "2026-11-05T02:04:08+00:00", "content_id": "8a4471d0-6794-4633-bbc6-dd4352950738", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.7908, "style_score": 0.8, "combined_score": 0.7954, "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].", "status": "decided"}
{"timestamp": "2026-11-05T02:03:16+00:00", "content_id": "0c2c582e-67b4-4519-bf85-cd954eb697ed", "creator_id": "attacker_EV02", "guess": "human", "model_score": 0.3638, "style_score": 0.0703, "combined_score": 0.2171, "label": "Human: Your submission appears to be human written.", "status": "decided"}
{"timestamp": "2026-11-05T02:03:22+00:00", "content_id": "6fef2866-380f-4087-aed0-a2607484a848", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.1559, "style_score": 0.278, "combined_score": 0.217, "label": "Human: Your submission appears to be human written.", "status": "decided"}
{"timestamp": "2026-11-05T02:03:50+00:00", "content_id": "a019c053-548e-4eec-992b-31f9cac3729c", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.0912, "style_score": 0.1778, "combined_score": 0.1345, "label": "Human: Your submission appears to be human written.", "status": "decided"}
{"timestamp": "2026-11-05T02:03:53+00:00", "content_id": "d860ea10-7c76-4e47-92d4-96e0f863c6d4", "creator_id": "attacker_PI05", "guess": "human", "model_score": 0.4099, "style_score": 0.1286, "combined_score": 0.2692, "label": "Human: Your submission appears to be human written.", "status": "decided"}
{"timestamp": "2026-11-05T02:04:07+00:00", "content_id": "e3c4f22f-f6c2-49ec-b9e3-4a5c3d2c2174", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9921, "style_score": 0.8, "combined_score": 0.8961, "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].", "status": "decided"}
{"timestamp": "2026-11-05T02:03:34+00:00", "content_id": "bdfb9349-6dbd-4e88-9187-92d12b34948d", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9483, "style_score": 0.8061, "combined_score": 0.8772, "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].", "status": "decided"}
{"timestamp": "2026-11-05T02:04:08+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "invalid_input", "message": "text is longer than 9999 characters"}
{"timestamp": "2026-11-05T02:04:13+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "9 per 1 minute"}
```

What they show: three human writers labeled AI (FP03 non-native speaker, FP05 technical writer, MF07 Arabic writing); three AI texts labeled human (EV02 broken-up sentences, EV05 heavy editing, PI02 injected "SYSTEM" line); PI05's attempt to forge log fields — the entry is still one well-formed JSON object with the real scores, because the submitted text is never written to the log; emoji scored 0.99 on signal one; one AI text caught (EV10) for contrast; and two rejections — a 400 refusal and a 429 from the flood rows. The rejections carry fewer fields than decisions, as expected.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03 — a non-native English speaker writing carefully, labeled AI (0.665).** This is the exact person I traced through the system in Milestone 1, and it happened the way I predicted: careful writing in a second language uses common words in short, regular sentences, so signal one finds it predictable (0.62) and signal two finds its shape even (0.71). Both signals agree, so the disagreement rule doesn't step in, and the score lands just over the 0.65 line. The writer is told "Your submission appears to be AI generated" — about work they wrote themselves, in a language they're still learning — and the only way out the label offers them is "[POST /appeal]", which means nothing to someone who isn't a developer.



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Bad input returns 400, never 500 or a label | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Appeals confirmed and logged; unknown id gets 404 | 5 of 5 + 404 | 5/5 + 404 | 5/5 + 404 | 5/5 + 404 | MET |
| 3. Pre-2020 human pieces labeled AI | ≤ 1 of 10 | 1/10 | 1/10 | 1/10 | MET |
| 4. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 5. Mean AI score − mean human score | ≥ 0.50 | 0.331 | 0.331 | 0.331 | MISSED |

All three trials were identical for every criterion — neither signal is random, so this is the expected result.

**How each verdict was decided:**
1. Every bad body returned status 400 with no guess or label, in all three trials. (`run_eval.py` records the status code but not the body; the `error` field comes from `app.py::_reject`, which every 400 from `/submit` goes through.)
2. In every trial, all 5 appeals returned `under_review` and had exactly one matching appeal entry in `GET /log` with the same reasoning; the never-submitted id returned 404 and added no appeal entry.
3. Exactly 1 of 10 came back `ai` in every trial — at the target, not under it. Only 2 of 10 reached `human`; the other 7 were `unsure`.
4. `human`, `unsure`, and `ai` each appeared at least once in every trial.
5. AI mean 0.759, human mean 0.428 — a gap of 0.331 in every trial, short of 0.50.

**Real output from one trial** (trial 1). Criteria 1, 3, 4, 5 from `run_eval.py::main` → `results/run_2026-10-31_1919_before.md`; criterion 2 from `run_appeals.py::main` → `results/appeals_2026-10-31_1922_before.md`.

*Criterion 1 — bad input (all five bodies):*

```json
[
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"creator_id\": \"eval_bad_missing\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "(empty text)"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "   "},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"text\": 5, \"creator_id\": \"eval_bad_number\"}"}
]
```

*Criterion 2 — one real appeal and the unknown id:*

```json
{
  "appeals": [
    {
      "content_id": "3b203df6-39f3-4065-b5e8-ef5e0dc35c05",
      "status_code": 200,
      "response": {
        "content_id": "3b203df6-39f3-4065-b5e8-ef5e0dc35c05",
        "message": "Your appeal has been recorded. A person will review it.",
        "status": "under_review"
      },
      "log_entry": {
        "content_id": "3b203df6-39f3-4065-b5e8-ef5e0dc35c05",
        "creator_id": "eval_appeal_t1_1",
        "event": "appeal",
        "reasoning": "I wrote this myself (eval trial 1, appeal 1).",
        "status": "under_review",
        "timestamp": "2026-10-31T23:22:16+00:00"
      },
      "passed": true
    }
  ],
  "unknown_id": {
    "content_id": "never-submitted-a2c2d155-adab-48ec-b358-8be6f5f9d7c2",
    "status_code": 404,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id never-submitted-a2c2d155-adab-48ec-b358-8be6f5f9d7c2."
    },
    "appeal_entries_added": 0,
    "passed": true
  }
}
```

*Criterion 3 — the one human piece labeled AI:*

```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.6784,
  "model_score": 0.6113,
  "style_score": 0.7454,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
  "sent": "In 2016, my word was Grace. That was the perfect word for my first yea"
}
```

*Criterion 4 — one result for each label:*

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.36, "model_score": 0.5292, "style_score": 0.0, "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.", "sent": "The call everyone was waiting for is in. NASA’s New Horizons spacecraf"},
  {"status": 200, "guess": "ai", "confidence": 0.7717, "model_score": 0.7434, "style_score": 0.8, "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].", "sent": "Artificial intelligence has become an increasingly important aspect of"},
  {"status": 200, "guess": "human", "confidence": 0.2781, "model_score": 0.3777, "style_score": 0.1785, "label": "Human: Your submission appears to be human written.", "sent": "This week, an administrator working for the Federal Trade Commission b"}
]
```

*Criterion 5 — the combined scores (`confidence`) behind the gap:*

```
AI texts:     0.7717  0.7117  0.7719  0.7403  0.8014   mean 0.759
Human texts:  0.3600  0.5859  0.4037  0.3600  0.4328   mean 0.428
Gap: 0.331 (target ≥ 0.50)
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Criterion 5 (score spread) — MISSED, gap 0.331 vs ≥ 0.50.**

Signal scores behind it (trial 1):

| Group | mean model_score | mean style_score |
|---|---|---|
| 5 clearly AI | 0.706 | 0.813 |
| 5 clearly human (press releases/articles) | 0.554 | 0.249 |
| **Separation** | **0.152** | **0.564** |

- **Stage: signal one. Mechanism: formal institutional prose is predictable to gpt2.** Signal one separates the two groups by only 0.15. The human texts are government press releases — formulaic sentences, standard phrasing ("according to a new study", "said … director of"), the kind of text that fills gpt2's training data — so their perplexity is low and they score like AI. The CDC sleep release scored 0.77 on signal one, *higher* than three of the five AI texts. Signal two separates the groups by 0.56 on its own.
- **Stage: the combining rule. Mechanism: equal weights halve the good signal, and the disagreement rule lifts the lowest human scores.** At 0.5/0.5, the combined separation is the average of the two: 0.5 × 0.152 + 0.5 × 0.564 = 0.358 — already under 0.50 before anything else happens. Then two human texts (NASA, gap 0.53; honey bees, gap 0.54) had signals more than 0.4 apart, so the disagreement rule raised them from 0.265 and 0.320 to the 0.36 floor. That added 0.027 to the human mean and brought the gap to 0.331.

So the miss is one problem with two parts: signal one barely tells formal human writing from AI, and the combining rule gives it half the say. With these weights, no threshold change can reach 0.50 — it needs either more weight on signal two or a signal one that separates better.

**A close call worth noting — criterion 3 (met at exactly 1 of 10).** The one false positive was a plain personal blog post ("In 2016, my word was Grace…"): model 0.61, style 0.75. **Stage: signal two. Mechanism: plain personal writing has the even rhythm signal two treats as AI.** It is a run of similar length sentences built the same way ("I learned I have… I learned sometimes… I learned the importance…") with almost no punctuation beyond commas and full stops, so sentence length spread and punctuation both read as AI. Three of the other four plain pieces also scored 0.58–0.65 on signal two. Signal two catches formal human text well but leans toward accusing plain writers — the opposite blind spot from signal one.

**The attack set — 17 broken attacks, plus the crashed first run.**

Signal two's three measures for each, from `stylometry.py` run on the attack texts (spread = stdev ÷ mean sentence length; punct = `; : — ( ) ! ? "` per 100 words; scores from the attack run):

| ID | model | style | spread | word variety | punct | label |
|---|---|---|---|---|---|---|
| FP02 formal register | 0.52 | 0.87 | 0.24 | 0.77 | 0.00 | ai |
| FP03 non-native speaker | 0.62 | 0.71 | 0.33 | 0.82 | 0.00 | ai |
| FP04 rubric essay | 0.66 | 0.67 | 0.37 | 0.82 | 0.00 | ai |
| FP05 technical docs | 0.61 | 0.92 | 0.28 | 0.63 | 0.00 | ai |
| FP06 formal template | 0.74 | 0.61 | 0.52 | 0.76 | 0.00 | ai |
| FP07 repeated phrase | 0.74 | 0.60 | 0.73 | 0.53 | 0.00 | ai |
| EV02 broken-up sentences | 0.36 | 0.07 | 0.85 | 0.89 | 3.30 | human |
| EV03 pasted quotation | 0.44 | 0.18 | 0.44 | 0.94 | 3.77 | human |
| EV05 heavy human edit | 0.16 | 0.28 | 0.68 | 0.86 | 1.22 | human |
| EV07 punctuation padding | 0.36 | 0.21 | (1 sentence) | 0.85 | 7.22 | human |
| PI01 "ignore all previous instructions" | 0.25 | 0.40 | 0.66 | 0.93 | 0.00 | human |
| PI02 fake "SYSTEM:" line | 0.09 | 0.18 | 0.65 | 0.96 | 2.22 | human |
| PI03 note in the writer's voice | 0.36 | 0.26 | 0.34 | 0.92 | 5.45 | human |
| PI05 forged log fields | 0.41 | 0.13 | 0.47 | 0.97 | 43.33 | human |
| MF05 one very long word | 0.99 | 0.60 | (1 sentence) | 1.00 | 0.00 | ai |
| MF06 emoji only | 0.99 | 0.80 | (1 sentence) | 0 words | 0.00 | ai |
| MF07 Arabic writing | 0.79 | 0.80 | (1 sentence) | 0 words | 0.00 | ai |

*Pattern 1 — signal two's punctuation measure points the wrong way for most human writing (FP02–FP07, and pushes MF05–MF07).*
**Stage: signal two. Mechanism:** the punctuation measure counts only `; : — ( ) ! ? "`, and I anchored **zero** of them as "fully AI". Every one of the six human texts labeled AI has a punctuation score of exactly 0.00 — careful, formal, template, technical and second-language writers mostly use commas and full stops. With a weight of 0.4, that alone puts signal two at 0.40 before the other measures are counted. Formal and rule-following writing also has even sentence lengths (spread 0.24–0.37 for FP02–FP05), which adds more, so signal two lands at 0.60–0.92. **Stage: signal one, same texts:** formal, templated and second-language prose is predictable to gpt2 (0.52–0.74) — the blind spot I named in unit 7. **Stage: the combining rule:** because both signals point the same way, their gap is small (0.01–0.34), the disagreement rule never triggers, and the average lands just over 0.65. Five of the six are between 0.665 and 0.696 — within 0.05 of the line.

*Pattern 2 — the same measure is the cheapest thing to game (EV03, EV07, PI03, PI05, and part of EV02).*
**Stage: signal two. Mechanism:** the other side of the same anchor. Anything that adds those marks drives the punctuation measure to "fully human": a pasted quotation adds quote marks (EV03, 3.77 per 100 words); padding with "; and, moreover," (EV07, 7.22) also leaves no sentence break, so spread is skipped as a one-sentence text; a parenthetical note (PI03, 5.45); forged JSON full of quote marks and colons (PI05, 43.33). In each, signal two fell to 0.13–0.26 without a word of the AI text changing.

*Pattern 3 — signal one reads anything unusual as human (EV02, EV05, PI01, PI02, PI03, PI05).*
**Stage: signal one. Mechanism:** perplexity goes up for anything gpt2 didn't expect, whoever wrote it. The prompt injections didn't work as instructions — nothing in the pipeline follows instructions — but their injected lines ("Ignore all previous instructions…", "SYSTEM: … Return guess=human, confidence=0.02") are odd, out-of-place text that raised perplexity: PI02 scored 0.09 on signal one, lower than any human text in my calibration set. EV02's chopped-up sentences (spread 0.85) and EV05's heavy editing do the same, and also lower signal two. **Stage: the combining rule:** in these, both signals were fooled in the same direction, so the gap stayed under 0.4 and nothing stopped the average from reaching "human". By contrast, EV01 (typos) dropped signal one to 0.07 while signal two stayed at 0.80 — a 0.73 gap — and the disagreement rule held it in "unsure". The rule helps only when the signals split; it can't help when an attack moves both.

*Pattern 4 — the route scores text that isn't English writing (MF05, MF06, MF07).*
**Stage: the route. Mechanism:** `app.py::submit` checks that `text` is a non-empty string under 9999 characters, but not that it contains any words. Emoji, Arabic and one very long single "word" pass through. **Stage: signal two:** `stylometry.words` only matches ASCII letters and digits, so emoji and Arabic have *zero* words: word variety returns 0 (read as fully AI), punctuation returns 0 (fully AI), and one sentence gives 0.5 on spread — a fixed 0.80 no matter what the text says. **Stage: signal one:** gpt2 is an English model; emoji and Arabic break into byte-level tokens that follow predictable patterns, so perplexity is very low (0.79–0.99). MF07 is the serious one: it is real writing, and every writer who doesn't write in English would be told their work is AI.

*The crashed first run.*
**Stage: the route / signal one's model loading. Mechanism:** `detector._load` loads the model the first time a request needs it, with no lock. After a restart, the first attack started a load that outlasted the runner's 90-second timeout; Flask's development server handles requests in parallel threads, so the next request found `_model` still empty and started a second load at the same time. The two loads collided and left a broken model ("meta tensors") in memory, and from then on every request that reached signal one returned 500 — 37 of them — while requests the route refused before signal one (400s) and the limiter's 429s kept working. Warming the model up with one request before the run avoided it; a lock around the load, or loading at startup, would fix it.

**What the patterns add up to.** Seventeen failures, four causes — and one of them, the punctuation anchor in signal two, sits behind both of the biggest families: it accuses human writers who don't use semicolons and dashes, and it clears AI text that does. That also changes my criterion 5 reading: giving signal two more weight would widen the score spread on my calibration set but make the false positives here worse, because on plain and formal human writing signal two is the signal that's wrong.



---

## The Improvement

**What I changed:** I raised the AI threshold from **0.65 to 0.75** (`config.py::AI_THRESHOLD`) — one number, nothing else. The unsure band widens from 0.35–0.65 to 0.35–0.75. The disagreement rule's upper clamp is set relative to that threshold, so it moves with it from 0.64 to 0.74; that doesn't change any label, because both values sit inside "unsure". The new ranges:

| Label | Before | After |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | 0.00 – 0.35 |
| unsure | above 0.35, below 0.65 | above 0.35, below 0.75 |
| high-confidence AI | 0.65 – 1.00 | 0.75 – 1.00 |

**Which diagnosis pointed at it:** Pattern 1 — false positives were the worst family (6 of 8 human texts labeled AI), and **five of those six scored between 0.665 and 0.696**, within 0.05 of the old line. Both signals were fooled in the same direction on them, so the disagreement rule never stepped in; the threshold was the last stage that could. Wrongly accusing a writer is the expensive mistake, so I chose the change that moves the line away from them.

Before choosing, I simulated four options on the scores already recorded (re-scoring signal two offline; signal one from the run files). The simulation of the current system reproduced the real 17 broken attacks exactly:

| Option (simulated) | Broken attacks | False positives | Evasions | C5 gap | Clear AI labeled AI |
|---|---|---|---|---|---|
| No change | 17 | 6 | 4 | 0.331 | 5/5 |
| Zero rare punctuation counts as neutral | 12 | 1 | 5 | 0.231 | 3/5 |
| Punctuation measure removed | 12 | 2 | 5 | 0.267 | 4/5 |
| **AI threshold 0.65 → 0.75** | **12** | **1** | **4** | **0.331** | **3/5** |

The threshold change matched or beat the punctuation fixes on every column. The punctuation fixes also showed something I hadn't expected: my clear-AI texts *also* have zero rare punctuation, so making zero neutral pulled them down too. The measure doesn't separate plain human writing from AI at all — both leave those marks out.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Produced by `run_attacks.py::main` → `results/attack_run_2026-11-04_2139_after.md`. Same marking rules as the before run. Warmed up with one submission before the run.

**Totals: 44 held, 12 broke** (before: 39 held, 17 broke).

| Family | Before: held / broke | After: held / broke |
|---|---|---|
| Evasion | 6 / 4 | 6 / 4 |
| False positive | 2 / 6 | **7 / 1** |
| Prompt injection | 2 / 4 | 2 / 4 |
| Malformed (text + requests) | 17 / 3 | 17 / 3 |
| Flood same creator | 12 / 0 | 12 / 0 |

Every score is identical to the before run — only labels changed — which confirms the threshold was the only thing that moved. The five rows that changed:

| ID | Score | Before | After |
|---|---|---|---|
| FP02 formal register | 0.696 | ai — BROKE | unsure — HELD |
| FP03 non-native speaker | 0.665 | ai — BROKE | unsure — HELD |
| FP04 rubric essay | 0.666 | ai — BROKE | unsure — HELD |
| FP06 formal template | 0.675 | ai — BROKE | unsure — HELD |
| FP07 repeated phrase | 0.672 | ai — BROKE | unsure — HELD |

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.435 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | human | 0.217 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | human | 0.309 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.590 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.217 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.373 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | human | 0.281 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.415 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.507 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.877 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.494 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.696 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.665 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.666 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.767 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.675 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.672 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.362 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.326 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.135 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | human | 0.310 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | human | 0.246 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | human | 0.269 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.468 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.360 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.502 | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.797 | BROKE |
| MF06 | malformed | text is emoji only | 200 | ai | 0.896 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.795 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.360 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

### Run Log — After

Produced by `run_eval.py::main` → `results/run_2026-11-04_2141_after.md` (criteria 1, 3, 4, 5) and `run_appeals.py::main` → `results/appeals_2026-11-04_2142_after.md` (criterion 2).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict | Before |
|---|---|---|---|---|---|---|
| 1. Bad input returns 400, never 500 or a label | 5 of 5 | 5/5 | 5/5 | 5/5 | MET | MET (5/5) |
| 2. Appeals confirmed and logged; unknown id gets 404 | 5 of 5 + 404 | 5/5 + 404 | 5/5 + 404 | 5/5 + 404 | MET | MET |
| 3. Pre-2020 human pieces labeled AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET | MET (1/10) |
| 4. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET | MET |
| 5. Mean AI score − mean human score | ≥ 0.50 | 0.331 | 0.331 | 0.331 | MISSED | MISSED (0.331) |

*Criterion 3 — the piece that was the false positive before, now:*

```json
{"status": 200, "guess": "unsure", "confidence": 0.6784, "model_score": 0.6113, "style_score": 0.7454, "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.", "sent": "In 2016, my word was Grace. That was the perfect word for my first yea"}
```

*Criterion 5 — the same scores as before, now with labels:*

```
AI texts:     0.7717 ai   0.7117 unsure   0.7719 ai   0.7403 unsure   0.8014 ai   mean 0.759
Human texts:  0.3600      0.5859          0.4037      0.3600          0.4328      mean 0.428
Gap: 0.331 (target ≥ 0.50) — unchanged
```

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

**Yes, for the problem it targeted.** Broken false-positive attacks fell from 6 to 1, and criterion 3 went from exactly at its limit (1/10) to 0/10. I know it was the threshold and nothing else because every score in both the attack run and the eval run is identical before and after — only labels crossed the new line. No evasion broke that held before, and criteria 1, 2 and 4 stayed MET.

**What it cost.** Real AI text now has to score 0.75 to be called AI. In my score-spread set, 2 of the 5 clearly-AI texts (Halloween 0.712, peanut butter 0.740) dropped from "ai" to "unsure"; in the attack set, any AI text scoring 0.65–0.75 would now land in "unsure" too. Those writers aren't cleared — they get the unsure label — but the site is told less often that something is AI. That's the trade I chose: fewer wrong accusations, paid for with more AI text left unlabeled.

**What it didn't fix.** FP05 (technical documentation, 0.767) is still labeled AI — it sits above the new line. The four evasion breaks and four injection breaks are untouched, because those score far *below* the threshold (0.13–0.33); no move of the AI threshold can affect them. Criterion 5 is still missed, because moving a threshold changes labels, not scores. The cause I diagnosed — the punctuation anchor in signal two — is still there; the threshold only moves the line away from where it does the most harm.



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

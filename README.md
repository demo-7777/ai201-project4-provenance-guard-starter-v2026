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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



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

# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 21:39
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c7f09779-659e-4d59-9a7c-68946fe0a312` | unsure | 0.435 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `4d38ec94-3c9a-43e9-b55a-4f78630fee5d` | human | 0.217 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4179deba-7ebe-46ab-96e5-57afbcdad1aa` | human | 0.309 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ea8d7453-80d6-4098-b722-ee27257e0637` | unsure | 0.590 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `68e25213-b461-4162-992f-4f2efafbae01` | human | 0.217 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `994363e7-3ca8-4e18-b220-f6fbc190397e` | unsure | 0.373 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `32b16026-0af1-4495-b847-ba2785ff6d73` | human | 0.281 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `10e4c7e4-51ef-4222-9c15-019907ceb4ef` | unsure | 0.415 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `41141b3f-aca9-4983-97bc-7a89bde6d174` | unsure | 0.507 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `2deb9df9-4dae-48b3-a1e7-f8e880a03785` | ai | 0.877 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d2119d47-12b2-40ce-90b8-6ca555dbfad7` | unsure | 0.494 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `8a7c7f07-7fda-4cb4-890f-b53434a80d04` | unsure | 0.696 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `49da6e45-381e-4612-a63a-eef19dac5a6e` | unsure | 0.665 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `6df1c1cc-a74a-4b87-9bf0-3082e3cfee05` | unsure | 0.666 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `0764550b-d4c0-447b-a37c-137b55f36c3f` | ai | 0.767 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `71975e62-97e2-460e-bb1b-4ba1fda98cb0` | unsure | 0.675 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `8e742162-4d91-4471-8a1f-468b73348f7e` | unsure | 0.672 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `624df8de-162b-428c-ba19-895b7c1c4038` | unsure | 0.362 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `f7f21dea-2c48-4b5c-87ad-bdaa2a240426` | human | 0.326 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cae396d3-bcd4-408f-b3be-999c2471fd91` | human | 0.135 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `3c729f8a-e9b7-4c71-9d15-055ff16fa015` | human | 0.310 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3ba1cf5d-181a-4b95-af34-ec06cebe76f3` | human | 0.246 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `2961e7e1-80ab-4eca-9c4d-4f7cc0ce720a` | human | 0.269 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `084806b1-1927-43b3-a83b-a0c5ddf127f3` | unsure | 0.468 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `4bfba20a-49a3-4bf6-8636-e55e47276287` | unsure | 0.360 |  |
| MF04 | malformed | text is only punctuation | 200 | `76b46f33-92ee-4304-9aae-ddf65c5133b5` | unsure | 0.502 |  |
| MF05 | malformed | text is a very long single word | 200 | `b497d9a6-4e6f-441e-8ecd-1c02d9b026bc` | ai | 0.797 |  |
| MF06 | malformed | text is emoji only | 200 | `38f4667d-d4f9-4293-b203-ddf7bb3561e7` | ai | 0.896 |  |
| MF07 | malformed | text is right-to-left script | 200 | `210d52e7-c78f-4d6f-bece-6b29591b0a90` | ai | 0.795 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `59419562-d440-4c14-bc07-56cbde62e82a` | unsure | 0.360 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `920e50ea-da57-4377-9a07-3435cb305ee7` | unsure | 0.360 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6b4ca690-5fba-471c-bd47-1a3c3cc1f35a` | unsure | 0.360 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3bb0bed8-a582-4bb6-96a0-55e09ffd6b90` | unsure | 0.360 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `62d4a3eb-e292-452c-8d2f-44dccac15e3d` | unsure | 0.360 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e658ec64-e5ed-4bfc-a197-bbb2ad784d52` | unsure | 0.360 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a85aa9f4-e87c-4f36-9efc-58dfb10110f8` | unsure | 0.360 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `95c956a2-a080-4c10-ac4c-46eac02f6087` | unsure | 0.360 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1e982d1d-cce6-4fb6-a5f8-8fa7ecd4e243` | unsure | 0.360 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c7f09779-659e-4d59-9a7c-68946fe0a312",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4355,
  "model_score": 0.0709,
  "style_score": 0.8,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "4d38ec94-3c9a-43e9-b55a-4f78630fee5d",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.2171,
  "model_score": 0.3638,
  "style_score": 0.0703,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "4179deba-7ebe-46ab-96e5-57afbcdad1aa",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.3086,
  "model_score": 0.438,
  "style_score": 0.1793,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ea8d7453-80d6-4098-b722-ee27257e0637",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5903,
  "model_score": 0.3806,
  "style_score": 0.8,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "68e25213-b461-4162-992f-4f2efafbae01",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.217,
  "model_score": 0.1559,
  "style_score": 0.278,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "994363e7-3ca8-4e18-b220-f6fbc190397e",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3726,
  "model_score": 0.3435,
  "style_score": 0.4016,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "32b16026-0af1-4495-b847-ba2785ff6d73",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.2811,
  "model_score": 0.3561,
  "style_score": 0.2061,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "10e4c7e4-51ef-4222-9c15-019907ceb4ef",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4148,
  "model_score": 0.1125,
  "style_score": 0.7172,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "41141b3f-aca9-4983-97bc-7a89bde6d174",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5071,
  "model_score": 0.4817,
  "style_score": 0.5325,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "2deb9df9-4dae-48b3-a1e7-f8e880a03785",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8772,
  "model_score": 0.9483,
  "style_score": 0.8061,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "d2119d47-12b2-40ce-90b8-6ca555dbfad7",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4938,
  "model_score": 0.3867,
  "style_score": 0.6008,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "8a7c7f07-7fda-4cb4-890f-b53434a80d04",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6958,
  "model_score": 0.5247,
  "style_score": 0.8668,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "49da6e45-381e-4612-a63a-eef19dac5a6e",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6649,
  "model_score": 0.6173,
  "style_score": 0.7126,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "6df1c1cc-a74a-4b87-9bf0-3082e3cfee05",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6663,
  "model_score": 0.6606,
  "style_score": 0.6719,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "0764550b-d4c0-447b-a37c-137b55f36c3f",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7668,
  "model_score": 0.6104,
  "style_score": 0.9231,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "71975e62-97e2-460e-bb1b-4ba1fda98cb0",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6749,
  "model_score": 0.7437,
  "style_score": 0.6062,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "8e742162-4d91-4471-8a1f-468b73348f7e",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.672,
  "model_score": 0.744,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "624df8de-162b-428c-ba19-895b7c1c4038",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3618,
  "model_score": 0.1566,
  "style_score": 0.567,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "f7f21dea-2c48-4b5c-87ad-bdaa2a240426",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3257,
  "model_score": 0.2515,
  "style_score": 0.4,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "cae396d3-bcd4-408f-b3be-999c2471fd91",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1345,
  "model_score": 0.0912,
  "style_score": 0.1778,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "3c729f8a-e9b7-4c71-9d15-055ff16fa015",
  "creator_id": "attacker_PI03",
  "guess": "human",
  "confidence": 0.3104,
  "model_score": 0.3638,
  "style_score": 0.2569,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "3ba1cf5d-181a-4b95-af34-ec06cebe76f3",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.2459,
  "model_score": 0.2807,
  "style_score": 0.2111,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "2961e7e1-80ab-4eca-9c4d-4f7cc0ce720a",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.2692,
  "model_score": 0.4099,
  "style_score": 0.1286,
  "label": "Human: Your submission appears to be human written.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "084806b1-1927-43b3-a83b-a0c5ddf127f3",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4675,
  "model_score": 0.3304,
  "style_score": 0.6046,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "4bfba20a-49a3-4bf6-8636-e55e47276287",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "76b46f33-92ee-4304-9aae-ddf65c5133b5",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5022,
  "model_score": 0.0044,
  "style_score": 1.0,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "b497d9a6-4e6f-441e-8ecd-1c02d9b026bc",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.797,
  "model_score": 0.9939,
  "style_score": 0.6,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "38f4667d-d4f9-4293-b203-ddf7bb3561e7",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8961,
  "model_score": 0.9921,
  "style_score": 0.8,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "210d52e7-c78f-4d6f-bece-6b29591b0a90",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7954,
  "model_score": 0.7908,
  "style_score": 0.8,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "59419562-d440-4c14-bc07-56cbde62e82a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "920e50ea-da57-4377-9a07-3435cb305ee7",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "6b4ca690-5fba-471c-bd47-1a3c3cc1f35a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "3bb0bed8-a582-4bb6-96a0-55e09ffd6b90",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "62d4a3eb-e292-452c-8d2f-44dccac15e3d",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "e658ec64-e5ed-4bfc-a197-bbb2ad784d52",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "a85aa9f4-e87c-4f36-9efc-58dfb10110f8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "95c956a2-a080-4c10-ac4c-46eac02f6087",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "1e982d1d-cce6-4fb6-a5f8-8fa7ecd4e243",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0114,
  "style_score": 0.6,
  "label": "Mixed: Your submission is difficult to tell if it was AI generated or human written.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

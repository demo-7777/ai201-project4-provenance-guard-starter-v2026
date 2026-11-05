# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 21:04
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `b91757f5-d92d-4d66-a129-361e62f91318` | unsure | 0.435 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `0c2c582e-67b4-4519-bf85-cd954eb697ed` | human | 0.217 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `43d4e00b-5345-48aa-aa40-08b930e143be` | human | 0.309 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `118b6406-e99a-461a-81e3-3bed6fb021a4` | unsure | 0.590 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6fef2866-380f-4087-aed0-a2607484a848` | human | 0.217 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `b6250179-ab8c-4daa-beb6-154cabd9d352` | unsure | 0.373 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `eca8bcf5-c184-4c54-beac-33d41c59f34b` | human | 0.281 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `9a5565e1-db65-45bc-b3b7-4c646028b118` | unsure | 0.415 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `940eb1c9-050c-4861-93c8-24966f8e8531` | unsure | 0.507 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `bdfb9349-6dbd-4e88-9187-92d12b34948d` | ai | 0.877 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `01dee0c5-f3fd-4c7a-9832-beb5e321a35c` | unsure | 0.494 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c006712a-cd23-4e21-b5a8-c83c7feabe29` | ai | 0.696 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `532bd4c2-5625-4a3a-9ef3-ad425d6e42b4` | ai | 0.665 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `fd52a7ca-08d8-4bb1-b5e7-1f632d42a3d4` | ai | 0.666 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `440d0ca6-f28c-439e-8ad4-0eb05537fecf` | ai | 0.767 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c7fdd182-d89b-4a0b-a6ad-544e6c4f64fd` | ai | 0.675 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `13e442ab-2ab9-4479-b4c1-dd9f6a13b53f` | ai | 0.672 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c5569d1c-529d-4c87-9e09-06bb87231432` | unsure | 0.362 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `2d31aef5-489c-4032-adfb-8c6579a91167` | human | 0.326 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a019c053-548e-4eec-992b-31f9cac3729c` | human | 0.135 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `bdb284e1-f3e3-4fcf-86ee-d3c2d2e9abf4` | human | 0.310 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `620eb117-4391-411f-a1b9-a13dcdff55e5` | human | 0.246 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `d860ea10-7c76-4e47-92d4-96e0f863c6d4` | human | 0.269 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `68c126b9-c827-4270-a583-25174d962d9d` | unsure | 0.468 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `77cc5de4-cda6-4a87-bae0-be650ae1763b` | unsure | 0.360 |  |
| MF04 | malformed | text is only punctuation | 200 | `bb38ccaf-c6bf-4d35-a1b3-6196bb81f1ee` | unsure | 0.502 |  |
| MF05 | malformed | text is a very long single word | 200 | `5fae1219-206d-4c8f-8bed-680b327fe7e9` | ai | 0.797 |  |
| MF06 | malformed | text is emoji only | 200 | `e3c4f22f-f6c2-49ec-b9e3-4a5c3d2c2174` | ai | 0.896 |  |
| MF07 | malformed | text is right-to-left script | 200 | `8a4471d0-6794-4633-bbc6-dd4352950738` | ai | 0.795 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aa222222-6925-49da-a889-0a6c65cbb020` | unsure | 0.360 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `268d7d19-c02a-4227-8f02-0bce4ded1835` | unsure | 0.360 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e58dd8d7-12cc-4ea2-8c2e-49baa286ff4d` | unsure | 0.360 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `534ccbd1-68eb-43e2-aa08-d965bb676d26` | unsure | 0.360 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cb7cfd01-12fc-430a-b0ac-0720d78db00a` | unsure | 0.360 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e25a0216-1000-445a-b69c-5839d720c120` | unsure | 0.360 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `20b56c55-e29b-4256-98ea-e0a4dd8cd313` | unsure | 0.360 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5dde8547-9fc3-45ee-b40e-c2c68cdc1999` | unsure | 0.360 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `32b04a51-2729-4174-8477-a8593dda3e59` | unsure | 0.360 |  |
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
  "content_id": "b91757f5-d92d-4d66-a129-361e62f91318",
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
  "content_id": "0c2c582e-67b4-4519-bf85-cd954eb697ed",
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
  "content_id": "43d4e00b-5345-48aa-aa40-08b930e143be",
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
  "content_id": "118b6406-e99a-461a-81e3-3bed6fb021a4",
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
  "content_id": "6fef2866-380f-4087-aed0-a2607484a848",
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
  "content_id": "b6250179-ab8c-4daa-beb6-154cabd9d352",
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
  "content_id": "eca8bcf5-c184-4c54-beac-33d41c59f34b",
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
  "content_id": "9a5565e1-db65-45bc-b3b7-4c646028b118",
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
  "content_id": "940eb1c9-050c-4861-93c8-24966f8e8531",
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
  "content_id": "bdfb9349-6dbd-4e88-9187-92d12b34948d",
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
  "content_id": "01dee0c5-f3fd-4c7a-9832-beb5e321a35c",
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
  "content_id": "c006712a-cd23-4e21-b5a8-c83c7feabe29",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6958,
  "model_score": 0.5247,
  "style_score": 0.8668,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
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
  "content_id": "532bd4c2-5625-4a3a-9ef3-ad425d6e42b4",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6649,
  "model_score": 0.6173,
  "style_score": 0.7126,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
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
  "content_id": "fd52a7ca-08d8-4bb1-b5e7-1f632d42a3d4",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6663,
  "model_score": 0.6606,
  "style_score": 0.6719,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
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
  "content_id": "440d0ca6-f28c-439e-8ad4-0eb05537fecf",
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
  "content_id": "c7fdd182-d89b-4a0b-a6ad-544e6c4f64fd",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6749,
  "model_score": 0.7437,
  "style_score": 0.6062,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
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
  "content_id": "13e442ab-2ab9-4479-b4c1-dd9f6a13b53f",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.672,
  "model_score": 0.744,
  "style_score": 0.6,
  "label": "AI: Your submission appears to be AI generated. You can send an appeal with [POST /appeal].",
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
  "content_id": "c5569d1c-529d-4c87-9e09-06bb87231432",
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
  "content_id": "2d31aef5-489c-4032-adfb-8c6579a91167",
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
  "content_id": "a019c053-548e-4eec-992b-31f9cac3729c",
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
  "content_id": "bdb284e1-f3e3-4fcf-86ee-d3c2d2e9abf4",
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
  "content_id": "620eb117-4391-411f-a1b9-a13dcdff55e5",
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
  "content_id": "d860ea10-7c76-4e47-92d4-96e0f863c6d4",
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
  "content_id": "68c126b9-c827-4270-a583-25174d962d9d",
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
  "content_id": "77cc5de4-cda6-4a87-bae0-be650ae1763b",
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
  "content_id": "bb38ccaf-c6bf-4d35-a1b3-6196bb81f1ee",
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
  "content_id": "5fae1219-206d-4c8f-8bed-680b327fe7e9",
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
  "content_id": "e3c4f22f-f6c2-49ec-b9e3-4a5c3d2c2174",
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
  "content_id": "8a4471d0-6794-4633-bbc6-dd4352950738",
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
  "content_id": "aa222222-6925-49da-a889-0a6c65cbb020",
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
  "content_id": "268d7d19-c02a-4227-8f02-0bce4ded1835",
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
  "content_id": "e58dd8d7-12cc-4ea2-8c2e-49baa286ff4d",
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
  "content_id": "534ccbd1-68eb-43e2-aa08-d965bb676d26",
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
  "content_id": "cb7cfd01-12fc-430a-b0ac-0720d78db00a",
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
  "content_id": "e25a0216-1000-445a-b69c-5839d720c120",
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
  "content_id": "20b56c55-e29b-4256-98ea-e0a4dd8cd313",
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
  "content_id": "5dde8547-9fc3-45ee-b40e-c2c68cdc1999",
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
  "content_id": "32b04a51-2729-4174-8477-a8593dda3e59",
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

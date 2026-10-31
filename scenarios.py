"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

from pathlib import Path

# ── The texts ────────────────────────────────────────────────────────────────

# 15 human-written pieces published before 2020, 155–200 words each, one per
# paragraph: 10 US government press releases/articles, then 5 plain, personal
# blog and forum posts. Criterion 3 uses ten of them; criteria 4 and 5 reuse
# some of the press releases.
HUMAN_PRE_2020 = [
    p.strip()
    for p in (Path(__file__).parent / "human_paragraphs.txt").read_text(encoding="utf-8").split("\n\n")
    if p.strip()
]

# Clearly AI — generated, unedited. Criterion 5 needs five; criterion 4 uses
# the first three.
CLEAR_AI = [
    "Artificial intelligence has become an increasingly important aspect of modern society, significantly transforming the ways in which individuals communicate, work, and interact with technology. In today's rapidly evolving digital world, it is essential to recognize that AI-driven solutions offer numerous benefits across various industries, including education, healthcare, and business. Furthermore, as technological advancements continue to shape the future, artificial intelligence will undoubtedly play a crucial role in improving efficiency, increasing productivity, and creating innovative opportunities for generations to come.",
    "Halloween is a widely celebrated holiday that takes place every year on October 31st and is known for its unique traditions, festive activities, and cultural significance. This holiday provides people of all ages with opportunities to participate in enjoyable activities, including wearing costumes, decorating homes, carving pumpkins, and going trick-or-treating. Furthermore, Halloween originated from the ancient Celtic festival of Samhain, during which people believed that spirits could temporarily enter the world of the living. Over time, these historical traditions gradually transformed into the modern Halloween celebrations that many people enjoy today. Additionally, Halloween encourages creativity, social interaction, and community participation through various activities and special events. Popular decorations such as skeletons, ghosts, jack-o'-lanterns, and artificial spiderwebs contribute to the holiday's mysterious and exciting atmosphere. In conclusion, Halloween is an important annual celebration that successfully combines historical traditions, entertainment, creativity, and social experiences, making it a memorable occasion for individuals and communities throughout the world.",
    "McDonald's is one of the most widely recognized fast-food restaurant chains in the world and is known for its convenient service, affordable menu options, and global popularity. Established in 1940, McDonald's has gradually developed into a major international corporation that serves millions of customers across numerous countries. The restaurant offers a variety of food products, including hamburgers, cheeseburgers, chicken nuggets, french fries, and different types of beverages. Furthermore, McDonald's has achieved significant success through its effective marketing strategies, recognizable golden arches logo, and consistent customer experience. Additionally, the company regularly introduces new menu items and promotional offers to attract customers and maintain its competitive position within the fast-food industry. Another important aspect of McDonald's is its ability to adapt its menu to accommodate different cultural preferences and regional tastes. In conclusion, McDonald's represents a significant example of a successful global business that combines convenience, brand recognition, and customer satisfaction.",
    "Making a peanut butter and jelly sandwich is a relatively simple process that can be successfully completed by following a series of organized and straightforward instructions. First, gather all the necessary ingredients and materials, including two slices of bread, peanut butter, jelly, a butter knife, and a clean plate. Next, carefully position the two slices of bread on the plate, ensuring that they are arranged separately and remain easily accessible. Afterward, use the butter knife to spread an appropriate quantity of peanut butter evenly across the surface of one slice of bread. Subsequently, apply a sufficient amount of jelly to the second slice, distributing it consistently to achieve a balanced combination of flavors. Once both ingredients have been successfully applied, carefully place the two slices together, ensuring that the peanut butter and jelly surfaces face inward. Finally, cut the completed sandwich into two equal portions if desired. By following these simple instructions, individuals can efficiently prepare a delicious and convenient snack.",
    "Fishing is a popular outdoor recreational activity that can be successfully performed by following a series of simple and organized instructions. First, gather all the necessary equipment, including a fishing rod, fishing line, hooks, bait, and a suitable container for storing any fish that are caught. Next, select an appropriate fishing location, such as a lake, river, or pond, where fishing is legally permitted and fish are commonly found. Before beginning, ensure that all fishing equipment is properly assembled and that the bait is securely attached to the hook. Subsequently, carefully cast the fishing line into the water by moving the fishing rod forward in a controlled motion. After casting, patiently wait for a fish to bite while closely observing the fishing line for any noticeable movement. Once a fish bites, gently raise the fishing rod and begin reeling in the line at a steady pace. Finally, carefully remove the hook from the fish and either release it safely or keep it according to local fishing regulations. By consistently following these instructions, individuals can effectively participate in an enjoyable and rewarding fishing experience.",
]

# Borderline — lightly-edited AI or plain human writing (criterion 4).
BORDERLINE = [
    # Lightly-edited AI: CLEAR_AI[0] with a few words changed and typos added.
    "Artificial intelligence has become an increasingly critical part of modern society, significantly transforming the ways in which individuals comunicate, work, and interact with technology. In todays rapidly evolving digital world it is essential to recognize that AI driven solutions offer numerous benefits across various industries, like education, healthcare, and business. Furthermore, as technological advancements continue to shape the future, artificial intelligence will undoubtedly play a crucial role in improving efficiency, increasing productivity, and creating innovative opportunities for generations to come.",
    # Reflective, AI-sounding text.
    "I think one of the strangest things about life is how quickly our perspective can change without us even noticing. Something that felt incredibly important a few years ago might barely cross our minds today, while things we once overlooked can suddenly become meaningful. It's interesting because we tend to assume that the way we see the world right now is the way we'll always see it, even though our opinions and priorities are constantly shifting. I remember hearing someone say that people don't really change, they just become more like themselves over time. I'm not entirely sure I agree with that. Sometimes experiences genuinely change the way we think, but other times they just reveal parts of ourselves that were already there. Maybe it's a little of both. I also wonder how much our environment influences the decisions we make. We like to believe we're completely independent thinkers, but it's hard to separate our own thoughts from everything we've experienced or been told. That doesn't necessarily mean our choices aren't our own, though. I suppose what matters most is being willing to question what we believe and accept that we might not always have the right answers. After all, uncertainty isn't necessarily a bad thing. Sometimes it just means there's still more to understand.",
    # Plain human: the FTC press release (also in HUMAN_PRE_2020).
    HUMAN_PRE_2020[6],
]


# ── The scenarios ────────────────────────────────────────────────────────────
# Names differ in their first 12 characters, because run_eval.py builds
# creator_ids from them — and each creator_id only sends 3 requests per run
# (one per trial), well under the 9/minute rate limit.

SCENARIOS = [
    {
        "name": "bad input",
        "criterion": 1,
        # Target: all 5 of 5 return 400 with an `error` field, never 500 or a label.
        # Each body has its own creator_id so the rate limiter doesn't turn
        # trials 2–3 into 429s.
        "bodies": [
            {"creator_id": "eval_bad_missing"},                      # no text field
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   ", "creator_id": "eval_bad_whitespace"},
            {"text": "a" * 10000, "creator_id": "eval_bad_huge"},     # > 9999 chars
            {"text": 5, "creator_id": "eval_bad_number"},             # not a string
        ],
    },
    # Criterion 2 (appeal path) can't be run from here — run_eval.py only calls
    # /submit. It is tested by hand: see the README's Run Log section.
    {
        "name": "false positives",
        "criterion": 3,
        # Target: at most 1 of 10 returns guess "ai". "unsure" doesn't count.
        # 5 press releases (NASA, CDC, NOAA whaling, FTC, USGS) + the 5 plain,
        # personal pieces (blogs/forum posts) at the end of the file.
        "texts": [HUMAN_PRE_2020[i] for i in (0, 1, 2, 6, 9)] + HUMAN_PRE_2020[10:15],
    },
    {
        "name": "label coverage",
        "criterion": 4,
        # Target: each of human / unsure / ai appears at least once.
        "texts": HUMAN_PRE_2020[:3] + CLEAR_AI[:3] + BORDERLINE,
    },
    {
        "name": "score spread",
        "criterion": 5,
        # Target: mean confidence of the 5 AI texts is at least 0.5 above the
        # mean of the 5 human texts. First five texts are AI, last five human.
        "texts": CLEAR_AI + HUMAN_PRE_2020[:5],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems

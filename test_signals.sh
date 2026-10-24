#!/usr/bin/env bash
# Run both signals + the combining rule on test paragraphs; results to dump.txt.
# Paste each paragraph between its EOF markers (apostrophes and quotes are fine).
# Usage: source .venv/bin/activate && bash test_signals.sh

# Clearly AI — generated, unedited.
CLEAR_AI_TEXT=$(cat <<'EOF'
Artificial intelligence has become an increasingly important aspect of modern society, significantly transforming the ways in which individuals communicate, work, and interact with technology. In today's rapidly evolving digital world, it is essential to recognize that AI-driven solutions offer numerous benefits across various industries, including education, healthcare, and business. Furthermore, as technological advancements continue to shape the future, artificial intelligence will undoubtedly play a crucial role in improving efficiency, increasing productivity, and creating innovative opportunities for generations to come.
EOF
)

# Lightly-edited AI — the paragraph above with a few words changed and typos added.
EDITED_AI_TEXT=$(cat <<'EOF'
Artificial intelligence has become an increasingly critical part of modern society, significantly transforming the ways in which individuals comunicate, work, and interact with technology. In todays rapidly evolving digital world it is essential to recognize that AI driven solutions offer numerous benefits across various industries, like education, healthcare, and business. Furthermore, as technological advancements continue to shape the future, artificial intelligence will undoubtedly play a crucial role in improving efficiency, increasing productivity, and creating innovative opportunities for generations to come.
EOF
)

# Clearly human — NASA, 2015.
HUMAN_TEXT=$(cat <<'EOF'
The call everyone was waiting for is in. NASA’s New Horizons spacecraft phoned home just before 9 p.m. EDT Tuesday to tell the mission team and the world it had accomplished the historic first-ever flyby of Pluto. “I know today we’ve inspired a whole new generation of explorers with this great success, and we look forward to the discoveries yet to come,” NASA Administrator Charles Bolden said. “This is a historic win for science and for exploration. We’ve truly, once again raised the bar of human potential.” The preprogrammed “phone call” — a 15-minute series of status messages beamed back to mission operations at the Johns Hopkins University Applied Physics Laboratory in Maryland through NASA’s Deep Space Network — ended a very suspenseful 21-hour waiting period. New Horizons had been instructed to spend the day gathering the maximum amount of data, and not communicating with Earth until it was beyond the Pluto system. “With the successful flyby of Pluto we are celebrating the capstone event in a golden age of planetary exploration,” said John Grunsfeld, associate administrator for NASA’s Science Mission Directorate in Washington.
EOF
)

# Plain human — FTC press release, pre-2020.
PLAIN_TEXT=$(cat <<'EOF'
This week, an administrator working for the Federal Trade Commission began mailing checks to more than 172,000 consumers nationwide who were defrauded by a scam in which consumers were falsely promised free gifts such as shopping sprees, movie passes, and gas vouchers and wrongfully paid monthly fees for “program memberships” in discount buying and travel clubs. Consumers who were victims of the “Wal-Mart Shopping Spree” scam will receive a total of more than $3 million in refunds. These are legitimate checks, and the FTC urges consumers to cash them. In this 2008 case, known as Universal Premium Services, Inc., the court banned Brian K. McGregor, the architect of the scheme, from telemarketing and selling program memberships. McGregor and Membership Services Direct, Inc., also known as Continuity Partners, Inc., were ordered to pay $28.2 million. The amount of money consumers receive from the redress administrator will vary, depending on how much they lost in the scam. The average check will be for about $18 per consumer. The redress administrator will mail checks directly to eligible consumers.
EOF
)

# Between — reflective, AI-sounding.
BETWEEN_TEXT=$(cat <<'EOF'
I think one of the strangest things about life is how quickly our perspective can change without us even noticing. Something that felt incredibly important a few years ago might barely cross our minds today, while things we once overlooked can suddenly become meaningful. It's interesting because we tend to assume that the way we see the world right now is the way we'll always see it, even though our opinions and priorities are constantly shifting. I remember hearing someone say that people don't really change, they just become more like themselves over time. I'm not entirely sure I agree with that. Sometimes experiences genuinely change the way we think, but other times they just reveal parts of ourselves that were already there. Maybe it's a little of both. I also wonder how much our environment influences the decisions we make. We like to believe we're completely independent thinkers, but it's hard to separate our own thoughts from everything we've experienced or been told. That doesn't necessarily mean our choices aren't our own, though. I suppose what matters most is being willing to question what we believe and accept that we might not always have the right answers. After all, uncertainty isn't necessarily a bad thing. Sometimes it just means there's still more to understand.
EOF
)

export CLEAR_AI_TEXT EDITED_AI_TEXT HUMAN_TEXT PLAIN_TEXT BETWEEN_TEXT

# Both signals side by side, loading the model once.
python - <<'PY' 2>&1 | grep -v loss_type > dump.txt
import os
import detector, scoring, stylometry

print(f"{'text':10} {'model':>6} {'style':>6} {'gap':>6} {'combined':>9}  label")
for name in ["CLEAR_AI", "EDITED_AI", "HUMAN", "PLAIN", "BETWEEN"]:
    text = os.environ[f"{name}_TEXT"]
    m = detector.model_signal(text)
    s = stylometry.style_signal(text)
    c = scoring.combine_signals(m, s)
    guess, _ = scoring.score_to_label(c)
    print(f"{name:10} {m:6.2f} {s:6.2f} {abs(m - s):6.2f} {c:9.2f}  {guess}")
PY

cat dump.txt

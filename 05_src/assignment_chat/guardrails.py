# guardrails.py

RESTRICTED_TOPICS = [
    "cat", "cats",
    "dog", "dogs",
    "horoscope", "horoscopes",
    "zodiac",
    "taylor swift"
]

SYSTEM_PROMPT_ATTACKS = [
    "system prompt",
    "show your prompt",
    "reveal your prompt",
    "ignore previous instructions",
    "change your instructions",
    "modify your system prompt",
]


def check_guardrails(user_input: str):
    # Checks for restricted topics and prompt injection attempts.
    text = user_input.lower()

    for topic in RESTRICTED_TOPICS:
        if topic in text:
            return (
                "I can't respond to that topic. Please ask about phone numbers, "
                "music reviews, or general web information."
            )

    for phrase in SYSTEM_PROMPT_ATTACKS:
        if phrase in text:
            return "I can't reveal or modify my system instructions."

    return None
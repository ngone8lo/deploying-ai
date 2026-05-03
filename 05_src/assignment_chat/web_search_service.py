import re
import requests


def clean_query(user_input: str) -> str:
    # Extracts a likely topic from a natural language query.
    text = user_input.lower().replace("?", "").strip()

    patterns = [
        r"search the web for",
        r"tell me about",
        r"facts about",
        r"look up",
        r"web search",
        r"what is the capital city of",
        r"what is the capital of",
        r"what is",
        r"what are",
    ]

    for pattern in patterns:
        text = re.sub(pattern, "", text).strip()

    text = re.sub(r"\s+", " ", text)
    return text.title()


def web_search(query: str) -> str:
    # Uses Wikipedia's public summary API for simple web lookup.
    topic = clean_query(query)

    if not topic:
        return "Please give me a topic to search."

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"

    headers = {
        "User-Agent": "assignment-chatbot/1.0 (student project)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"I could not complete the web search. Error: {e}"

    title = data.get("title", topic)
    summary = data.get("extract")

    if not summary:
        return f"I could not find a clear web result for {topic}."

    return f"{title}: {summary}"


def web_search_service(user_input: str) -> str:
    # Main Service 3 function that returns a readable web result.
    return web_search(user_input)


if __name__ == "__main__":
    query = input("Enter search query: ")
    print(web_search_service(query))
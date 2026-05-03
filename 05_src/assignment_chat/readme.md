# Assignment 2: Boussole Chatbot

## Contents
- [Summary](#summary)
- [Services](#services)
- [Service 1: API Calls](#service-1-api-calls)
- [Service 2: Semantic Query](#service-2-semantic-query)
- [Service 3: Web Search](#service-3-web-search)
- [User Interface](#user-interface)
- [Guardrails and Other Limitations](#guardrails-and-other-limitations)
- [Implementation](#implementation)
- [Setup Instructions](#setup-instructions)
- [Example Usage](#example-usage)
- [Summary](#summary)

## Summary
The goal of this assignment is to design and implement an AI system with a conversational interface.

This implementation builds a modular chatbot called **Boussole**, which integrates multiple services into a single conversational system. The chatbot allows users to validate phone numbers, search music reviews using semantic search, and retrieve general information through web search.

The system was developed incrementally, starting with simple service implementations and then integrating them into a unified chat interface. Each service is implemented independently and connected through routing logic in the main application.

---

## Services

This implementation is based on a simple service-based architecture. Each service is implemented as a separate Python module and imported into the main application (`app.py`).

### Service 1: API Calls

Service 1 uses the **Numverify API** to validate global phone numbers.

- The user can input a phone number in natural language (e.g., “Check this number +14165551234”).
- The system extracts the phone number and sends a request to the Numverify API.
- The API response is transformed into a natural-language summary instead of being returned as raw JSON.

The response includes:
- whether the number is valid
- associated country and location
- carrier and line type

This service demonstrates API integration and transformation of structured data into readable output.

---

### Service 2: Semantic Query

Service 2 implements semantic search using the **Pitchfork dataset** from the course labs.

- The dataset is loaded from a JSONL file
- Review text is embedded and stored in a persistent **ChromaDB collection**
- The system retrieves relevant review excerpts based on semantic similarity

When a user asks a question such as:

> “Find reviews about experimental indie rock”

The system:
- embeds the query
- retrieves the most relevant documents
- returns them as readable excerpts

This service demonstrates vector database usage and semantic retrieval.

---

### Service 3: Web Search

Service 3 performs simple web search using the **Wikipedia Summary API**.

- User queries are cleaned and converted into a topic
- The system retrieves a summary from Wikipedia
- The result is returned as a short, readable answer

Example queries:
- “Tell me about Brazil”
- “what is the capital city of Senegal?”

This satisfies the assignment requirement for a web search tool without using agent-based search.

---

## User Interface

The chatbot is implemented using **Gradio**.

Features:
- conversational chat interface
- automatic routing to services
- short-term memory using chat history
- clear responses depending on service type

The main application (`app.py`) handles:
- user input
- routing logic
- integration of all services


The chatbot maintains short-term conversational memory using the Gradio chat history.

The chatbot has a defined personality called “Boussole,” which translates to compass in French, a friendly and concise assistant that guides users through phone validation, music search, and web queries in a clear and helpful tone.

---

## Guardrails and Other Limitations

Guardrails are implemented in a separate file (`guardrails.py`).

The system prevents:
- access to system prompts
- modification of system instructions
- responses to restricted topics:
  - cats or dogs
  - horoscopes or zodiac signs
  - Taylor Swift

If a restricted query is detected, the chatbot returns a safe fallback response.

---


## Implementation

Project Files:
```
05_src/assignment_chat/
├── app.py
├── api_service.py
├── build_pitchfork_db.py
├── chroma_db/
├── semantic_service.py
├── web_search_service.py
├── guardrails.py
├── readme.md
├── .env   (not committed)

```



---

## Setup Instructions

### Install dependencies
```
pip install gradio chromadb requests python-dotenv
```

#### API Key Setup
To use this service, you need a Numverify API key:

1. Go to https://numverify.com and create a free account.
2. After signing in, navigate to your dashboard.
3. Copy your API key.
4. Create a `.env` file: NUMVERIFY_API_KEY=your_key_here

### Build semantic search database
```
python build_pitchfork_db.py
```

### Run application
```
python app.py
```

---

## Example Usage

- `Check this number +221775546723`
- `Find Pitchfork reviews about experimental indie rock`
- `Tell me about Canada`
- `What is the capital city of Brazil?`

---

## Summary

This chatbot integrates three different service types:
- API-based lookup (Numverify)
- semantic search (Pitchfork dataset + ChromaDB)
- web search (Wikipedia API)

The system demonstrates how multiple AI services can be combined into a single conversational interface while maintaining modular design and clear separation of responsibilities.
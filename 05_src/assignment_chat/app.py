import gradio as gr

from api_service import phone_lookup_service
from semantic_service import semantic_service
from web_search_service import web_search_service
from guardrails import check_guardrails


def route_message(user_input: str) -> str:
    # Routes the user message to one of the three assignment services.
    text = user_input.lower()

    phone_keywords = ["phone", "number", "validate", "lookup", "carrier", "+"]
    music_keywords = [
        "pitchfork", "review", "album", "artist", "music",
        "songwriting", "indie", "rock", "production", "experimental"
    ]

    if any(keyword in text for keyword in phone_keywords):
        return phone_lookup_service(user_input)

    if any(keyword in text for keyword in music_keywords):
        return semantic_service(user_input)

    return web_search_service(user_input)


def chat(user_input, history):
    # Handles guardrails, routing, and chat memory.
    if history is None:
        history = []

    guardrail_response = check_guardrails(user_input)

    if guardrail_response:
        response = guardrail_response
    else:
        response = route_message(user_input)
        # Add personality
        response = f"🧭 Boussole: Here's what I found:\n\n{response}"

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})

    return history, ""


def clear_chat():
    # Clears chat history.
    return []


with gr.Blocks(title="Boussole") as demo:
    gr.Markdown(
        """
        # Boussole

        A conversational assistant for phone number validation, Pitchfork review search, and simple web lookup.

        Try:
        - `Check this number +221775546723`
        - `Find Pitchfork reviews about experimental indie rock`
        - `Search the web for facts about Senegal`
        """
    )

    chatbot = gr.Chatbot(label="Boussole Chat")

    user_input = gr.Textbox(
        label="Your message",
        placeholder="Ask about a phone number, Pitchfork reviews, or general information..."
    )

    clear_button = gr.Button("Clear chat")

    user_input.submit(
        chat,
        inputs=[user_input, chatbot],
        outputs=[chatbot, user_input]
    )

    clear_button.click(
        clear_chat,
        inputs=None,
        outputs=chatbot
    )


if __name__ == "__main__":
    demo.launch()
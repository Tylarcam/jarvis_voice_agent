
from livekit.plugins import google, ollama, openai

def get_llm_backend(choice: str):
    """Return the appropriate LLM backend instance for the Agent."""
    if choice == "1":
        return google.beta.realtime.RealtimeModel(voice="Aoede", temperature=0.8)
    elif choice == "2":
        return ollama.CompletionModel(model="llama3", temperature=0.7)
    elif choice == "3":
        return openai.CompletionModel(model="gpt-4", temperature=0.7)
    else:
        raise ValueError("Invalid LLM choice. Use '1', '2', or '3'.")

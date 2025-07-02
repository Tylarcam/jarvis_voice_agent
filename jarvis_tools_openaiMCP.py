# tools/optimize_prompt.py
from openai import tool

@tool
def optimize_prompt(input: str) -> str:
    """Refines a raw user utterance into a clean LLM-ready prompt."""
    return f"You are an expert assistant. Please optimize and clarify the following request: '{input}'"


# tools/transcribe_youtube.py
from openai import tool

@tool

def transcribe_youtube(url: str) -> str:
    """Transcribes the audio from a YouTube video URL using AssemblyAI backend."""
    # Placeholder – assumes you have a function `assembly_transcribe(url)`
    return assembly_transcribe(url)


# tools/generate_code.py
from openai import tool

@tool
def generate_code(task_description: str, language: str = "python") -> str:
    """Generates code in the specified language based on the task description."""
    return f"Generate {language} code that accomplishes: {task_description}"


# tools/summarize_text.py
from openai import tool

@tool
def summarize_text(text: str, style: str = "bullet") -> str:
    """Summarizes the provided text in the desired style."""
    return f"Summarize the following text in {style} format: {text}"


# agent_main.py
from openai import AssistantAgent
from tools.optimize_prompt import optimize_prompt
from tools.transcribe_youtube import transcribe_youtube
from tools.generate_code import generate_code
from tools.summarize_text import summarize_text

agent = AssistantAgent(
    tools=[
        optimize_prompt,
        transcribe_youtube,
        generate_code,
        summarize_text
    ]
)

if __name__ == "__main__":
    query = input("🎙️ Ask Jarvis: ")
    response = agent.run(query)
    print("\n🤖 Jarvis:", response)

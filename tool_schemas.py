import assemblyai as aai
import os

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "1214db4c0cc549e7bb3171b2d96d3865")

def transcribe_local_audio(filepath):
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(filepath, config=config)
    if hasattr(transcript, 'utterances'):
        return "\n".join([f"{utt.speaker}: {utt.text}" for utt in transcript.utterances])
    else:
        return transcript.text if hasattr(transcript, 'text') else "[No transcript available]"

gemini_tool_schemas = [
    {
        "name": "optimize_prompt",
        "description": "Refine user input into a clean LLM-ready prompt.",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "User's raw natural language request."}
            },
            "required": ["input"]
        }
    },
    {
        "name": "transcribe_youtube",
        "description": "Transcribe YouTube audio via backend (e.g., AssemblyAI).",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "YouTube video URL."}
            },
            "required": ["url"]
        }
    },
    {
        "name": "transcribe_local_audio",
        "description": "Transcribe a local audio file using AssemblyAI.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to the audio file."}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "generate_code",
        "description": "Generate code in a specified language for a given task.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_description": {"type": "string"},
                "language": {"type": "string", "default": "python"}
            },
            "required": ["task_description"]
        }
    },
    {
        "name": "summarize_text",
        "description": "Summarize input text in a given format.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "style": {"type": "string", "default": "bullet"}
            },
            "required": ["text"]
        }
    }
]

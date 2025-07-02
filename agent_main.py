
from livekit import agents
from livekit.agents import AgentSession, RoomInputOptions
from livekit.plugins import noise_cancellation
from agent import Assistant
from modules.llm_selector import get_llm_backend
from prompts import SESSION_INSTRUCTION

def prompt_user_for_llm():
    print("\nSelect which model Jarvis should use:")
    print("1. Gemini (Google)")
    print("2. Ollama 3.2 (local)")
    print("3. OpenAI (GPT-4/3.5)")
    return input("Enter number: ").strip()

async def entrypoint(ctx: agents.JobContext):
    choice = prompt_user_for_llm()
    llm_backend = get_llm_backend(choice)
    agent = Assistant(llm_backend)

    session = AgentSession()
    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    await ctx.connect()
    await session.generate_reply(instructions=SESSION_INSTRUCTION)

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

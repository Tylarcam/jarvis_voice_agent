from livekit import agents
from livekit.agents import AgentSession, RoomInputOptions
from livekit.plugins import noise_cancellation, google
from agent import Assistant
from prompts import SESSION_INSTRUCTION

async def entrypoint(ctx: agents.JobContext):
    llm_backend = google.beta.realtime.RealtimeModel(voice="Aoede", temperature=0.8)
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
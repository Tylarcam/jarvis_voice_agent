
from livekit.agents import Agent
from prompts import AGENT_INSTRUCTION
from tools import get_weather, search_web, send_email, open_directory

class Assistant(Agent):
    def __init__(self, llm_backend) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=llm_backend,
            tools=[
                get_weather,
                search_web,
                send_email,
                open_directory,
            ],
        )

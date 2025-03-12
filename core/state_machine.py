import time
from enum import Enum
from .api_client import XNETAPIClient
from .rag_engine import RagEngine
from .command_handler import TerminalCommandHandler
from utils.config import CONFIG
from utils.logger import logger

class State(Enum):
    UNAUTHENTICATED = "unauthenticated"
    AUTHENTICATED = "authenticated"
    SESSION_ENDED = "session_ended"

class XNETStateMachine:
    def __init__(self, api_client: XNETAPIClient, rag_engine: RagEngine):
        self.State = State  # For CommandHandler to access
        self.CONFIG = CONFIG  # For CommandHandler to access
        self.state = State.UNAUTHENTICATED
        self.api_client = api_client
        self.rag_engine = rag_engine
        self.command_handler = TerminalCommandHandler(self)
        self.token_expiry = 0
        self.last_interaction = time.time()
        self.credentials = None

    def process(self, user_input: str) -> str:
        self.last_interaction = time.time()
        
        if self.state == State.AUTHENTICATED and time.time() > self.token_expiry:
            if time.time() - self.last_interaction < CONFIG["REFRESH_WINDOW"]:
                if self.credentials and self.api_client.login(*self.credentials):
                    self.token_expiry = time.time() + CONFIG["TERMINAL_TIMEOUT"]
                    logger.info("Token refreshed silently")
                else:
                    self.state = State.UNAUTHENTICATED
                    return "Session expired. Please log in again."
            else:
                self.state = State.UNAUTHENTICATED
                return "Session expired due to inactivity. Please log in again."

        if self.state == State.SESSION_ENDED:
            return "Session has ended. Start a new session with /login."

        return self.command_handler.process(user_input)

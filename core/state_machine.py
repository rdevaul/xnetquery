import time
from enum import Enum
from .api_client import XNETAPIClient
from .rag_engine import RagEngine
from utils.config import CONFIG
from utils.logger import logger

class State(Enum):
    UNAUTHENTICATED = "unauthenticated"
    AUTHENTICATED = "authenticated"
    SESSION_ENDED = "session_ended"

class XNETStateMachine:
    def __init__(self, api_client: XNETAPIClient, rag_engine: RagEngine):
        self.state = State.UNAUTHENTICATED
        self.api_client = api_client
        self.rag_engine = rag_engine
        self.token_expiry = 0
        self.last_interaction = time.time()
        self.credentials = None

    def process(self, user_input: str) -> str:
        self.last_interaction = time.time()
        
        if self.state == State.UNAUTHENTICATED:
            if user_input.lower().startswith("login"):
                try:
                    email, password = user_input.split()[1], user_input.split()[2]
                    if self.api_client.login(email, password):
                        self.state = State.AUTHENTICATED
                        self.token_expiry = time.time() + CONFIG["TERMINAL_TIMEOUT"]
                        self.credentials = (email, password)
                        return "Logged in successfully!"
                    return "Login failed. Check your credentials."
                except IndexError:
                    return "Please provide email and password: login <email> <password>"
            return self.rag_engine.answer(user_input)

        elif self.state == State.AUTHENTICATED:
            if user_input.lower() == "end session":
                self.state = State.SESSION_ENDED
                self.api_client.token = None
                self.credentials = None
                return "Session ended."
            
            if time.time() > self.token_expiry:
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

            if "venues" in user_input.lower():
                data = self.api_client.get_venues()
                return f"Venues: {data}" if "error" not in data else data["error"]
            elif "devices" in user_input.lower():
                data = self.api_client.get_devices()
                return f"Devices: {data}" if "error" not in data else data["error"]
            return self.rag_engine.answer(user_input)

        elif self.state == State.SESSION_ENDED:
            return "Session has ended. Start a new session with 'login'."

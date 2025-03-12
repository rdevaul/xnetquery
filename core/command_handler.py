from abc import ABC, abstractmethod
from typing import Dict, Callable, List
import json
import time
from utils.logger import logger

class CommandHandler(ABC):
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.commands: Dict[str, Callable[[List[str]], str]] = {}
        self.register_base_commands()

    def register_base_commands(self):
        self.commands["/help"] = self.help_command
        self.commands["/login"] = self.login_command
        self.commands["/logout"] = self.logout_command

    def register_command(self, command: str, handler: Callable[[List[str]], str]):
        self.commands[command] = handler

    def process(self, user_input: str) -> str:
        if not user_input.startswith("/"):
            return self.state_machine.rag_engine.answer(user_input)
        
        parts = user_input.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        handler = self.commands.get(command)
        if handler:
            return handler(args)
        return "Unknown command. Type /help for assistance."

    def help_command(self, args: List[str]) -> str:
        base_help = (
            "Available commands:\n"
            "/help - Show this help message\n"
            "/login <email> <password> - Authenticate with the XNET API\n"
            "/logout - End the current session\n"
        )
        return base_help

    def login_command(self, args: List[str]) -> str:
        if len(args) != 2:
            return "Usage: /login <email> <password>"
        email, password = args
        if self.state_machine.api_client.login(email, password):
            self.state_machine.state = self.state_machine.State.AUTHENTICATED
            self.state_machine.token_expiry = time.time() + self.state_machine.CONFIG["TERMINAL_TIMEOUT"]
            self.state_machine.credentials = (email, password)
            return "Logged in successfully!"
        return "Login failed. Check your credentials."

    def logout_command(self, args: List[str]) -> str:
        self.state_machine.state = self.state_machine.State.SESSION_ENDED
        self.state_machine.api_client.token = None
        self.state_machine.credentials = None
        return "Session ended."

class TerminalCommandHandler(CommandHandler):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.register_api_commands()

    def register_api_commands(self):
        self.register_command("/get", self.get_command)

    def get_command(self, args: List[str]) -> str:
        if not self.state_machine.state == self.state_machine.State.AUTHENTICATED:
            return "Please log in first with /login <email> <password>"

        if not args:
            return "Usage: /get <endpoint> [args] (e.g., /get venues, /get venue <id>)"

        endpoint = args[0].lower()
        sub_args = args[1:] if len(args) > 1 else []

        if endpoint == "venues":
            return self.get_venues(sub_args)
        elif endpoint == "venue":
            return self.get_venue(sub_args)
        return "Supported /get endpoints: venues, venue <id>"

    def get_venues(self, args: List[str]) -> str:
        filter_obj = {"name": args[0]} if args else {}
        try:
            data = self.state_machine.api_client.get_venues(filter_obj)
            if "error" in data:
                return f"Error: {data['error']}"
            if not data:
                return "No venues found."
            summary = "\n".join(
                f"{v['name']} (ID: {v['id']}) - {v.get('address', 'No address')}"
                for v in data
            )
            return f"Venues:\n{summary}"
        except Exception as e:
            logger.error(f"Error fetching venues: {e}")
            return "Failed to retrieve venues."

    def get_venue(self, args: List[str]) -> str:
        if not args:
            return "Usage: /get venue <id>"
        venue_id = args[0]
        try:
            # Assuming /venues/{id} endpoint exists per Swagger
            data = self.state_machine.api_client.get_venue(venue_id)
            if "error" in data:
                return f"Error: {data['error']}"
            return json.dumps(data, indent=2)
        except Exception as e:
            logger.error(f"Error fetching venue {venue_id}: {e}")
            return f"Failed to retrieve venue {venue_id}."

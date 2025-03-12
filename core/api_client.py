import requests
from utils.config import CONFIG
from utils.logger import logger

class XNETAPIClient:
    def __init__(self):
        self.base_url = CONFIG["API_BASE_URL"]
        self.token = None
        self.headers = {}

    def login(self, email: str, password: str) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False

    def get_venues(self) -> dict:
        return self._get("/venues")

    def get_devices(self) -> dict:
        return self._get("/devices")

    def _get(self, endpoint: str) -> dict:
        try:
            response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API GET {endpoint} failed: {e}")
            return {"error": str(e)}

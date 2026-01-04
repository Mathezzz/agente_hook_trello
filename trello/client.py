import requests
import logging
from config import TRELLO_API_KEY, TRELLO_TOKEN

class TrelloClient:
    def __init__(self):
        if not TRELLO_API_KEY or not TRELLO_TOKEN:
            raise RuntimeError("Credenciais do Trello não configuradas no .env")

        self.base_url = "https://api.trello.com/1"
        self.auth = {
            "key": TRELLO_API_KEY,
            "token": TRELLO_TOKEN
        }

    def get_cards_from_list(self, list_id: str):
        url = f"{self.base_url}/lists/{list_id}/cards"
        logging.info(f"Buscando cards da lista {list_id}")

        response = requests.get(url, params=self.auth, timeout=30)
        response.raise_for_status()
        return response.json()

    def add_comment(self, card_id: str, text: str):
        url = f"{self.base_url}/cards/{card_id}/actions/comments"
        params = {**self.auth, "text": text}

        logging.info(f"Adicionando comentário no card {card_id}")
        response = requests.post(url, params=params, timeout=30)
        response.raise_for_status()

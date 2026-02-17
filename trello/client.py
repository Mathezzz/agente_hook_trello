import requests
import logging
from config import TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_LIST_ID

class TrelloClient:
    def __init__(self):
        if not TRELLO_API_KEY or not TRELLO_TOKEN:
            raise RuntimeError("Credenciais do Trello não configuradas no .env")

        self.base_url = "https://api.trello.com/1"
        self.auth = {
            "key": TRELLO_API_KEY,
            "token": TRELLO_TOKEN
        }
        self.list_id = TRELLO_LIST_ID

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

    def move_card_to_list(self, card_id: str, list_id: str):
        url = f"{self.base_url}/cards/{card_id}"
        params = {**self.auth, "idList": list_id}

        logging.info(f"Movendo card {card_id} para lista {list_id}")
        response = requests.put(url, params=params, timeout=30)
        response.raise_for_status()

    def register_webhook(self, callback_url: str):
        """Registra um webhook para novos cards adicionados à lista"""
        url = f"{self.base_url}/webhooks/"
        params = {
            **self.auth,
            "callbackURL": callback_url,
            "idModel": self.list_id,
            "description": "Webhook para novos cards"
        }

        logging.info(f"Registrando webhook para lista {self.list_id}")
        response = requests.post(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_webhooks(self):
        """Lista todos os webhooks registrados"""
        url = f"{self.base_url}/webhooks"
        
        logging.info("Listando webhooks")
        response = requests.get(url, params=self.auth, timeout=30)
        response.raise_for_status()
        return response.json()

    def delete_webhook(self, webhook_id: str):
        """Deleta um webhook registrado"""
        url = f"{self.base_url}/webhooks/{webhook_id}"
        
        logging.info(f"Deletando webhook {webhook_id}")
        response = requests.delete(url, params=self.auth, timeout=30)
        response.raise_for_status()


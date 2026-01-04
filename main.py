import logging
from logs.logger import setup_logger
from trello.client import TrelloClient
from trello.parser import parse_card
from config import TRELLO_LIST_ID

TEST_COMMENT = """
🤖 Revisão automática (teste)

Este é um comentário de teste da V1 do AI Backlog Reviewer.
Nenhuma ação foi tomada neste ticket.
"""

def main():
    logging.info("Iniciando AI Backlog Reviewer - Pacote 2")

    if not TRELLO_LIST_ID:
        raise RuntimeError("TRELLO_LIST_ID não configurado no .env")

    trello = TrelloClient()
    cards = trello.get_cards_from_list(TRELLO_LIST_ID)

    logging.info(f"{len(cards)} cards encontrados")

    for card in cards:
        parsed = parse_card(card)
        trello.add_comment(parsed["id"], TEST_COMMENT)
        logging.info(f"Comentário adicionado no card: {parsed['name']}")

if __name__ == "__main__":
    setup_logger()
    main()

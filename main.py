import logging
from logs.logger import setup_logger

from trello.client import TrelloClient
from trello.parser import parse_card
from docs.loader import load_docs
from agent.llm_client import get_llm_client
from agent.reviewer import analyze_ticket

from config import TRELLO_LIST_ID, TRELLO_NEXT_LIST_ID

COMMENT_PREFIX = "🤖 Revisão automática de backlog\n\n"

def main():
    logging.info("Iniciando AI Backlog Reviewer - V1")

    if not TRELLO_LIST_ID or not TRELLO_NEXT_LIST_ID:
        raise RuntimeError("IDs de listas do Trello não configurados")

    trello = TrelloClient()
    llm_client = get_llm_client()
    boas_praticas = load_docs()

    cards = trello.get_cards_from_list(TRELLO_LIST_ID)
    logging.info(f"{len(cards)} cards encontrados")

    for card in cards:
        parsed = parse_card(card)

        try:
            comment_body = analyze_ticket(
                llm_client,
                parsed,
                boas_praticas
            )

            full_comment = COMMENT_PREFIX + comment_body

            trello.add_comment(parsed["id"], full_comment)
            trello.move_card_to_list(parsed["id"], TRELLO_NEXT_LIST_ID)

            logging.info(f"Card processado com sucesso: {parsed['name']}")

        except Exception as e:
            logging.error(f"Erro ao processar card {parsed['name']}: {e}")

if __name__ == "__main__":
    setup_logger()
    main()

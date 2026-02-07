import logging
import requests
from flask import Flask, request, jsonify
from logs.logger import setup_logger
from trello.client import TrelloClient
from trello.parser import parse_card
from agent.llm_client import get_llm_client
from agent.reviewer import analyze_ticket

from config import TRELLO_NEXT_LIST_ID, WEBHOOK_PORT, WEBHOOK_URL

COMMENT_PREFIX = "🤖 Revisão automática de backlog\n\n"

app = Flask(__name__)
trello_client = None
llm_client = None
boas_praticas = None

def process_card(card_id: str):
    """Processa um card e adiciona comentário + move para próxima lista"""
    try:
        # Busca dados do card
        url = f"{trello_client.base_url}/cards/{card_id}"
        response = requests.get(url, params=trello_client.auth, timeout=30)
        response.raise_for_status()
        card = response.json()

        parsed = parse_card(card)

        comment_body = analyze_ticket(
            llm_client,
            parsed
        )

        full_comment = COMMENT_PREFIX + comment_body

        trello_client.add_comment(parsed["id"], full_comment)
        trello_client.move_card_to_list(parsed["id"], TRELLO_NEXT_LIST_ID)

        logging.info(f"Card processado com sucesso: {parsed['name']}")

    except Exception as e:
        logging.error(f"Erro ao processar card {card_id}: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    """Endpoint que recebe eventos do webhook do Trello"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"status": "ok"}), 200

        logging.info(f"Webhook recebido: {data}")

        # Verifica se é o evento "addCardToList"
        action = data.get("action", {})
        action_type = action.get("type")

        if action_type == "addCardToList":
            card_id = action.get("data", {}).get("card", {}).get("id")
            if card_id:
                process_card(card_id)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        logging.error(f"Erro ao processar webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Endpoint para verificar se o servidor está rodando"""
    return jsonify({"status": "ok"}), 200

def main():
    global trello_client, llm_client, boas_praticas
    
    logging.info("Iniciando AI Backlog Reviewer - Webhook Mode")

    if not TRELLO_NEXT_LIST_ID:
        raise RuntimeError("ID da próxima lista do Trello não configurado")

    if not WEBHOOK_URL:
        raise RuntimeError("WEBHOOK_URL não configurada")

    trello_client = TrelloClient()
    llm_client = get_llm_client()
    boas_praticas = load_docs()

    # Registra o webhook
    try:
        webhook_response = trello_client.register_webhook(WEBHOOK_URL)
        logging.info(f"Webhook registrado com sucesso: {webhook_response}")
    except Exception as e:
        logging.error(f"Erro ao registrar webhook: {e}")
        raise

    # Inicia o servidor Flask
    logging.info(f"Iniciando servidor webhook na porta {WEBHOOK_PORT}")
    app.run(host="0.0.0.0", port=WEBHOOK_PORT, debug=False)

if __name__ == "__main__":
    setup_logger()
    main()

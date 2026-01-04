def parse_card(card: dict) -> dict:
    """
    Normaliza o card do Trello para o formato interno da aplicação.
    """
    return {
        "id": card.get("id"),
        "name": card.get("name"),
        "desc": card.get("desc"),
        "url": card.get("shortUrl"),
        "list_id": card.get("idList")
    }

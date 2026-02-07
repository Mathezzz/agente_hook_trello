from agent.prompt import BASE_PROMPT
from config import LLM_MODEL


def analyze_ticket(llm_client, ticket: dict) -> str:
    user_content = f"""
TICKET:
Título: {ticket['name']}
Descrição:
{ticket.get('desc', 'Sem descrição')}
"""

    response = llm_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

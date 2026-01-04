from pathlib import Path
import logging

DOCS_DIR = Path("docs")

def load_docs() -> str:
    """
    Carrega todos os arquivos .md da pasta docs
    e retorna um único contexto concatenado.
    """
    contents = []

    if not DOCS_DIR.exists():
        logging.warning("Diretório docs/ não encontrado.")
        return ""

    md_files = sorted(DOCS_DIR.glob("*.md"))

    if not md_files:
        logging.warning("Nenhum arquivo .md encontrado em docs/")
        return ""

    for file in md_files:
        try:
            logging.info(f"Carregando documentação: {file.name}")
            text = file.read_text(encoding="utf-8")
            contents.append(f"\n\n### Fonte: {file.name}\n{text}")
        except Exception as e:
            logging.error(f"Erro ao ler {file.name}: {e}")

    return "\n".join(contents)

from taxxq.logger import logger

def query_chain(retriever, llm, prompt, user_input: str):
    try:
        pass
    except Exception:
        logger.exception("Error on query chain")
        raise
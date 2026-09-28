from taxxq.logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result = chain.invoke(user_input)
        response = {
            "response": result.content
        }
        logger.debug(f"Chain response: {response}")
        return response
    except Exception:
        logger.exception("Error on query chain")
        raise
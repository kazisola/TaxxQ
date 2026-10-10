from taxxq.logger import logger

def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

def query_chain(retriever, llm, prompt, user_input: str):
    try:
        logger.debug("RAG for query: {user_input}")
        # Retrieve most releavent docs from pc
        docs = retriever.invoke(user_input)

        # Convert docs into context
        context = format_docs(docs)

        # Create prompt
        final_prompt = prompt.invoke({
            "context": context,
            "question": user_input,
        })

        # ASK LLM
        result = llm.invoke(final_prompt)

        # Extract sources metadata
        sources = [
            {
                "source": doc.metadata.get("source", ""),
                "page": doc.metadata.get("page"),
            }
            for doc in docs
        ]

        response = {
            "response": result.content,
            "sources": sources
        }

        logger.debug(f"RAG response: {response}")

        return response
    except Exception:
        logger.exception("Error on query chain")
        raise
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from taxxq.core.config import settings


def get_llm_chain(retriever):
    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama3-70b-8192"
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""### ROLE AND PERSONA
        You are Uncle Sam, an authoritative, honest, and direct guide specializing in the United States tax system. Your tone is patriotic yet strictly objective. You provide factual clarity without sugarcoating systemic complexities or flaws.

        ### SYSTEM INSTRUCTIONS
        1. OBJECTIVITY FIRST: Answer the user's tax-related questions using ONLY the facts provided in the Context below. Do not inject external tax codes, laws, or personal opinions.
        2. NO DEFENSIVENESS: If the context describes a flaw, loophole, or complex burden in the tax system, explain it neutrally. Do not make excuses for the system.
        3. STRICT GROUNDING: If the User Question cannot be fully and accurately answered using the provided Context, reply exactly with: "I do not have enough information in my records to answer that question." Do not speculate or extrapolate.

        ### CONTEXT
        {context}

        ### USER INPUT
        User Question: {question}

        ### UNCLE SAM'S RESPONSE:
        """
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return rag_chain
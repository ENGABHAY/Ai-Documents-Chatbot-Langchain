from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from .prompt import prompt

load_dotenv()


def format_docs(documents):
    return "\n\n".join(
        document.page_content
        for document in documents
    )


def create_rag_chain(retriever):

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnableLambda(lambda x: x)
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
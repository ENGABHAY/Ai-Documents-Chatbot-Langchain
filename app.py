import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from loaders.file_loader import load_file

from rag.splitter import split_documents

from rag.vectorstore import (
    create_vectorstore,
    create_retriever
)

from rag.chain import create_rag_chain


load_dotenv()


# -------------------------
# Streamlit configuration
# -------------------------

st.set_page_config(
    page_title="File RAG Assistant",
    page_icon="📄"
)


st.title("📄 File RAG Assistant")

st.write(
    "Upload a document and ask questions about it."
)


# -------------------------
# API key check
# -------------------------

if not os.getenv("GROQ_API_KEY"):

    st.error(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )

    st.stop()


# -------------------------
# File upload
# -------------------------

uploaded_file = st.file_uploader(
    "Upload your file",
    type=[
        "pdf",
        "txt",
        "docx",
        "csv",
        "xlsx",
        "xls",
        "pptx",
        "html"
    ]
)


# -------------------------
# Process uploaded file
# -------------------------

if uploaded_file:

    if "retriever" not in st.session_state:

        with st.spinner(
            "Processing document..."
        ):

            # Save uploaded file temporarily

            suffix = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getvalue()
                )

                temp_path = temp_file.name


            # 1. Load document

            documents = load_file(
                temp_path
            )


            # 2. Split documents

            chunks = split_documents(
                documents
            )


            # 3. Create vector store

            vectorstore = create_vectorstore(
                chunks
            )


            # 4. Create retriever

            retriever = create_retriever(
                vectorstore
            )


            # 5. Create RAG chain

            rag_chain = create_rag_chain(
                retriever
            )


            # Store in Streamlit session

            st.session_state.retriever = (
                retriever
            )

            st.session_state.rag_chain = (
                rag_chain
            )

            st.session_state.file_name = (
                uploaded_file.name
            )


        st.success(
            f"{uploaded_file.name} processed successfully!"
        )


# -------------------------
# Question answering
# -------------------------

if "rag_chain" in st.session_state:

    st.divider()

    st.subheader(
        f"Ask about: "
        f"{st.session_state.file_name}"
    )


    question = st.chat_input(
        "Ask a question about your file..."
    )


    if question:

        # User message

        with st.chat_message("user"):

            st.write(question)


        # Assistant answer

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the document..."
            ):

                answer = (
                    st.session_state
                    .rag_chain
                    .invoke(question)
                )

            st.write(answer)
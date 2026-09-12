from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template("""
You are a document question-answering assistant.

Answer the question ONLY using the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not make up information.
3. If the answer is not present in the context, say:
   "I could not find the answer in the uploaded file."

Context:
{context}

Question:
{question}

Answer:
""")
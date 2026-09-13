from loaders.file_loader import load_file

from rag.chain import create_rag_chain

from rag.vectorstore import create_vectorstore, create_retriever

from rag.splitter import split_documents



file_path = r"D:\VS code\Rag using langchain\data\uploads\NIPS-2017-attention-is-all-you-need-Paper.pdf"

query = "What is self-attention?"


file = load_file(file_path=file_path)

print("added file")

splits = split_documents(file)

print("chunked doc")

db = create_vectorstore(splits)

print("stored in vector db")

retrival = create_retriever(db)

print("retrieval created")

docs = retrival.invoke(query)

for i , doc in enumerate(docs,start=1):
    print(f"\n{'='*70}")
    print(f"RETRIEVED CHUNK {i}")
    print(f"{'='*70}")
    print(doc.page_content)
    print("Metadata:", doc.metadata)
    
chain = create_rag_chain(retrival)

print("chain created")




answer = chain.invoke(query)



print("\nANSWER:")

print(answer)
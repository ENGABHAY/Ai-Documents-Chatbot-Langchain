import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from loaders.file_loader import load_file

from loaders.file_loader import load_file

documents = load_file(
    r"D:\VS code\Rag using langchain\data\uploads\Section_2_Transpose_Pivot_Unpivot.xlsx"
)

print("Number of documents:", len(documents))

print("\nFirst document:")
print(documents[0].page_content[:1000])

print("\nMetadata:")
print(documents[0].metadata)
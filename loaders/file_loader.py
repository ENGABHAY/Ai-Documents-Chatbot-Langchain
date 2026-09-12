from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    CSVLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
)

from .excel_loader import load_excel


def load_file(file_path: str):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return PyPDFLoader(file_path).load()

    elif extension == ".txt":
        return TextLoader(
            file_path,
            encoding="utf-8"
        ).load()

    elif extension == ".docx":
        return Docx2txtLoader(file_path).load()

    elif extension == ".csv":
        return CSVLoader(file_path).load()

    elif extension in [".xlsx", ".xls"]:
        return load_excel(file_path)

    elif extension == ".pptx":
        return UnstructuredPowerPointLoader(file_path).load()

    elif extension in [".html", ".htm"]:
        return UnstructuredHTMLLoader(file_path).load()

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )
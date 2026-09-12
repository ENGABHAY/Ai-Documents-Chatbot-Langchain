import pandas as pd

from langchain_core.documents import Document


def load_excel(file_path: str):

    excel_file = pd.ExcelFile(file_path)

    documents = []

    for sheet_name in excel_file.sheet_names:

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name
        )

        text = df.to_string(index=False)

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path,
                    "sheet": sheet_name
                }
            )
        )

    return documents
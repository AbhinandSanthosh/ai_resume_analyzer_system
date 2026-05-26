from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_resume(file_path):

    text = ""

    try:

        if file_path.endswith(".pdf"):

            pdf = PdfReader(file_path)

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted


        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            for para in doc.paragraphs:

                text += para.text + "\n"


        return text.strip()


    except Exception as e:

        print("Resume parser error:", e)

        return ""
import fitz

def extract_text_from_pdf(file):

    file.seek(0)

    doc = fitz.open(stream=file.getvalue(), filetype="pdf")

    pages = []

    for page in doc:
        text = page.get_text()

        if text.strip():   # ignore empty pages
            pages.append(text)

    return pages
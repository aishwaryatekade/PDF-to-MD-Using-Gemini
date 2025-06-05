def main():
   import fitz
def extract_text(pdf path):
    documnet = fitz.open(pdf_path)
    all_text = ""
    for page in document:
    all_text += page.get_text()
    document.close()
    return all_text
     


if _name_ == '_main_':
    main()
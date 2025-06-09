import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                                             
from utils.file_handler import extract_text_from_pdf, save_to_markdown
from utils.gemini_client import summarize_with_gemini

def main():
    pdf_file_path = "path_to_pdf_file.pdf"
    print("Reading PDF file...")
    try:
        raw_text = extract_text_from_pdf(pdf_file_path)
    except Exception as e:
        print("Error extracting PDF:", e)
        return

    print("Summarizing using Gemini AI...")
    try:
        markdown_summary = summarize_with_gemini(raw_text)
        save_to_markdown(markdown_summary, "output.md")
    
        print("Markdown saved successfully!")
    except Exception as e:  
        print("Error summarizing:", e) 
if __name__ == "__main__":
    main()

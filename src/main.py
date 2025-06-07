import os
from utils.file_handler import extract_text_from_pdf , save_to_markdown
from utils.gemini_client import summarize_with_gemini

def main():
    # Path to the input PDF file
    pdf_file = "sample.pdf"

    # Step 1: Read the content from the PDF
    print("Reading PDF content...")
    try:
       raw_text = extract_text_from_pdf(pdf_file)
    except FileNotFoundError:
        print(f"Error: '{pdf_file}' not found.")
        return
    
    # Step 2: Send the text to Gemini and get the summarized content
    print("Summarizing using Gemini AI...")
    try:
        markdown_summary = summarize_with_gemini(raw_text)
    except Exception as e:
        print(f"Error during summarization: {e}")
        return
    
     # Step 3: Save the summary to a Markdown file
    output_path = "output/summary.md"
    print(f"Saving summary to '{output_path}'...")
    save_to_markdown(markdown_summary, output_path)

    print("✅ Summary saved successfully!")

    if __name__ == "__main__":
       main()




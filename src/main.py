import os
import fitz  # PyMuPDF
import requests

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("API Key:", GEMINI_API_KEY)  # You can remove this after confirming it's loading correctly

# ✅ Step 1: PDF se text extract karne wala function
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# ✅ Step 2: Text ko Gemini API pe bhejna
def send_text_to_gemini_api(extracted_text):
    api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"


    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [{"text": extracted_text}]
            }
        ]
    }
    response = requests.post(api_endpoint, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['candidates'][0]['content']['parts'][0]['text']

# ✅ Step 3: Text ko markdown me convert karna
def format_text_to_markdown(processed_text):
    return processed_text.replace('\n', '  \n')

# ✅ Step 4: Markdown file me likhna
def write_markdown_to_file(markdown_output, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(markdown_output)

# ✅ Step 5: Pura process execute karna
def execute_conversion(pdf_file):
    extracted_content = extract_text_from_pdf(pdf_file)
    summarized_text = send_text_to_gemini_api(extracted_content)
    markdown_format = format_text_to_markdown(summarized_text)
    markdown_file_path = os.path.splitext(pdf_file)[0] + '.md'
    write_markdown_to_file(markdown_format, markdown_file_path)
    print(f"✅ Markdown content saved to {markdown_file_path}")

# ✅ Run the program
if __name__ == "__main__":
    pdf_path = "../resumeat.pdf"  # ✅ correct relative path
    execute_conversion(pdf_path)



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

def send_text_to_gemini_api(content):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": content
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"{url}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]



# ✅ Step 3: Gemini se mila plain text ko Markdown format me convert karne ka function (basic placeholder)
def format_text_to_markdown(text):
    # You can improve this later; for now, return as-is
    return text

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
    import sys

    if len(sys.argv) < 2:
        print("❌ Please provide the PDF filename as an argument.")
        print("✅ Example: python main.py resumeat.pdf")
        sys.exit(1)

    relative_pdf_path = sys.argv[1]

    # Make path absolute based on project root
    pdf_path = os.path.abspath(relative_pdf_path)




    print("📄 Full path:", pdf_path)
    execute_conversion(pdf_path)

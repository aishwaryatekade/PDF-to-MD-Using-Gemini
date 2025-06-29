from dotenv import load_dotenv
load_dotenv()

import os
import fitz  # PyMuPDF
import textwrap
import google.generativeai as genai


# --- Load Gemini API Key Securely ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "❌ Gemini API key not found. Please set the 'GEMINI_API_KEY' environment variable."
    )

# --- Configure Gemini API ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    raise RuntimeError(f"❌ Failed to configure Gemini API: {e}")


# --- PDF Text Extraction ---
def extract_text_from_pdf(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF file not found: {pdf_path}")

    try:
        with fitz.open(pdf_path) as doc:
            return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        raise RuntimeError(f"❌ Error reading PDF '{pdf_path}': {e}")


# --- Gemini Text Processing ---
def process_text_with_gemini(text: str) -> str:
    if not text.strip():
        return ""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = textwrap.dedent(f"""
        Summarize the following document and format it into clean, readable Markdown.
        Use proper sections, headings, lists, emphasis, and structure.

        --- Document Start ---
        {text}
        --- Document End ---
        """)

        print("📤 Sending content to Gemini API...")
        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()
        else:
            raise ValueError("⚠️ No content returned by Gemini API.")

    except Exception as e:
        raise RuntimeError(f"❌ Gemini API processing failed: {e}")


# --- Conversion Orchestrator ---
def convert_pdf_to_markdown(pdf_path: str, output_dir: str = ".") -> str:
    os.makedirs(output_dir, exist_ok=True)

    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(output_dir, f"{file_name}.md")

    try:
        print(f"📄 Processing PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)

        if not text.strip():
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("<!-- No text found in PDF. -->\n")
            print("⚠️ PDF contained no text. Markdown file saved with a note.")
            return output_path

        markdown = process_text_with_gemini(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"✅ Conversion successful. File saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return ""


# --- CLI Entry Point ---
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Convert PDF to Markdown using Gemini AI.")
    parser.add_argument("pdf_file", nargs="?", default="Lstm.pdf", help="Path to the input PDF file.")

    parser.add_argument("-o", "--output_dir", default=".", help="Directory to save the output Markdown file.")

    args = parser.parse_args()

    output = convert_pdf_to_markdown(args.pdf_file, args.output_dir)

    if output:
        print(f"🎉 Done! Markdown saved at: {output}")
    else:
        print("❌ Failed to convert PDF.")
        

        
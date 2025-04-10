import pdfplumber
import requests
from bs4 import BeautifulSoup
import re
import warnings

def extract_text_from_pdf(file_path):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="pdfplumber")
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                text = re.sub(r'%PDF-\d\.\d.*?(stream|endstream).*?(obj|endobj)', '', text, flags=re.DOTALL)
                text = re.sub(r'\s+', ' ', text).strip()
                return text if text else "No readable text extracted."
        except Exception as e:
            return f"Error extracting text: {e}"

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        abstract = soup.find("meta", {"name": "description"}) or soup.find("div", {"class": "abstract"})
        text = abstract.get("content") if abstract and "content" in abstract.attrs else abstract.get_text() if abstract else soup.get_text()
        text = re.sub(r'\s+', ' ', text).strip()
        return text if text else "No abstract available."
    except Exception as e:
        return f"Error fetching URL: {e}"

def resolve_doi(doi):
    url = f"https://doi.org/{doi}"
    return fetch_url_content(url)

def extract_introduction(text):
    intro_start = text.lower().find("introduction")
    if intro_start != -1:
        intro_end = text.find("\n\n", intro_start)
        if intro_end == -1:
            intro_end = len(text)
        return text[intro_start:intro_end].strip()
    return text[:2000]

def generate_citation(paper):
    title = paper.get('title', 'Untitled')
    url = paper.get('url', 'No URL')
    return f"{title}. Source: {url}"
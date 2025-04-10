import arxiv
from core.utils import extract_text_from_pdf, fetch_url_content, resolve_doi
import re

class SearchAgent:
    def __init__(self):
        self.results = []

    def search_papers(self, query, max_results=5, sort_by='recency'):
        sort_criterion = arxiv.SortCriterion.SubmittedDate if sort_by == 'recency' else arxiv.SortCriterion.Relevance
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion,
            sort_order=arxiv.SortOrder.Descending
        )
        self.results = []
        for paper in search.results():
            abstract = paper.summary if paper.summary else "No abstract available."
            abstract = re.sub(r'[^\x20-\x7E\n]', ' ', abstract)
            abstract = re.sub(r'\s+', ' ', abstract).strip()
            self.results.append({
                'title': paper.title,
                'url': paper.pdf_url,
                'content': abstract,
                'citation': f"{paper.title}. Source: {paper.pdf_url}"
            })
        return self.results

    def process_upload(self, file_path):
        text = extract_text_from_pdf(file_path)
        return {
            'title': file_path.split('/')[-1],
            'url': file_path,
            'content': text,
            'citation': f"{file_path.split('/')[-1]}. Source: Local file {file_path}"
        }

    def process_url(self, url):
        content = fetch_url_content(url)
        return {
            'title': url.split('/')[-1] or "URL Paper",
            'url': url,
            'content': content,
            'citation': f"URL Paper. Source: {url}"
        }

    def process_doi(self, doi):
        content = resolve_doi(doi)
        return {
            'title': doi,
            'url': f"https://doi.org/{doi}",
            'content': content,
            'citation': f"DOI Paper {doi}. Source: https://doi.org/{doi}"
        }
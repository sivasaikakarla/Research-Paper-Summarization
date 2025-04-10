class ProcessingAgent:
    def process(self, paper_data):
        content = paper_data['content']
        title = paper_data['title']
        citation = paper_data['citation']
        return {'title': title, 'processed_content': content.strip(), 'citation': citation}
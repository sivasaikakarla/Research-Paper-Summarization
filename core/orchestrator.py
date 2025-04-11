from agents.search_agent import SearchAgent
from agents.processing_agent import ProcessingAgent
from agents.classification_agent import ClassificationAgent
from agents.summary_agent import SummaryAgent
from agents.synthesis_agent import SynthesisAgent
from agents.audio_agent import AudioAgent
from core.utils import extract_introduction
# 
class Orchestrator:
    def __init__(self, topics):
        self.search_agent = SearchAgent()
        self.processing_agent = ProcessingAgent()
        self.classification_agent = ClassificationAgent(topics)
        self.summary_agent = SummaryAgent()
        self.synthesis_agent = SynthesisAgent()
        self.audio_agent = AudioAgent()
        self.topics = topics

    def run(self, query=None, file_path=None, url=None, doi=None, sort_by='recency'):
        papers = []
        if query:
            papers.extend(self.search_agent.search_papers(query, sort_by=sort_by))
        if file_path:
            papers.append(self.search_agent.process_upload(file_path))
        if url:
            papers.append(self.search_agent.process_url(url))
        if doi:
            papers.append(self.search_agent.process_doi(doi))

        processed_papers = []
        for paper in papers:
            content = paper.get('content', '')
            if file_path and paper['title'] == file_path.split('/')[-1]:
                intro = extract_introduction(content)
            else:
                intro = content  
            processed = self.processing_agent.process(paper)
            topic = self.classification_agent.classify(processed['processed_content'])
            processed['topic'] = topic
            processed_papers.append(processed)

        summaries_by_topic = {}
        for paper in processed_papers:
            summary = self.summary_agent.summarize(paper['processed_content'])
            summary_with_citation = f"{summary}\n\nCitation: {paper['citation']}"
            topic = paper['topic']
            if topic not in summaries_by_topic:
                summaries_by_topic[topic] = []
            summaries_by_topic[topic].append(summary_with_citation)

        outputs = {}
        for topic, summaries in summaries_by_topic.items():
            for i, summary in enumerate(summaries, 1):
                with open(f"outputs/summaries/{topic}_paper_{i}.txt", "w", encoding="utf-8") as f:
                    f.write(summary)
                audio_path = f"outputs/podcasts/{topic}_paper_{i}.mp3"
                self.audio_agent.generate_podcast(summary, audio_path)
            synthesis = self.synthesis_agent.synthesize([s.split('\n\nCitation:')[0] for s in summaries], topic)
            synthesis_with_citation = f"{synthesis}\n\nCitations:\n" + "\n".join([s.split('\n\nCitation:')[1] for s in summaries])
            with open(f"outputs/summaries/{topic}_synthesis.txt", "w", encoding="utf-8") as f:
                f.write(synthesis_with_citation)
            audio_path = f"outputs/podcasts/{topic}_synthesis.mp3"
            self.audio_agent.generate_podcast(synthesis_with_citation, audio_path)
            outputs[topic] = {'summaries': summaries, 'synthesis': synthesis_with_citation}

        return outputs
from core.orchestrator import Orchestrator
import os

def main():
    topics = ["AI", "Physics", "Biology"]
    orchestrator = Orchestrator(topics)
    os.makedirs("outputs/summaries", exist_ok=True)
    os.makedirs("outputs/podcasts", exist_ok=True)
    outputs = orchestrator.run(
        query="machine learning and ai",
        file_path="sample_papers/sample2.pdf",
        url="https://www.sciencedirect.com/science/article/pii/S1364032120307024",  
        doi="https://doi.org/10.1007/s10462-024-10862-8",        
        sort_by="relevance"                 
    )
    print("Processing complete. Check 'outputs' directory for summaries and podcasts.")

if __name__ == "__main__":
    main()


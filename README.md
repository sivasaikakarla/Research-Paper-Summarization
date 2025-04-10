# Research Paper Summarizer

This project is a multi-agent system that searches, processes, summarizes, classifies, and synthesizes research papers from open-access sources, generating audio podcasts for summaries and syntheses. It supports queries, file uploads, URLs, and DOIs, with topic classification and citation tracking.

---

## Features

- Search for open-access research papers from arXiv.
- Process papers from local PDFs, URLs, and DOIs.
- Classify papers into user-defined topics (e.g., "AI", "Physics", "Biology").
- Generate summaries and cross-paper topic syntheses.
- Convert summaries and syntheses into audio podcasts (MP3).
- Include citations for traceability.

---

## Setup Instructions

### Prerequisites

- Python: 3.8 or higher  
- Docker: Latest version (optional, for containerized setup)  
- Internet: Required for initial model downloads and audio generation
- Hardware: At least 8GB RAM (for local models)  

---

### Local Installation

#### Clone the Repository:

```bash
git clone https://github.com/sivasaikakarla/Research-Paper-Summarization.git
cd research-summarizer
```

#### Install Dependencies:

```bash
pip3 install -r requirements.txt
```

#### Download Models:

**Summarization Model (`bart-large-cnn`):**

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
model_name = "facebook/bart-large-cnn"
save_dir = "./models/bart-large-cnn"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Model saved to {save_dir}")
```

**Classification Model (`bart-large-mnli`):**

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model_name = "facebook/bart-large-mnli"
save_dir = "./models/bart-large-mnli"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Model saved to {save_dir}")
```

#### Run the System:

Place a sample PDF (e.g., `sample1.pdf`) in `sample_papers/`.  
Execute:

```bash
python main.py
```

Outputs appear in `outputs/summaries/` (text) and `outputs/podcasts/` (MP3s).

---

## Docker Setup

### Build the Docker Image:

Ensure Docker is installed and running.  
Create a Dockerfile in the project root:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libsndfile1

# Pre-download models
RUN python3 -c "from transformers import AutoModelForSeq2SeqLM, AutoTokenizer;   model = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large-cnn');   tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn');   model.save_pretrained('./models/bart-large-cnn');   tokenizer.save_pretrained('./models/bart-large-cnn')"
RUN python3 -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer;   model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli');   tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli');   model.save_pretrained('./models/bart-large-mnli');   tokenizer.save_pretrained('./models/bart-large-mnli')"

CMD ["python3", "main.py"]
```

### Build:

```bash
docker build -t research-summarizer .
```

### Run the Container:

**Without a PDF (query only):**

```bash
docker run research-summarizer
```

Outputs are saved to `outputs/` on your host machine.

**Notes:**

- Initial build downloads ~3GB of models; subsequent runs use cached versions.
- Ensure `sample_papers/` and `outputs/` directories exist on your host.

---

## System Architecture

The system is a modular, multi-agent pipeline:

- **Input Layer:** Accepts queries, PDFs, URLs, and DOIs via `main.py`.
- **Processing Layer:** Multi-agent system (`agents/`) handles tasks.
- **Output Layer:** Generates text files and MP3s in `outputs/`.
- **Core Coordination:** `orchestrator.py` manages agent interactions.

### Key components:

- **Models:** Local `bart-large-cnn` (summarization) and `bart-large-mnli` (classification).
- **Storage:** `./models/` for models, `outputs/` for results.

---

## Multi-Agent Design and Coordination

The system uses a multi-agent architecture with specialized agents coordinated by `Orchestrator`:

- **SearchAgent:**  
  Searches arXiv, processes uploads, URLs, and DOIs.  
  Returns metadata (title, content, citation).

- **ProcessingAgent:**  
  Cleans and prepares content.

- **ClassificationAgent:**  
  Classifies using `bart-large-mnli`.

- **SummaryAgent:**  
  Generates summaries.

- **SynthesisAgent:**  
  Combines summaries into syntheses.

- **AudioAgent:**  
  Converts text to MP3s using gTTS (online).

**Coordination:**  
Agents operate sequentially:  
`search → process → classify → summarize → synthesize → audio`.

---

## Paper Processing Methodology

- **Input Handling:**  
  - Query: arXiv abstracts.  
  - PDF: Text from `pdfplumber`.  
  - URL/DOI: Scraped with `requests` + `BeautifulSoup`.

- **Content Extraction:**  
  - PDFs: Intro or first 2000 characters.  
  - Online: Abstract.

- **Classification:**  
  - `bart-large-mnli` zero-shot classification (≤1000 chars).

- **Summarization:**  
  - `bart-large-cnn` chunked processing (~4000 chars).  
  - Target: 500 words (pads if needed).

- **Synthesis:**  
  - Topic-level overview of multiple summaries.

- **Citation:**  
  - Adds title + source to each output.

---

## Audio Generation Implementation

- **Primary:** gTTS converts text to MP3s via Google’s TTS.
- **Fallback:** pyttsx3 (offline) used if gTTS fails.

**Process:**

- Sanitizes text (ASCII only).
- Tries gTTS (3 attempts, 5s delay).
- Falls back to pyttsx3 if needed.
- MP3s saved in `outputs/podcasts/`.

---

## Limitations and Future Improvements

### Limitations

- gTTS requires internet; pyttsx3 has lower quality.
- Classification limited by `bart-large-mnli` and 1000-char input.
- Summaries may contain padding when input is short.
- `pdfplumber` fails on image-based PDFs.
- Local models are memory-heavy (~8GB RAM minimum).

### Future Improvements

- **Offline TTS:** Replace gTTS with local engine (e.g., Coqui TTS).
- **Fine-Tuned Classification:** Train `bart-large-mnli` on domain data.
- **OCR Support:** Add `pytesseract` for image PDFs.
- **Dynamic Summaries:** Adaptive length instead of fixed padding.
- **Parallelism:** Use multiprocessing for faster processing.

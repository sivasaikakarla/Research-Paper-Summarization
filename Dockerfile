FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*


COPY . .

RUN mkdir -p ./models/bart-large-cnn ./models/bart-large-mnli
RUN if [ ! -f ./models/bart-large-cnn/config.json ]; then \
    python -c "from transformers import AutoModelForSeq2SeqLM, AutoTokenizer; \
    model = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large-cnn'); \
    tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn'); \
    model.save_pretrained('./models/bart-large-cnn'); \
    tokenizer.save_pretrained('./models/bart-large-cnn')"; \
    fi
RUN if [ ! -f ./models/bart-large-mnli/config.json ]; then \
    python -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer; \
    model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli'); \
    tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli'); \
    model.save_pretrained('./models/bart-large-mnli'); \
    tokenizer.save_pretrained('./models/bart-large-mnli')"; \
    fi

CMD ["python", "main.py"]
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# model_name = "facebook/bart-large-cnn"
# save_dir = "./models/bart-large-cnn"

# # Download and save model and tokenizer
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model.save_pretrained(save_dir)
# tokenizer.save_pretrained(save_dir)

# print(f"Model saved to {save_dir}")


from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "facebook/bart-large-mnli"
save_dir = "./models/bart-large-mnli"

# Download and save model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)

print(f"Model saved to {save_dir}")
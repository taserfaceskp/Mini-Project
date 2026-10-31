import os
import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments

class PhishingDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def train_nlp():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(current_dir, '../../data/nlp/phishing_emails.csv'))

    if not os.path.exists(csv_path):
        print(f'Error: {csv_path} not found.')
        return

    print('Loading NLP Dataset...')
    df = pd.read_csv(csv_path)
    texts = df['text'].tolist()
    labels = df['label'].tolist()

    print('Tokenizing with DistilBERT...')
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)

    dataset = PhishingDataset(encodings, labels)
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=2,
        logging_steps=1,
        use_cpu=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    print('Starting NLP training...')
    trainer.train()
    print('NLP Training complete!')

if __name__ == '__main__':
    train_nlp()
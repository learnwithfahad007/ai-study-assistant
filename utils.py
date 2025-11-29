import nltk
from nltk.corpus import stopwords
import math
import re
import os
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

# Add project nltk_data to path
proj_nltk = os.path.join(os.path.dirname(__file__), '.venv', 'nltk_data')
if proj_nltk not in nltk.data.path:
    nltk.data.path.insert(0, proj_nltk)

STOP = set(stopwords.words('english'))

# Regex-based tokenizers (no punkt dependency)


def sent_tokenize(text):
    """Split text into sentences using regex."""
    return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]


def word_tokenize(text):
    """Split text into words using regex."""
    return re.findall(r'\b\w+\b', text.lower())


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def summarize_text(text, num_sentences=3):
    text = clean_text(text)
    sents = sent_tokenize(text)
    if len(sents) <= num_sentences:
        return text

    # build word frequencies
    freq = {}
    for sent in sents:
        for w in word_tokenize(sent.lower()):
            if w.isalpha() and w not in STOP:
                freq[w] = freq.get(w, 0) + 1

    # score sentences
    scores = []
    for i, sent in enumerate(sents):
        score = 0
        for w in word_tokenize(sent.lower()):
            if w.isalpha():
                score += freq.get(w, 0)
        scores.append((i, score))

    # pick top sentences
    top = sorted(scores, key=lambda x: x[1], reverse=True)[:num_sentences]
    top_idx = sorted([i for i, s in top])
    summary = ' '.join([sents[i] for i in top_idx])
    return summary


def generate_mcqs(text, num_q=5):
    # naive MCQ: pick sentences and mask a noun or keyword
    sents = sent_tokenize(text)
    mcqs = []
    for sent in sents[: num_q*3]:
        words = [w for w in word_tokenize(sent) if w.isalpha()]
        if len(words) < 4:
            continue

        # pick the longest word not a stopword
        candidates = [w for w in words if w.lower() not in STOP]
        if not candidates:
            continue
        answer = max(candidates, key=len)
        prompt = sent.replace(answer, '_____')
        options = [answer]

        # create distractors by mutating answer
        options += [answer[::-1], answer.capitalize() + 's',
                    answer[: max(1, len(answer)-1)]]
        mcqs.append({"question": prompt, "options": options, "answer": answer})
        if len(mcqs) >= num_q:
            break
    return mcqs


def make_flashcards(text, num=10):
    sents = sent_tokenize(text)
    flash = []
    for sent in sents[:num]:
        question = 'What is the main idea of: "' + \
            (sent[:60] + '...' if len(sent) > 60 else sent) + '"'
        answer = sent
        flash.append({"q": question, "a": answer})
    return flash


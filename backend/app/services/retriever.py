from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.knowledge_base import kb_documents

class KBRetriever:
    def __init__(self):
        self.docs = kb_documents()
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english"
        )
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in self.docs])

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        ranked = scores.argsort()[::-1][:top_k]

        results = []
        for idx in ranked:
            score = float(scores[idx])
            if score <= 0:
                continue
            item = dict(self.docs[idx])
            item["score"] = round(score, 4)
            results.append(item)
        return results

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Source:
    question: str
    subject: str
    score: float


@dataclass
class AnswerResult:
    answer: str
    subject: str
    confidence: float
    sources: List[Source]


class QAEngine:
    def __init__(self, dataset_path: str) -> None:
        self.dataset_path = dataset_path
        self.entries: List[Dict[str, str]] = self._load_dataset(dataset_path)
        self.size = len(self.entries)
        corpus = [self._normalize(e["question"] + " \n " + e.get("answer", "")) for e in self.entries]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(corpus)

    def _load_dataset(self, path: str) -> List[Dict[str, str]]:
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._default_dataset(), f, ensure_ascii=False, indent=2)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        # Ensure required keys
        cleaned: List[Dict[str, str]] = []
        for item in data:
            q = (item.get("question") or "").strip()
            a = (item.get("answer") or "").strip()
            s = (item.get("subject") or "General").strip() or "General"
            if q and a:
                cleaned.append({"question": q, "answer": a, "subject": s})
        return cleaned

    def _normalize(self, text: str) -> str:
        return " ".join(text.lower().split())

    def answer(self, question: str, subject: str = "General", top_k: int = 3) -> AnswerResult:
        query = self._normalize(question)
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()

        # Filter by subject with a small boost
        indices = list(range(len(self.entries)))
        scored: List[Tuple[int, float]] = []
        for i in indices:
            entry = self.entries[i]
            score = float(scores[i])
            if entry["subject"].lower() == subject.lower():
                score *= 1.08
            scored.append((i, score))

        scored.sort(key=lambda t: t[1], reverse=True)
        top = scored[: max(3, top_k)]

        sources: List[Source] = [
            Source(
                question=self.entries[i]["question"],
                subject=self.entries[i]["subject"],
                score=float(s),
            )
            for (i, s) in top
        ]

        best_idx, best_score = top[0]
        best_entry = self.entries[best_idx]
        answer_text = best_entry["answer"]

        # Calibrate a confidence from cosine similarity
        confidence = max(0.0, min(1.0, (best_score - 0.1) / 0.6))

        return AnswerResult(
            answer=answer_text,
            subject=best_entry["subject"],
            confidence=float(confidence),
            sources=sources,
        )

    def _default_dataset(self) -> List[Dict[str, str]]:
        return [
            {
                "subject": "Computer Science",
                "question": "Explain binary search",
                "answer": "Binary search finds a target in a sorted array by repeatedly halving the search space: compare middle, discard the half that cannot contain the target, and repeat. Time complexity is O(log n).",
            },
            {
                "subject": "Computer Science",
                "question": "What is time complexity?",
                "answer": "Time complexity estimates how an algorithm's running time grows with input size. Common classes include O(1), O(log n), O(n), O(n log n), and O(n^2).",
            },
            {
                "subject": "Mathematics",
                "question": "State the Pythagorean theorem",
                "answer": "In a right triangle with legs a and b and hypotenuse c, a^2 + b^2 = c^2.",
            },
            {
                "subject": "Physics",
                "question": "What is Newton's second law?",
                "answer": "Force equals mass times acceleration (F = m a). It describes how the velocity of an object changes when acted upon by a net force.",
            },
            {
                "subject": "English",
                "question": "What is a thesis statement?",
                "answer": "A thesis statement is a concise claim that expresses the main point of an essay, guiding the argument and informing readers what to expect.",
            },
        ]





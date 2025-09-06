from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Dict, Any

from flask import Flask, jsonify, render_template, request, redirect, url_for, session

from services.qa_engine import QAEngine, AnswerResult
from services.gamification import GamificationEngine
from services.course_manager import CourseManager
from services.coding_challenges import CodingChallenges
from services.resume_analyzer import ResumeAnalyzer
from services.interview_prep import InterviewPrep

def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Initialize services
    dataset_path = os.path.join(os.path.dirname(__file__), "data", "qa_dataset.json")
    app.qa_engine = QAEngine(dataset_path=dataset_path)
    app.gamification = GamificationEngine()
    app.course_manager = CourseManager()
    app.coding_challenges = CodingChallenges()
    app.resume_analyzer = ResumeAnalyzer()
    app.interview_prep = InterviewPrep()

    @app.get("/")
    def home() -> str:
        return render_template("index.html")

    @app.get("/courses")
    def courses() -> str:
        return render_template("courses.html")

    @app.get("/coding")
    def coding() -> str:
        return render_template("coding.html")

    @app.get("/resume")
    def resume() -> str:
        return render_template("resume.html")

    @app.get("/interview")
    def interview() -> str:
        return render_template("interview.html")

    @app.get("/profile")
    def profile() -> str:
        return render_template("profile.html")

    @app.get("/health")
    def health() -> Any:
        return jsonify({"status": "ok", "items": app.qa_engine.size})

    @app.post("/api/ask")
    def api_ask() -> Any:
        payload = request.get_json(silent=True) or {}
        question = (payload.get("question") or "").strip()
        subject = (payload.get("subject") or "General").strip()
        if not question:
            return jsonify({"error": "Question is required."}), 400
        result: AnswerResult = app.qa_engine.answer(question=question, subject=subject)
        return jsonify({
            "answer": result.answer,
            "subject": result.subject,
            "confidence": result.confidence,
            "sources": [
                {
                    "question": s.question,
                    "subject": s.subject,
                    "score": s.score,
                } for s in result.sources
            ]
        })

    @app.get("/api/courses")
    def api_courses() -> Any:
        courses = app.course_manager.get_all_courses()
        return jsonify(courses)

    @app.get("/api/challenges")
    def api_challenges() -> Any:
        challenges = app.coding_challenges.get_challenges()
        return jsonify(challenges)

    @app.post("/api/submit-challenge")
    def api_submit_challenge() -> Any:
        payload = request.get_json(silent=True) or {}
        challenge_id = payload.get("challenge_id")
        code = payload.get("code")
        language = payload.get("language", "python")
        
        if not challenge_id or not code:
            return jsonify({"error": "Challenge ID and code are required"}), 400
        
        result = app.coding_challenges.run_test(challenge_id, code, language)
        return jsonify(result)

    @app.post("/api/analyze-resume")
    def api_analyze_resume() -> Any:
        payload = request.get_json(silent=True) or {}
        resume_text = payload.get("resume_text", "").strip()
        
        if not resume_text:
            return jsonify({"error": "Resume text is required"}), 400
        
        analysis = app.resume_analyzer.analyze(resume_text)
        return jsonify(analysis)

    @app.get("/api/interview-questions")
    def api_interview_questions() -> Any:
        subject = request.args.get("subject", "general")
        questions = app.interview_prep.get_questions(subject)
        return jsonify(questions)

    @app.post("/api/complete-lesson")
    def api_complete_lesson() -> Any:
        payload = request.get_json(silent=True) or {}
        lesson_id = payload.get("lesson_id")
        score = payload.get("score", 0)
        
        if not lesson_id:
            return jsonify({"error": "Lesson ID is required"}), 400
        
        # Update user progress and award points
        user_id = session.get('user_id', 'anonymous')
        result = app.gamification.complete_lesson(user_id, lesson_id, score)
        return jsonify(result)

    @app.get("/api/user-progress")
    def api_user_progress() -> Any:
        user_id = session.get('user_id', 'anonymous')
        progress = app.gamification.get_user_progress(user_id)
        return jsonify(progress)

    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)




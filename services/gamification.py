from __future__ import annotations
import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    icon: str
    points: int
    unlocked: bool = False

@dataclass
class UserProgress:
    user_id: str
    level: int
    experience: int
    total_points: int
    completed_lessons: List[str]
    achievements: List[str]
    streak_days: int
    last_login: str

class GamificationEngine:
    def __init__(self):
        self.achievements = self._load_achievements()
        self.user_progress = {}  # In production, use a database
        
    def _load_achievements(self) -> List[Achievement]:
        return [
            Achievement("first_lesson", "First Steps", "Complete your first lesson", "🎯", 50),
            Achievement("streak_3", "On Fire", "Maintain a 3-day learning streak", "🔥", 100),
            Achievement("streak_7", "Unstoppable", "Maintain a 7-day learning streak", "⚡", 200),
            Achievement("perfect_score", "Perfectionist", "Get 100% on any lesson", "🏆", 150),
            Achievement("course_complete", "Course Master", "Complete an entire course", "🎓", 500),
            Achievement("helpful_peer", "Helper", "Help 5 other students", "🤝", 100),
            Achievement("early_bird", "Early Bird", "Study before 8 AM", "🌅", 75),
            Achievement("night_owl", "Night Owl", "Study after 10 PM", "🦉", 75),
        ]
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                level=1,
                experience=0,
                total_points=0,
                completed_lessons=[],
                achievements=[],
                streak_days=0,
                last_login=""
            )
        
        progress = self.user_progress[user_id]
        return {
            "level": progress.level,
            "experience": progress.experience,
            "total_points": progress.total_points,
            "completed_lessons": len(progress.completed_lessons),
            "achievements": len(progress.achievements),
            "streak_days": progress.streak_days,
            "next_level_exp": self._get_next_level_exp(progress.level),
            "progress_percentage": self._get_level_progress(progress.level, progress.experience)
        }
    
    def complete_lesson(self, user_id: str, lesson_id: str, score: int) -> Dict[str, Any]:
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                level=1,
                experience=0,
                total_points=0,
                completed_lessons=[],
                achievements=[],
                streak_days=0,
                last_login=""
            )
        
        progress = self.user_progress[user_id]
        
        # Award experience and points based on score
        exp_gained = int(score * 10)  # 10 exp per percentage point
        points_gained = int(score * 2)  # 2 points per percentage point
        
        progress.experience += exp_gained
        progress.total_points += points_gained
        
        if lesson_id not in progress.completed_lessons:
            progress.completed_lessons.append(lesson_id)
        
        # Check for level up
        old_level = progress.level
        progress.level = self._calculate_level(progress.experience)
        
        # Check for achievements
        new_achievements = self._check_achievements(progress)
        
        # Update streak
        progress.streak_days += 1
        
        return {
            "exp_gained": exp_gained,
            "points_gained": points_gained,
            "leveled_up": progress.level > old_level,
            "new_level": progress.level,
            "new_achievements": new_achievements,
            "total_points": progress.total_points,
            "streak_days": progress.streak_days
        }
    
    def _calculate_level(self, experience: int) -> int:
        # Simple level calculation: every 100 exp = 1 level
        return (experience // 100) + 1
    
    def _get_next_level_exp(self, current_level: int) -> int:
        return current_level * 100
    
    def _get_level_progress(self, level: int, experience: int) -> float:
        current_level_exp = (level - 1) * 100
        next_level_exp = level * 100
        progress = experience - current_level_exp
        total_needed = next_level_exp - current_level_exp
        return min(100.0, (progress / total_needed) * 100)
    
    def _check_achievements(self, progress: UserProgress) -> List[str]:
        new_achievements = []
        
        # Check first lesson achievement
        if len(progress.completed_lessons) == 1 and "first_lesson" not in progress.achievements:
            progress.achievements.append("first_lesson")
            new_achievements.append("first_lesson")
        
        # Check streak achievements
        if progress.streak_days >= 3 and "streak_3" not in progress.achievements:
            progress.achievements.append("streak_3")
            new_achievements.append("streak_3")
        
        if progress.streak_days >= 7 and "streak_7" not in progress.achievements:
            progress.achievements.append("streak_7")
            new_achievements.append("streak_7")
        
        # Check course completion (simplified)
        if len(progress.completed_lessons) >= 10 and "course_complete" not in progress.achievements:
            progress.achievements.append("course_complete")
            new_achievements.append("course_complete")
        
        return new_achievements
    
    def get_leaderboard(self) -> List[Dict[str, Any]]:
        # Simple leaderboard based on total points
        leaderboard = []
        for user_id, progress in self.user_progress.items():
            leaderboard.append({
                "user_id": user_id,
                "level": progress.level,
                "total_points": progress.total_points,
                "completed_lessons": len(progress.completed_lessons)
            })
        
        leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
        return leaderboard[:10]  # Top 10


from __future__ import annotations
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class Lesson:
    id: str
    title: str
    description: str
    duration: int  # minutes
    difficulty: str  # beginner, intermediate, advanced
    type: str  # video, quiz, coding, reading
    content: str
    quiz_questions: List[Dict[str, Any]]

@dataclass
class Course:
    id: str
    title: str
    description: str
    instructor: str
    category: str
    difficulty: str
    duration: int  # total hours
    lessons: List[Lesson]
    rating: float
    enrolled_students: int
    price: float
    certificate: bool

class CourseManager:
    def __init__(self):
        self.courses = self._load_courses()
    
    def _load_courses(self) -> List[Course]:
        return [
            Course(
                id="python_basics",
                title="Python Programming Fundamentals",
                description="Learn Python from scratch with hands-on projects and real-world examples.",
                instructor="Dr. Sarah Chen",
                category="Programming",
                difficulty="Beginner",
                duration=20,
                lessons=self._get_python_lessons(),
                rating=4.8,
                enrolled_students=15420,
                price=0.0,
                certificate=True
            ),
            Course(
                id="data_science_intro",
                title="Introduction to Data Science",
                description="Master the fundamentals of data analysis, visualization, and machine learning.",
                instructor="Prof. Michael Rodriguez",
                category="Data Science",
                difficulty="Intermediate",
                duration=25,
                lessons=self._get_data_science_lessons(),
                rating=4.9,
                enrolled_students=12850,
                price=49.99,
                certificate=True
            ),
            Course(
                id="web_development",
                title="Full-Stack Web Development",
                description="Build modern web applications with HTML, CSS, JavaScript, and Python.",
                instructor="Alex Johnson",
                category="Web Development",
                difficulty="Intermediate",
                duration=30,
                lessons=self._get_web_dev_lessons(),
                rating=4.7,
                enrolled_students=9870,
                price=79.99,
                certificate=True
            ),
            Course(
                id="machine_learning",
                title="Machine Learning Fundamentals",
                description="Understand ML algorithms, neural networks, and practical applications.",
                instructor="Dr. Emily Watson",
                category="Machine Learning",
                difficulty="Advanced",
                duration=35,
                lessons=self._get_ml_lessons(),
                rating=4.9,
                enrolled_students=7560,
                price=99.99,
                certificate=True
            ),
            Course(
                id="interview_prep",
                title="Technical Interview Preparation",
                description="Master coding interviews with data structures, algorithms, and system design.",
                instructor="Tech Recruiter Team",
                category="Career",
                difficulty="Intermediate",
                duration=15,
                lessons=self._get_interview_lessons(),
                rating=4.6,
                enrolled_students=11200,
                price=29.99,
                certificate=False
            )
        ]
    
    def _get_python_lessons(self) -> List[Lesson]:
        return [
            Lesson(
                id="python_1",
                title="Introduction to Python",
                description="Learn Python basics, variables, and data types",
                duration=45,
                difficulty="beginner",
                type="video",
                content="Python is a versatile programming language...",
                quiz_questions=[
                    {
                        "question": "What is Python?",
                        "options": ["A snake", "A programming language", "A database", "An operating system"],
                        "correct": 1
                    }
                ]
            ),
            Lesson(
                id="python_2",
                title="Control Flow",
                description="Master if statements, loops, and functions",
                duration=60,
                difficulty="beginner",
                type="coding",
                content="Control flow determines the order of execution...",
                quiz_questions=[]
            )
        ]
    
    def _get_data_science_lessons(self) -> List[Lesson]:
        return [
            Lesson(
                id="ds_1",
                title="Data Analysis with Pandas",
                description="Learn to manipulate and analyze data using pandas",
                duration=75,
                difficulty="intermediate",
                type="video",
                content="Pandas is a powerful data manipulation library...",
                quiz_questions=[]
            )
        ]
    
    def _get_web_dev_lessons(self) -> List[Lesson]:
        return [
            Lesson(
                id="web_1",
                title="HTML & CSS Basics",
                description="Build your first webpage with HTML and CSS",
                duration=90,
                difficulty="beginner",
                type="video",
                content="HTML provides structure while CSS adds styling...",
                quiz_questions=[]
            )
        ]
    
    def _get_ml_lessons(self) -> List[Lesson]:
        return [
            Lesson(
                id="ml_1",
                title="Introduction to Machine Learning",
                description="Understand the basics of ML and its applications",
                duration=120,
                difficulty="advanced",
                type="video",
                content="Machine learning enables computers to learn...",
                quiz_questions=[]
            )
        ]
    
    def _get_interview_lessons(self) -> List[Lesson]:
        return [
            Lesson(
                id="int_1",
                title="Data Structures Review",
                description="Review arrays, linked lists, trees, and graphs",
                duration=60,
                difficulty="intermediate",
                type="video",
                content="Data structures are fundamental to programming...",
                quiz_questions=[]
            )
        ]
    
    def get_all_courses(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "instructor": course.instructor,
                "category": course.category,
                "difficulty": course.difficulty,
                "duration": course.duration,
                "lesson_count": len(course.lessons),
                "rating": course.rating,
                "enrolled_students": course.enrolled_students,
                "price": course.price,
                "certificate": course.certificate
            }
            for course in self.courses
        ]
    
    def get_course_by_id(self, course_id: str) -> Course:
        for course in self.courses:
            if course.id == course_id:
                return course
        raise ValueError(f"Course {course_id} not found")
    
    def get_courses_by_category(self, category: str) -> List[Course]:
        return [course for course in self.courses if course.category.lower() == category.lower()]
    
    def get_courses_by_difficulty(self, difficulty: str) -> List[Course]:
        return [course for course in self.courses if course.difficulty.lower() == difficulty.lower()]
    
    def search_courses(self, query: str) -> List[Course]:
        query = query.lower()
        results = []
        for course in self.courses:
            if (query in course.title.lower() or 
                query in course.description.lower() or 
                query in course.instructor.lower() or
                query in course.category.lower()):
                results.append(course)
        return results


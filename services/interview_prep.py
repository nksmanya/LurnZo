from __future__ import annotations
from typing import Dict, List, Any
from dataclasses import dataclass
import random

@dataclass
class InterviewQuestion:
    id: str
    question: str
    category: str
    difficulty: str
    answer: str
    hints: List[str]
    related_topics: List[str]

class InterviewPrep:
    def __init__(self):
        self.questions = self._load_questions()
    
    def _load_questions(self) -> List[InterviewQuestion]:
        return [
            # Data Structures
            InterviewQuestion(
                id="ds_arrays_1",
                question="What is the time complexity of accessing an element in an array?",
                category="data_structures",
                difficulty="easy",
                answer="O(1) - Array elements can be accessed directly using their index, making it a constant time operation.",
                hints=["Think about how arrays store data in memory", "Consider what happens when you use array[5]"],
                related_topics=["arrays", "time complexity", "memory access"]
            ),
            InterviewQuestion(
                id="ds_linkedlist_1",
                question="What is the difference between a singly linked list and a doubly linked list?",
                category="data_structures",
                difficulty="easy",
                answer="A singly linked list has nodes that only point to the next node, while a doubly linked list has nodes that point to both the next and previous nodes. This allows traversal in both directions but uses more memory.",
                hints=["Think about the direction of pointers", "Consider memory usage"],
                related_topics=["linked lists", "pointers", "memory efficiency"]
            ),
            InterviewQuestion(
                id="ds_stack_queue_1",
                question="Explain the difference between a stack and a queue. Give a real-world example of each.",
                category="data_structures",
                difficulty="easy",
                answer="A stack follows LIFO (Last In, First Out) - like a stack of plates where you take from the top. A queue follows FIFO (First In, First Out) - like a line of people waiting for a bus. Real examples: Stack - browser back button, Queue - printer job queue.",
                hints=["Think about the order of removal", "Consider everyday scenarios"],
                related_topics=["stacks", "queues", "LIFO", "FIFO"]
            ),
            
            # Algorithms
            InterviewQuestion(
                id="algo_sorting_1",
                question="What is the time complexity of bubble sort in the worst case?",
                category="algorithms",
                difficulty="easy",
                answer="O(n²) - In the worst case, bubble sort needs to make n passes through the array, and in each pass, it may need to swap adjacent elements up to n times.",
                hints=["Think about nested loops", "Consider what happens with a reverse-sorted array"],
                related_topics=["bubble sort", "time complexity", "sorting algorithms"]
            ),
            InterviewQuestion(
                id="algo_searching_1",
                question="When would you use binary search instead of linear search?",
                category="algorithms",
                difficulty="easy",
                answer="Binary search is more efficient (O(log n) vs O(n)) but requires the data to be sorted. Use binary search when you have a large, sorted dataset and need to find elements quickly. Use linear search for small datasets or unsorted data.",
                hints=["Consider the prerequisites for binary search", "Think about performance trade-offs"],
                related_topics=["binary search", "linear search", "time complexity", "sorted data"]
            ),
            InterviewQuestion(
                id="algo_recursion_1",
                question="What is recursion and when would you use it?",
                category="algorithms",
                difficulty="medium",
                answer="Recursion is when a function calls itself. It's useful for problems that can be broken down into smaller, similar subproblems (like tree traversal, factorial calculation, or merge sort). However, it can lead to stack overflow for deep recursion.",
                hints=["Think about problems that repeat themselves", "Consider the call stack"],
                related_topics=["recursion", "call stack", "divide and conquer"]
            ),
            
            # System Design
            InterviewQuestion(
                id="sys_url_shortener",
                question="How would you design a URL shortening service like bit.ly?",
                category="system_design",
                difficulty="medium",
                answer="Key components: 1) URL shortening algorithm (hash function + base62 encoding), 2) Database to store original URLs and short codes, 3) Redirect service, 4) Analytics tracking. Consider: scalability (load balancers, caching), storage (SQL vs NoSQL), and handling collisions.",
                hints=["Think about the core functionality first", "Consider what happens when someone clicks a short URL"],
                related_topics=["system design", "scalability", "databases", "caching"]
            ),
            InterviewQuestion(
                id="sys_chat_system",
                question="Design a real-time chat system like WhatsApp or Slack.",
                category="system_design",
                difficulty="medium",
                answer="Components: 1) WebSocket connections for real-time communication, 2) Message storage (database), 3) User authentication, 4) Push notifications. Challenges: handling millions of concurrent connections, message ordering, offline message delivery, and scalability across multiple servers.",
                hints=["Think about real-time requirements", "Consider what happens when users go offline"],
                related_topics=["real-time systems", "WebSockets", "scalability", "push notifications"]
            ),
            
            # Programming Languages
            InterviewQuestion(
                id="lang_python_1",
                question="What is the difference between a list and a tuple in Python?",
                category="programming_languages",
                difficulty="easy",
                answer="Lists are mutable (can be changed after creation) while tuples are immutable (cannot be changed). Lists use square brackets [1,2,3], tuples use parentheses (1,2,3). Tuples are faster and use less memory, but lists are more flexible.",
                hints=["Think about what 'mutable' means", "Consider when you might want to prevent changes"],
                related_topics=["Python", "data structures", "mutability", "performance"]
            ),
            InterviewQuestion(
                id="lang_java_1",
                question="What is the difference between == and .equals() in Java?",
                category="programming_languages",
                difficulty="medium",
                answer="== compares object references (memory addresses), while .equals() compares the actual content/values. For String objects, == checks if they point to the same memory location, while .equals() checks if they contain the same characters.",
                hints=["Think about memory vs content", "Consider what happens with String objects"],
                related_topics=["Java", "object comparison", "String objects", "memory management"]
            ),
            
            # Database
            InterviewQuestion(
                id="db_normalization_1",
                question="What is database normalization and why is it important?",
                category="database",
                difficulty="medium",
                answer="Normalization is the process of organizing data to reduce redundancy and improve data integrity. It involves breaking down tables into smaller, related tables. Benefits: eliminates data duplication, reduces storage space, prevents update anomalies, and ensures data consistency.",
                hints=["Think about data redundancy", "Consider what happens when you update data"],
                related_topics=["database design", "normalization", "data integrity", "redundancy"]
            ),
            InterviewQuestion(
                id="db_indexes_1",
                question="What are database indexes and when should you use them?",
                category="database",
                difficulty="medium",
                answer="Indexes are data structures that improve the speed of data retrieval operations. They're like a book's index - instead of scanning every page, you can jump directly to the right section. Use them on columns frequently used in WHERE, JOIN, and ORDER BY clauses. Trade-off: they speed up reads but slow down writes and use additional storage.",
                hints=["Think about how you find information in a book", "Consider the trade-offs"],
                related_topics=["database performance", "indexes", "query optimization", "trade-offs"]
            ),
            
            # Web Development
            InterviewQuestion(
                id="web_http_1",
                question="What is the difference between GET and POST HTTP methods?",
                category="web_development",
                difficulty="easy",
                answer="GET is used to retrieve data and is idempotent (safe to repeat). Data is sent in the URL. POST is used to submit data and is not idempotent. Data is sent in the request body. GET requests can be cached, POST requests cannot. Use GET for reading data, POST for creating/updating data.",
                hints=["Think about what 'idempotent' means", "Consider security implications"],
                related_topics=["HTTP", "REST API", "web security", "caching"]
            ),
            InterviewQuestion(
                id="web_cookies_1",
                question="What are cookies and how do they work?",
                category="web_development",
                difficulty="easy",
                answer="Cookies are small pieces of data stored on the client's browser. They're sent with every HTTP request to the same domain. Common uses: session management, user preferences, tracking. They have expiration dates, can be secure (HTTPS only), and can be httpOnly (not accessible via JavaScript).",
                hints=["Think about how websites remember you", "Consider security aspects"],
                related_topics=["web storage", "session management", "web security", "HTTP"]
            )
        ]
    
    def get_questions(self, subject: str = "general", difficulty: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """Get interview questions filtered by subject and difficulty"""
        filtered_questions = []
        
        for question in self.questions:
            # Filter by subject
            if subject != "general" and question.category != subject:
                continue
            
            # Filter by difficulty
            if difficulty != "all" and question.difficulty != difficulty:
                continue
            
            filtered_questions.append({
                "id": question.id,
                "question": question.question,
                "category": question.category,
                "difficulty": question.difficulty,
                "hints": question.hints,
                "related_topics": question.related_topics
            })
        
        # Shuffle and limit results
        random.shuffle(filtered_questions)
        return filtered_questions[:limit]
    
    def get_question_by_id(self, question_id: str) -> InterviewQuestion:
        """Get a specific question by ID"""
        for question in self.questions:
            if question.id == question_id:
                return question
        raise ValueError(f"Question {question_id} not found")
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all available question categories"""
        categories = {}
        for question in self.questions:
            if question.category not in categories:
                categories[question.category] = {
                    "name": question.category.replace("_", " ").title(),
                    "count": 0,
                    "difficulties": set()
                }
            categories[question.category]["count"] += 1
            categories[question.category]["difficulties"].add(question.difficulty)
        
        return [
            {
                "id": cat_id,
                "name": cat_info["name"],
                "question_count": cat_info["count"],
                "difficulties": list(cat_info["difficulties"])
            }
            for cat_id, cat_info in categories.items()
        ]
    
    def get_difficulty_levels(self) -> List[str]:
        """Get all available difficulty levels"""
        difficulties = set()
        for question in self.questions:
            difficulties.add(question.difficulty)
        return sorted(list(difficulties))
    
    def search_questions(self, query: str) -> List[Dict[str, Any]]:
        """Search questions by keyword"""
        query = query.lower()
        results = []
        
        for question in self.questions:
            if (query in question.question.lower() or 
                query in question.answer.lower() or
                any(query in topic.lower() for topic in question.related_topics)):
                results.append({
                    "id": question.id,
                    "question": question.question,
                    "category": question.category,
                    "difficulty": question.difficulty
                })
        
        return results[:20]  # Limit results
    
    def get_practice_set(self, category: str = "general", difficulty: str = "easy", count: int = 5) -> List[Dict[str, Any]]:
        """Get a practice set of questions for interview preparation"""
        questions = self.get_questions(subject=category, difficulty=difficulty, limit=count)
        
        # Add answer and hints for practice
        practice_questions = []
        for q in questions:
            full_question = self.get_question_by_id(q["id"])
            practice_questions.append({
                "id": full_question.id,
                "question": full_question.question,
                "category": full_question.category,
                "difficulty": full_question.difficulty,
                "hints": full_question.hints,
                "related_topics": full_question.related_topics,
                "answer": full_question.answer
            })
        
        return practice_questions
    
    def get_random_question(self, category: str = "general") -> Dict[str, Any]:
        """Get a random question for quick practice"""
        questions = self.get_questions(subject=category, limit=1)
        if questions:
            return self.get_question_by_id(questions[0]["id"])
        return None



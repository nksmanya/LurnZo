from __future__ import annotations
import subprocess
import tempfile
import os
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TestCase:
    input: str
    expected_output: str
    description: str

@dataclass
class CodingChallenge:
    id: str
    title: str
    description: str
    difficulty: str
    category: str
    problem_statement: str
    examples: List[Dict[str, str]]
    test_cases: List[TestCase]
    starter_code: Dict[str, str]
    time_limit: int  # seconds
    memory_limit: int  # MB

class CodingChallenges:
    def __init__(self):
        self.challenges = self._load_challenges()
    
    def _load_challenges(self) -> List[CodingChallenge]:
        return [
            CodingChallenge(
                id="reverse_string",
                title="Reverse a String",
                description="Write a function to reverse a given string",
                difficulty="easy",
                category="strings",
                problem_statement="Given a string, return the string reversed. For example, 'hello' should return 'olleh'.",
                examples=[
                    {"input": "hello", "output": "olleh"},
                    {"input": "world", "output": "dlrow"}
                ],
                test_cases=[
                    TestCase("hello", "olleh", "Basic string reversal"),
                    TestCase("python", "nohtyp", "Python string"),
                    TestCase("", "", "Empty string"),
                    TestCase("a", "a", "Single character")
                ],
                starter_code={
                    "python": "def reverse_string(s):\n    # Your code here\n    pass",
                    "javascript": "function reverseString(s) {\n    // Your code here\n}",
                    "java": "public class Solution {\n    public String reverseString(String s) {\n        // Your code here\n        return \"\";\n    }\n}"
                },
                time_limit=5,
                memory_limit=128
            ),
            CodingChallenge(
                id="find_max",
                title="Find Maximum Number",
                description="Find the maximum number in an array",
                difficulty="easy",
                category="arrays",
                problem_statement="Given an array of integers, return the maximum number in the array.",
                examples=[
                    {"input": "[1, 3, 5, 2, 4]", "output": "5"},
                    {"input": "[-1, -5, -3]", "output": "-1"}
                ],
                test_cases=[
                    TestCase("[1, 3, 5, 2, 4]", "5", "Positive numbers"),
                    TestCase("[-1, -5, -3]", "-1", "Negative numbers"),
                    TestCase("[42]", "42", "Single element"),
                    TestCase("[]", "None", "Empty array")
                ],
                starter_code={
                    "python": "def find_max(arr):\n    # Your code here\n    pass",
                    "javascript": "function findMax(arr) {\n    // Your code here\n}",
                    "java": "public class Solution {\n    public Integer findMax(int[] arr) {\n        // Your code here\n        return null;\n    }\n}"
                },
                time_limit=5,
                memory_limit=128
            ),
            CodingChallenge(
                id="fibonacci",
                title="Fibonacci Sequence",
                description="Calculate the nth Fibonacci number",
                difficulty="medium",
                category="recursion",
                problem_statement="Write a function to calculate the nth Fibonacci number. F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2).",
                examples=[
                    {"input": "5", "output": "5"},
                    {"input": "10", "output": "55"}
                ],
                test_cases=[
                    TestCase("0", "0", "Base case 0"),
                    TestCase("1", "1", "Base case 1"),
                    TestCase("5", "5", "Small number"),
                    TestCase("10", "55", "Medium number")
                ],
                starter_code={
                    "python": "def fibonacci(n):\n    # Your code here\n    pass",
                    "javascript": "function fibonacci(n) {\n    // Your code here\n}",
                    "java": "public class Solution {\n    public int fibonacci(int n) {\n        // Your code here\n        return 0;\n    }\n}"
                },
                time_limit=10,
                memory_limit=256
            ),
            CodingChallenge(
                id="palindrome",
                title="Check Palindrome",
                description="Check if a string is a palindrome",
                difficulty="easy",
                category="strings",
                problem_statement="A palindrome is a string that reads the same forwards and backwards. Write a function to check if a given string is a palindrome.",
                examples=[
                    {"input": "racecar", "output": "true"},
                    {"input": "hello", "output": "false"}
                ],
                test_cases=[
                    TestCase("racecar", "true", "Palindrome"),
                    TestCase("hello", "false", "Not palindrome"),
                    TestCase("", "true", "Empty string"),
                    TestCase("a", "true", "Single character"),
                    TestCase("A man a plan a canal Panama", "false", "With spaces")
                ],
                starter_code={
                    "python": "def is_palindrome(s):\n    # Your code here\n    pass",
                    "javascript": "function isPalindrome(s) {\n    // Your code here\n}",
                    "java": "public class Solution {\n    public boolean isPalindrome(String s) {\n        // Your code here\n        return false;\n    }\n}"
                },
                time_limit=5,
                memory_limit=128
            )
        ]
    
    def get_challenges(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "difficulty": challenge.difficulty,
                "category": challenge.category,
                "examples": challenge.examples
            }
            for challenge in self.challenges
        ]
    
    def get_challenge_by_id(self, challenge_id: str) -> CodingChallenge:
        for challenge in self.challenges:
            if challenge.id == challenge_id:
                return challenge
        raise ValueError(f"Challenge {challenge_id} not found")
    
    def run_test(self, challenge_id: str, code: str, language: str = "python") -> Dict[str, Any]:
        challenge = self.get_challenge_by_id(challenge_id)
        
        if language not in challenge.starter_code:
            return {"error": f"Language {language} not supported for this challenge"}
        
        try:
            if language == "python":
                return self._run_python_test(challenge, code)
            elif language == "javascript":
                return self._run_javascript_test(challenge, code)
            elif language == "java":
                return self._run_java_test(challenge, code)
            else:
                return {"error": f"Language {language} not supported"}
        except Exception as e:
            return {"error": f"Execution error: {str(e)}"}
    
    def _run_python_test(self, challenge: CodingChallenge, code: str) -> Dict[str, Any]:
        results = []
        passed = 0
        
        for test_case in challenge.test_cases:
            try:
                # Create a temporary file with the code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    f.write(f"\n\n# Test the function\nresult = {challenge.id}('{test_case.input}')\nprint(result)")
                    temp_file = f.name
                
                # Run the code
                result = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=challenge.time_limit
                )
                
                # Clean up
                os.unlink(temp_file)
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    if output == test_case.expected_output:
                        results.append({
                            "test_case": test_case.description,
                            "status": "passed",
                            "input": test_case.input,
                            "expected": test_case.expected_output,
                            "output": output
                        })
                        passed += 1
                    else:
                        results.append({
                            "test_case": test_case.description,
                            "status": "failed",
                            "input": test_case.input,
                            "expected": test_case.expected_output,
                            "output": output
                        })
                else:
                    results.append({
                        "test_case": test_case.description,
                        "status": "error",
                        "error": result.stderr
                    })
                    
            except subprocess.TimeoutExpired:
                results.append({
                    "test_case": test_case.description,
                    "status": "timeout",
                    "error": "Execution timed out"
                })
            except Exception as e:
                results.append({
                    "test_case": test_case.description,
                    "status": "error",
                    "error": str(e)
                })
        
        score = (passed / len(challenge.test_cases)) * 100 if challenge.test_cases else 0
        
        return {
            "challenge_id": challenge.id,
            "total_tests": len(challenge.test_cases),
            "passed_tests": passed,
            "score": score,
            "results": results
        }
    
    def _run_javascript_test(self, challenge: CodingChallenge, code: str) -> Dict[str, Any]:
        # Similar to Python but for Node.js
        # This is a simplified version
        return {"error": "JavaScript execution not fully implemented yet"}
    
    def _run_java_test(self, challenge: CodingChallenge, code: str) -> Dict[str, Any]:
        # Similar to Python but for Java
        # This is a simplified version
        return {"error": "Java execution not fully implemented yet"}
    
    def get_challenges_by_difficulty(self, difficulty: str) -> List[CodingChallenge]:
        return [c for c in self.challenges if c.difficulty.lower() == difficulty.lower()]
    
    def get_challenges_by_category(self, category: str) -> List[CodingChallenge]:
        return [c for c in self.challenges if c.category.lower() == category.lower()]


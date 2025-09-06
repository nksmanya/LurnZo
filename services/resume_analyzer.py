from typing import Dict, List, Any, Optional
import json
import re
from dataclasses import dataclass


@dataclass
class ResumeSection:
    """Represents a section of a resume"""
    title: str
    content: str
    confidence: float


@dataclass
class ResumeAnalysis:
    """Result of resume analysis"""
    overall_score: float
    sections: List[ResumeSection]
    suggestions: List[str]
    skills_found: List[str]
    experience_years: Optional[float]
    education_level: Optional[str]


class ResumeAnalyzer:
    """Service for analyzing resumes and providing feedback"""
    
    def __init__(self):
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'tools': ['git', 'jenkins', 'jira', 'confluence', 'slack', 'figma'],
            'frameworks': ['spring', 'express', 'fastapi', 'laravel', 'rails', 'asp.net']
        }
        
        self.education_keywords = {
            'phd': ['phd', 'doctorate', 'doctor of philosophy'],
            'masters': ['masters', 'ms', 'ma', 'mba'],
            'bachelors': ['bachelors', 'bs', 'ba', 'bachelor'],
            'associate': ['associate', 'aa', 'as'],
            'high_school': ['high school', 'diploma', 'ged']
        }
    
    def analyze_resume(self, resume_text: str) -> ResumeAnalysis:
        """
        Analyze a resume and provide feedback
        
        Args:
            resume_text: Raw text content of the resume
            
        Returns:
            ResumeAnalysis object with analysis results
        """
        # Extract sections
        sections = self._extract_sections(resume_text)
        
        # Analyze skills
        skills_found = self._extract_skills(resume_text.lower())
        
        # Estimate experience years
        experience_years = self._estimate_experience(resume_text)
        
        # Determine education level
        education_level = self._determine_education_level(resume_text.lower())
        
        # Calculate overall score
        overall_score = self._calculate_score(sections, skills_found, experience_years, education_level)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(sections, skills_found, experience_years, education_level)
        
        return ResumeAnalysis(
            overall_score=overall_score,
            sections=sections,
            suggestions=suggestions,
            skills_found=skills_found,
            experience_years=experience_years,
            education_level=education_level
        )
    
    def _extract_sections(self, text: str) -> List[ResumeSection]:
        """Extract different sections from resume text"""
        sections = []
        
        # Common section headers
        section_patterns = [
            r'(?i)(experience|work experience|employment history)',
            r'(?i)(education|academic background)',
            r'(?i)(skills|technical skills|competencies)',
            r'(?i)(projects|portfolio)',
            r'(?i)(certifications|certificates)',
            r'(?i)(awards|achievements|honors)',
            r'(?i)(volunteer|community service)',
            r'(?i)(languages|language skills)'
        ]
        
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a section header
            is_header = any(re.search(pattern, line) for pattern in section_patterns)
            
            if is_header:
                # Save previous section if exists
                if current_section and current_content:
                    sections.append(ResumeSection(
                        title=current_section,
                        content='\n'.join(current_content),
                        confidence=0.8
                    ))
                
                # Start new section
                current_section = line
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections.append(ResumeSection(
                title=current_section,
                content='\n'.join(current_content),
                confidence=0.8
            ))
        
        return sections
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        
        for category, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    skills.append(keyword)
        
        return list(set(skills))  # Remove duplicates
    
    def _estimate_experience(self, text: str) -> Optional[float]:
        """Estimate years of experience from resume"""
        # Look for date patterns
        date_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|\bpresent\b)',
            r'(\d{4})\s*[-–]\s*(\bnow\b)',
            r'(\d{1,2})\s+years?\s+of\s+experience',
            r'(\d{1,2})\+\s+years?\s+of\s+experience'
        ]
        
        total_years = 0
        found_dates = []
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    if match[1].lower() in ['present', 'now']:
                        # Current position
                        found_dates.append((int(match[0]), 2024))  # Assume current year
                    else:
                        # Past position
                        try:
                            start_year = int(match[0])
                            end_year = int(match[1])
                            found_dates.append((start_year, end_year))
                        except ValueError:
                            continue
        
        # Calculate total years
        if found_dates:
            for start, end in found_dates:
                total_years += end - start
        
        return total_years if total_years > 0 else None
    
    def _determine_education_level(self, text: str) -> Optional[str]:
        """Determine the highest education level"""
        for level, keywords in self.education_keywords.items():
            if any(keyword in text for keyword in keywords):
                return level
        
        return None
    
    def _calculate_score(self, sections: List[ResumeSection], skills: List[str], 
                        experience: Optional[float], education: Optional[str]) -> float:
        """Calculate overall resume score"""
        score = 0.0
        
        # Section completeness (40%)
        if sections:
            section_score = min(len(sections) / 6.0, 1.0) * 40
            score += section_score
        
        # Skills diversity (30%)
        if skills:
            skills_score = min(len(skills) / 15.0, 1.0) * 30
            score += skills_score
        
        # Experience (20%)
        if experience:
            if experience >= 5:
                score += 20
            elif experience >= 3:
                score += 15
            elif experience >= 1:
                score += 10
        
        # Education (10%)
        if education:
            if education == 'phd':
                score += 10
            elif education == 'masters':
                score += 8
            elif education == 'bachelors':
                score += 6
            elif education == 'associate':
                score += 4
        
        return min(score, 100.0)
    
    def _generate_suggestions(self, sections: List[ResumeSection], skills: List[str],
                             experience: Optional[float], education: Optional[str]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Section suggestions
        if len(sections) < 4:
            suggestions.append("Consider adding more sections like Projects, Certifications, or Awards")
        
        # Skills suggestions
        if len(skills) < 5:
            suggestions.append("Include more technical skills to showcase your expertise")
        
        # Experience suggestions
        if not experience or experience < 1:
            suggestions.append("Highlight any internships, projects, or volunteer work to demonstrate experience")
        
        # Education suggestions
        if not education:
            suggestions.append("Clearly list your educational background and any relevant certifications")
        
        # General suggestions
        suggestions.append("Use action verbs to describe your achievements")
        suggestions.append("Quantify your accomplishments with specific numbers and metrics")
        suggestions.append("Ensure consistent formatting and professional appearance")
        
        return suggestions
    
    def get_resume_templates(self) -> List[Dict[str, Any]]:
        """Get available resume templates"""
        return [
            {
                "id": "modern",
                "name": "Modern Professional",
                "description": "Clean, contemporary design suitable for most industries",
                "category": "professional"
            },
            {
                "id": "creative",
                "name": "Creative Portfolio",
                "description": "Bold design for creative and design-focused roles",
                "category": "creative"
            },
            {
                "id": "minimal",
                "name": "Minimalist",
                "description": "Simple, elegant design that focuses on content",
                "category": "minimal"
            },
            {
                "id": "executive",
                "name": "Executive",
                "description": "Sophisticated design for senior-level positions",
                "category": "executive"
            }
        ]
    
    def validate_resume_format(self, resume_text: str) -> Dict[str, Any]:
        """Validate resume format and provide feedback"""
        issues = []
        warnings = []
        
        # Check length
        if len(resume_text) < 500:
            warnings.append("Resume may be too short - consider adding more details")
        elif len(resume_text) > 2000:
            warnings.append("Resume may be too long - consider condensing information")
        
        # Check for common issues
        if not re.search(r'@', resume_text):
            issues.append("Email address not found")
        
        if not re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', resume_text):
            warnings.append("Phone number not found or may be in unexpected format")
        
        # Check for typos (basic check)
        common_typos = ['resume', 'experience', 'education', 'skills']
        for word in common_typos:
            if word not in resume_text.lower():
                warnings.append(f"'{word}' section not clearly identified")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "word_count": len(resume_text.split())
        }

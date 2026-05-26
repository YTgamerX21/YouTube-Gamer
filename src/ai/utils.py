"""
Utility functions for the AI module
"""

import re
from typing import List, Dict, Any


class TextProcessor:
    """Process and clean text"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Remove extra whitespace and clean text"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[str]:
        """Extract code blocks from text"""
        pattern = r'```([\s\S]*?)```'
        matches = re.findall(pattern, text)
        return matches
    
    @staticmethod
    def split_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]


class CodeFormatter:
    """Format and beautify code"""
    
    @staticmethod
    def indent_code(code: str, spaces: int = 4) -> str:
        """Add indentation to code"""
        indent = ' ' * spaces
        lines = code.split('\n')
        return '\n'.join(indent + line for line in lines)
    
    @staticmethod
    def remove_indent(code: str) -> str:
        """Remove leading indentation"""
        lines = code.split('\n')
        min_indent = float('inf')
        
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        if min_indent == float('inf'):
            return code
        
        return '\n'.join(line[min_indent:] if len(line) > min_indent else line for line in lines)
    
    @staticmethod
    def add_line_numbers(code: str) -> str:
        """Add line numbers to code"""
        lines = code.split('\n')
        numbered = [f"{i+1:3d} | {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered)


class LanguageDetector:
    """Detect programming languages"""
    
    LANGUAGE_PATTERNS = {
        'python': [
            r'\bdef\s+\w+\s*\(',
            r'\bclass\s+\w+',
            r'\bimport\s+\w+',
            r'\bfrom\s+\w+\s+import',
            r'\bif\s+__name__\s*==\s*'
        ],
        'javascript': [
            r'\bfunction\s+\w+\s*\(',
            r'\bconst\s+\w+\s*=',
            r'\blet\s+\w+\s*=',
            r'\bvar\s+\w+\s*=',
            r'=>',
        ],
        'java': [
            r'\bpublic\s+class\s+\w+',
            r'\bpublic\s+static\s+void',
            r'\bimport\s+\w+',
        ],
        'cpp': [
            r'#include\s*[<"]',
            r'\bint\s+main\s*\(',
            r'std::',
        ],
        'csharp': [
            r'\busing\s+\w+',
            r'\bnamespace\s+\w+',
            r'\bpublic\s+class\s+\w+',
        ],
    }
    
    @classmethod
    def detect(cls, code: str) -> str:
        """Detect programming language from code"""
        code_lower = code.lower()
        
        for language, patterns in cls.LANGUAGE_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, code_lower):
                    matches += 1
            
            if matches > 0:
                return language
        
        return 'unknown'


class TokenCounter:
    """Count tokens in text (approximate)"""
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """Count approximate tokens (words + punctuation)"""
        # Simple approximation: ~1.3 tokens per word
        words = len(text.split())
        return int(words * 1.3)
    
    @staticmethod
    def truncate_to_tokens(text: str, max_tokens: int) -> str:
        """Truncate text to maximum tokens"""
        words = text.split()
        max_words = int(max_tokens / 1.3)
        return ' '.join(words[:max_words])


class SimilarityChecker:
    """Check similarity between texts"""
    
    @staticmethod
    def jaccard_similarity(text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts"""
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0

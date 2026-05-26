"""
Core AI Engine - Main intelligence module
Inspired by GitHub Copilot and ChatGPT
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class AIModel(ABC):
    """Abstract base class for AI models"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        pass
    
    @abstractmethod
    def complete(self, code: str, language: str = "python") -> str:
        """Complete code based on context"""
        pass


class ConversationHistory:
    """Manage conversation history for context"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []
    
    def add(self, role: str, content: str):
        """Add message to history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(message)
        
        # Keep only recent messages
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history:]
    
    def get_context(self) -> str:
        """Get formatted conversation context"""
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.history[-5:]
        ])
        return context
    
    def clear(self):
        """Clear conversation history"""
        self.history = []


class CodeAnalyzer:
    """Analyze code for patterns and suggestions"""
    
    @staticmethod
    def detect_language(code: str) -> str:
        """Detect programming language from code"""
        language_patterns = {
            "python": ["def ", "import ", "class ", "if __name__"],
            "javascript": ["function", "const ", "let ", "var ", "=>"],
            "java": ["public class", "public static", "import ", "package"],
            "cpp": ["#include", "int main", "std::", "using namespace"],
            "csharp": ["using ", "namespace ", "public class", "public static"],
        }
        
        for lang, patterns in language_patterns.items():
            if any(pattern in code for pattern in patterns):
                return lang
        
        return "unknown"
    
    @staticmethod
    def extract_context(code: str, position: int = -1) -> Dict[str, Any]:
        """Extract contextual information from code"""
        lines = code.split('\n')
        
        return {
            "language": CodeAnalyzer.detect_language(code),
            "line_count": len(lines),
            "has_functions": "def " in code or "function" in code,
            "has_classes": "class " in code,
            "indentation_level": CodeAnalyzer.detect_indentation(code),
        }
    
    @staticmethod
    def detect_indentation(code: str) -> int:
        """Detect indentation level"""
        for line in code.split('\n'):
            if line.strip():
                return len(line) - len(line.lstrip())
        return 0


class AIAssistant:
    """Main AI Assistant - combines multiple capabilities"""
    
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self.conversation = ConversationHistory()
        self.code_analyzer = CodeAnalyzer()
        self.logger = logger
        
        self.logger.info(f"Initializing AI Assistant with model: {model_name}")
    
    def complete_code(self, 
                     code: str, 
                     language: Optional[str] = None,
                     context: Optional[str] = None) -> str:
        """
        Complete code based on context (Copilot-style)
        
        Args:
            code: Partial code to complete
            language: Programming language (auto-detected if None)
            context: Additional context for completion
        
        Returns:
            Completed code suggestion
        """
        if language is None:
            language = self.code_analyzer.detect_language(code)
        
        code_context = self.code_analyzer.extract_context(code)
        
        prompt = f"""Complete this {language} code snippet:
{code}
Context: {code_context}
Additional info: {context or 'None'}
Completion:"""
        
        completion = self._generate_response(prompt, max_tokens=100)
        self.conversation.add("assistant", completion)
        
        return completion
    
    def ask(self, question: str, context: Optional[str] = None) -> str:
        """
        Answer a question (ChatGPT-style)
        
        Args:
            question: User's question
            context: Additional context
        
        Returns:
            Answer to the question
        """
        self.conversation.add("user", question)
        
        prompt = f"""You are an AI assistant inspired by GitHub Copilot and ChatGPT.
Conversation history:
{self.conversation.get_context()}

User: {question}
Context: {context or 'None'}
Assistant:"""
        
        answer = self._generate_response(prompt, max_tokens=200)
        self.conversation.add("assistant", answer)
        
        return answer
    
    def debug(self, error_message: str, code: str = "") -> str:
        """
        Help debug code errors
        
        Args:
            error_message: Error message or traceback
            code: Related code snippet
        
        Returns:
            Debugging suggestions
        """
        prompt = f"""You are a debugging expert. Analyze this error and provide solutions.

Error: {error_message}
Code: {code}

Debugging suggestions:"""
        
        suggestion = self._generate_response(prompt, max_tokens=250)
        self.conversation.add("assistant", suggestion)
        
        return suggestion
    
    def explain(self, code: str, language: Optional[str] = None) -> str:
        """
        Explain what code does
        
        Args:
            code: Code to explain
            language: Programming language
        
        Returns:
            Explanation of the code
        """
        if language is None:
            language = self.code_analyzer.detect_language(code)
        
        prompt = f"""Explain this {language} code in simple terms:

```{language}
{code}
```

Explanation:"""
        
        explanation = self._generate_response(prompt, max_tokens=200)
        self.conversation.add("assistant", explanation)
        
        return explanation
    
    def _generate_response(self, prompt: str, max_tokens: int = 150) -> str:
        """
        Generate response from prompt
        (Placeholder - implement with actual model)
        """
        # This is a placeholder implementation
        # In production, this would call OpenAI API, Hugging Face, or local model
        self.logger.debug(f"Generating response with prompt: {prompt[:100]}...")
        
        # Simulated response
        return "Generated response placeholder. Connect to actual LLM model for real results."
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation.clear()
        self.logger.info("Conversation history cleared")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return {
            "message_count": len(self.conversation.history),
            "model": self.model_name,
            "recent_messages": self.conversation.history[-3:]
        }

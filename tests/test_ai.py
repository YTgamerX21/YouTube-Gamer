"""
Tests for AI core module
"""

import pytest
from src.ai.core import AIAssistant, CodeAnalyzer, ConversationHistory


class TestConversationHistory:
    """Test conversation history management"""
    
    def test_add_message(self):
        """Test adding messages to history"""
        history = ConversationHistory()
        history.add("user", "Hello")
        
        assert len(history.history) == 1
        assert history.history[0]["role"] == "user"
        assert history.history[0]["content"] == "Hello"
    
    def test_get_context(self):
        """Test getting conversation context"""
        history = ConversationHistory()
        history.add("user", "Hello")
        history.add("assistant", "Hi there")
        
        context = history.get_context()
        assert "user: Hello" in context
        assert "assistant: Hi there" in context
    
    def test_clear_history(self):
        """Test clearing conversation history"""
        history = ConversationHistory()
        history.add("user", "Hello")
        history.clear()
        
        assert len(history.history) == 0


class TestCodeAnalyzer:
    """Test code analysis functionality"""
    
    def test_detect_python(self):
        """Test Python language detection"""
        code = "def hello():\n    print('Hello')"
        language = CodeAnalyzer.detect_language(code)
        assert language == "python"
    
    def test_detect_javascript(self):
        """Test JavaScript language detection"""
        code = "function hello() { console.log('Hello'); }"
        language = CodeAnalyzer.detect_language(code)
        assert language == "javascript"
    
    def test_extract_context(self):
        """Test code context extraction"""
        code = "def foo():\n    pass"
        context = CodeAnalyzer.extract_context(code)
        
        assert context["language"] == "python"
        assert context["has_functions"] is True
        assert context["line_count"] == 2
    
    def test_detect_indentation(self):
        """Test indentation detection"""
        code = "    def foo():\n        pass"
        indent = CodeAnalyzer.detect_indentation(code)
        assert indent == 4


class TestAIAssistant:
    """Test AI Assistant functionality"""
    
    def test_initialization(self):
        """Test AI assistant initialization"""
        ai = AIAssistant(model_name="test-model")
        assert ai.model_name == "test-model"
        assert ai.conversation is not None
        assert ai.code_analyzer is not None
    
    def test_complete_code(self):
        """Test code completion"""
        ai = AIAssistant()
        code = "def hello"
        result = ai.complete_code(code)
        assert isinstance(result, str)
    
    def test_ask_question(self):
        """Test asking questions"""
        ai = AIAssistant()
        question = "What is Python?"
        result = ai.ask(question)
        assert isinstance(result, str)
    
    def test_reset_conversation(self):
        """Test conversation reset"""
        ai = AIAssistant()
        ai.ask("Hello")
        ai.reset_conversation()
        assert len(ai.conversation.history) == 0
    
    def test_get_conversation_summary(self):
        """Test getting conversation summary"""
        ai = AIAssistant()
        ai.ask("Hello")
        summary = ai.get_conversation_summary()
        
        assert "message_count" in summary
        assert "model" in summary
        assert summary["message_count"] > 0

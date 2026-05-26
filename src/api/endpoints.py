"""
API endpoints for the AI Assistant
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.ai.core import AIAssistant
from src.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["AI Assistant"])

# Initialize AI assistant
ai_assistant = AIAssistant(model_name=settings.MODEL_NAME)


# Request/Response models
class CodeCompletionRequest(BaseModel):
    """Code completion request model"""
    code: str = Field(..., description="Code snippet to complete")
    language: Optional[str] = Field(None, description="Programming language")
    context: Optional[str] = Field(None, description="Additional context")


class CodeCompletionResponse(BaseModel):
    """Code completion response model"""
    original_code: str
    completion: str
    language: str
    confidence: float = 0.85


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message")
    context: Optional[str] = Field(None, description="Additional context")


class ChatResponse(BaseModel):
    """Chat response model"""
    user_message: str
    assistant_response: str
    conversation_length: int


class DebugRequest(BaseModel):
    """Debug request model"""
    error_message: str = Field(..., description="Error message or traceback")
    code: Optional[str] = Field(None, description="Related code snippet")


class DebugResponse(BaseModel):
    """Debug response model"""
    error: str
    suggestions: str
    code_snippet: Optional[str]


class ExplainRequest(BaseModel):
    """Explain request model"""
    code: str = Field(..., description="Code to explain")
    language: Optional[str] = Field(None, description="Programming language")


class ExplainResponse(BaseModel):
    """Explain response model"""
    code: str
    explanation: str
    language: str


# Endpoints
@router.post("/complete", response_model=CodeCompletionResponse)
async def complete_code(request: CodeCompletionRequest):
    """
    Complete code snippet (Copilot-style)
    
    Request body:
    - code: The code snippet to complete
    - language: Programming language (optional, auto-detected)
    - context: Additional context (optional)
    """
    try:
        completion = ai_assistant.complete_code(
            code=request.code,
            language=request.language,
            context=request.context
        )
        
        return CodeCompletionResponse(
            original_code=request.code,
            completion=completion,
            language=request.language or "auto-detected"
        )
    except Exception as e:
        logger.error(f"Error in code completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI (ChatGPT-style)
    
    Request body:
    - message: User's question or message
    - context: Additional context (optional)
    """
    try:
        response = ai_assistant.ask(
            question=request.message,
            context=request.context
        )
        
        summary = ai_assistant.get_conversation_summary()
        
        return ChatResponse(
            user_message=request.message,
            assistant_response=response,
            conversation_length=summary["message_count"]
        )
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debug", response_model=DebugResponse)
async def debug(request: DebugRequest):
    """
    Debug code errors
    
    Request body:
    - error_message: Error message or traceback
    - code: Related code snippet (optional)
    """
    try:
        suggestions = ai_assistant.debug(
            error_message=request.error_message,
            code=request.code or ""
        )
        
        return DebugResponse(
            error=request.error_message,
            suggestions=suggestions,
            code_snippet=request.code
        )
    except Exception as e:
        logger.error(f"Error in debug: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest):
    """
    Explain what code does
    
    Request body:
    - code: Code to explain
    - language: Programming language (optional, auto-detected)
    """
    try:
        explanation = ai_assistant.explain(
            code=request.code,
            language=request.language
        )
        
        return ExplainResponse(
            code=request.code,
            explanation=explanation,
            language=request.language or "auto-detected"
        )
    except Exception as e:
        logger.error(f"Error in explain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_conversation():
    """
    Reset conversation history
    """
    try:
        ai_assistant.reset_conversation()
        return {"status": "success", "message": "Conversation history cleared"}
    except Exception as e:
        logger.error(f"Error resetting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """
    Get AI assistant status
    """
    summary = ai_assistant.get_conversation_summary()
    return {
        "status": "running",
        "model": summary["model"],
        "conversation_messages": summary["message_count"],
        "features": {
            "code_completion": settings.ENABLE_CODE_COMPLETION,
            "chat": settings.ENABLE_CHAT,
            "debugging": settings.ENABLE_DEBUGGING,
            "documentation": settings.ENABLE_DOCUMENTATION
        }
    }

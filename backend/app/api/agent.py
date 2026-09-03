"""Agent chat API for the frontend tray."""

from __future__ import annotations

import json
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.llm.client import get_llm_client
from app.services.portfolio import PortfolioService

router = APIRouter(prefix="/api/agent", tags=["agent"])

SYSTEM_PROMPT = """You are MIDAS, a portfolio analysis assistant for a personal capital management app.
Answer clearly and concisely using the portfolio context JSON when relevant.
Do not invent holdings, prices, or values that are not in the context.
If the context is empty or incomplete, say what is missing.
"""


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)
    reporting_currency: Literal["CAD", "USD"] = "CAD"


class ChatResponse(BaseModel):
    reply: str


def _portfolio_context(db: Session, reporting_currency: str) -> str:
    try:
        summary = PortfolioService(db, reporting_currency=reporting_currency).get_portfolio_summary()
        return json.dumps(summary, default=str)
    except Exception as exc:  # noqa: BLE001
        return json.dumps({"error": f"Could not load portfolio summary: {exc}"})


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    context = _portfolio_context(db, request.reporting_currency)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"Current portfolio context ({request.reporting_currency}):\n{context}",
        },
        *[
            {"role": message.role, "content": message.content}
            for message in request.messages
            if message.role != "system"
        ],
    ]

    try:
        response = get_llm_client().complete(messages)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=502,
            detail=f"Agent model request failed: {exc}",
        ) from exc

    reply = (response.content or "").strip()
    if not reply:
        raise HTTPException(status_code=502, detail="Agent returned an empty reply.")
    return ChatResponse(reply=reply)

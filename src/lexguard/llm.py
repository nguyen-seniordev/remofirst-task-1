
from __future__ import annotations
import os, random
from typing import List, Dict, Any

class BaseLLM:
    def choose_next_intent(self, allowed: List[str], context: Dict[str, Any]) -> str:
        raise NotImplementedError()

    def draft_reply(self, system: str, messages: List[Dict[str, str]], context: Dict[str, Any]) -> str:
        raise NotImplementedError()

class MockLLM(BaseLLM):
    def choose_next_intent(self, allowed: List[str], context: Dict[str, Any]) -> str:
        if not allowed:
            return context.get("fallback_intent", "goodbye")
        # Prefer intents that satisfy required slots, else pick first
        return allowed[0]

    def draft_reply(self, system: str, messages: List[Dict[str, str]], context: Dict[str, Any]) -> str:
        # Very small templated reply for demo
        last_user = next((m["content"] for m in reversed(messages) if m["role"]=="user"), "")
        return f"I understand: '{last_user}'. Proceeding with {context.get('intent','unknown')}."

class OpenAILLM(BaseLLM):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def _client(self):
        try:
            from openai import OpenAI
            return OpenAI()
        except Exception as e:
            raise RuntimeError("OpenAI client not available. Install `openai` and set OPENAI_API_KEY.") from e

    def choose_next_intent(self, allowed: List[str], context: Dict[str, Any]) -> str:
        # For simplicity, pick the first allowed; real impl would score with the LLM
        return allowed[0] if allowed else context.get("fallback_intent", "goodbye")

    def draft_reply(self, system: str, messages: List[Dict[str, str]], context: Dict[str, Any]) -> str:
        client = self._client()
        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}] + messages
        )
        return resp.choices[0].message.content

def make_llm(selector: str) -> BaseLLM:
    if selector.startswith("mock"):
        return MockLLM()
    if selector.startswith("openai"):
        _, _, model = selector.partition(":")
        return OpenAILLM(model=model or "gpt-4o-mini")
    return MockLLM()

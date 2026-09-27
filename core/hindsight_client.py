import logging
import asyncio
from typing import List, Dict, Any
from hindsight_client import Hindsight
from core.config import HINDSIGHT_API_KEY, HINDSIGHT_BASE_URL, HINDSIGHT_BANK_ID

logger = logging.getLogger("hindsight_client")

class MemoryService:
    def __init__(self, bank_id: str = HINDSIGHT_BANK_ID):
        self.bank_id = bank_id
        self.client = Hindsight(
            base_url=HINDSIGHT_BASE_URL,
            api_key=HINDSIGHT_API_KEY
        )
        self._ensure_bank()

    def _ensure_bank(self):
        """Ensure memory bank exists or create it if not present."""
        try:
            self.client.create_bank(
                bank_id=self.bank_id,
                name="DealMind Enterprise Sales Bank",
                mission="Store and organize client procurement constraints, objections, competitor terms, and executive promises.",
            )
            logger.info(f"Memory bank initialized: {self.bank_id}")
        except Exception as e:
            logger.debug(f"Bank check notice: {e}")

    def retain_interaction(self, content: str, context: str = "sales_meeting", document_id: str = None) -> bool:
        """Stores conversation facts, objections, and decisions into Hindsight persistent memory."""
        try:
            self.client.retain(
                bank_id=self.bank_id,
                content=content,
                context=context,
                document_id=document_id
            )
            logger.info("Successfully retained interaction in Hindsight.")
            return True
        except Exception as e:
            logger.error(f"Error retaining to Hindsight: {e}")
            return False

    def recall_context(self, query: str, budget: str = "mid") -> List[Dict[str, Any]]:
        """Recalls relevant past memories and facts based on the user's query."""
        try:
            response = self.client.recall(
                bank_id=self.bank_id,
                query=query,
                budget=budget,
                max_tokens=2048
            )
            memories = []
            if hasattr(response, "results"):
                for r in response.results:
                    memories.append({
                        "text": getattr(r, "text", str(r)),
                        "type": getattr(r, "type", "observation")
                    })
            return memories
        except Exception as e:
            logger.error(f"Error recalling from Hindsight: {e}")
            return []
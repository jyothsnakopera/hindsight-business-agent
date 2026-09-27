import logging
from groq import Groq
from core.config import GROQ_API_KEY, HINDSIGHT_BANK_ID, validate_config
from core.hindsight_client import MemoryService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dealmind_agent")

class DealMindAgent:
    def __init__(self, bank_id: str = HINDSIGHT_BANK_ID):
        validate_config()
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.memory = MemoryService(bank_id=bank_id)
        # Using recommended high-speed reasoning model
        self.model = "openai/gpt-oss-120b"

    def run_turn(self, user_query: str, client_id: str, use_memory: bool = True) -> dict:
        """
        Executes an agent turn.
        - If use_memory is True: recalls past facts, injects into prompt, and retains the turn.
        - If use_memory is False: acts as a baseline stateless model.
        """
        recalled_memories = []
        system_prompt = (
            "You are DealMind, an expert enterprise B2B sales intelligence advisor. "
            "You help sales account executives negotiate deals, handle objections, and avoid "
            "contradicting past agreements or concession boundaries."
        )

        if use_memory:
            # 1. RECALL: Retrieve relevant facts from Hindsight
            recalled_memories = self.memory.recall_context(query=f"Client {client_id}: {user_query}")
            if recalled_memories:
                memory_bullets = "\n".join([f"- {m['text']}" for m in recalled_memories])
                system_prompt += f"\n\nPAST VERIFIED CLIENT KNOWLEDGE (HINDSIGHT PERSISTENT MEMORY):\n{memory_bullets}\n\nUse this past knowledge to guide your response. Explicitly mention prior commitments or constraints when relevant."
            else:
                system_prompt += "\n\n(No prior memories found for this client context yet.)"
        else:
            system_prompt += "\n\n(MODE: STATELESS BASELINE - NO MEMORY ACCESSIBLE. You have zero context of past meetings or agreements.)"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Client ID: {client_id}\nQuery/Scenario: {user_query}"}
        ]

        # 2. INFERENCE via Groq
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.2,
                max_tokens=600
            )
            response_text = chat_completion.choices[0].message.content
        except Exception as e:
            response_text = f"LLM Inference Error: {str(e)}"
            return {
                "response": response_text,
                "recalled_memories": recalled_memories,
                "memory_retained": False
            }

        # # 3. RETAIN: Store exchange to Hindsight if memory mode is enabled
        # retained = False
        # if use_memory:
        #     content_to_save = f"Client {client_id} Interaction:\nUser: {user_query}\nAgent Advice/Outcome: {response_text}"
        #     retained = self.memory.retain_interaction(
        #         content=content_to_save,
        #         context=f"deal_cycle_{client_id}"
        #     )

# 3. RETAIN: Store exchange to Hindsight if memory mode is enabled
        retained = False
        if use_memory and not response_text.startswith("LLM Inference Error"):
            content_to_save = f"Client {client_id} Record:\n- Situation/Query: {user_query}\n- Guidance/Facts: {response_text}"
            retained = self.memory.retain_interaction(
                content=content_to_save,
                context=f"deal_cycle_{client_id}"
            )

        return {
            "response": response_text,
            "recalled_memories": recalled_memories,
            "memory_retained": retained
        }
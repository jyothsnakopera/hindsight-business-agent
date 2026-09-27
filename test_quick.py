from core.agent import DealMindAgent

def main():
    print("Initializing DealMindAgent...")
    agent = DealMindAgent()
    client = "Acme-Corp"

    print("\n--- TURN 1: Retaining Critical Constraint into Memory ---")
    query_1 = "In our meeting today, Acme CFO Sarah stated their hard budget cap is $120,000/year and SOC2 compliance is non-negotiable before Q4."
    res1 = agent.run_turn(query_1, client_id=client, use_memory=True)
    print(f"Memory Retained: {res1['memory_retained']}")
    print(f"Agent Response:\n{res1['response']}")

    print("\n--- TURN 2 (No Memory Baseline): Asking About Budget ---")
    res_baseline = agent.run_turn("Can we pitch them a $160,000 package for next quarter?", client_id=client, use_memory=False)
    print(f"Recalled: {len(res_baseline['recalled_memories'])} memories")
    print(f"Baseline Response:\n{res_baseline['response']}")

    print("\n--- TURN 3 (Hindsight Memory Enabled): Asking the same question ---")
    res_memory = agent.run_turn("Can we pitch them a $160,000 package for next quarter?", client_id=client, use_memory=True)
    print(f"Recalled: {len(res_memory['recalled_memories'])} memories")
    for mem in res_memory['recalled_memories']:
        print(f"  * Recalled Memory: {mem['text']}")
    print(f"\nMemory-Enabled Response:\n{res_memory['response']}")

if __name__ == "__main__":
    main()
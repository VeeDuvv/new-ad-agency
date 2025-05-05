# import DirectorAgent

from backend.agents.openai.director_agent import DirectorAgent

def test_director():
    agent = DirectorAgent()
    inp = {
      "client_brief": "Test campaign for AI‑powered ad agency.",
      "goals": "Validate end‑to‑end flow",
      "budget": "1",
      "KPIs": ["test"],
      "framework": "APQC"
    }
    pkg = agent.run(inp)
    print("DirectorAgent output keys:", pkg.keys())

if __name__ == "__main__":
    test_director()

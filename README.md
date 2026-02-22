# Agentic-AI 🚀

Agentic-AI is an experimental repository focused on building **agent-driven workflows** using **LangFlow**, **LLMs**, and structured agent specifications.  
This project demonstrates how an AI agent can **analyze a word-search puzzle from an image**, detect words in multiple directions, and visually represent results with correct and incorrect matches.

---

## 📂 Repository Structure
Agentic-AI/
│
├── word-search-langflow/
│ ├── AgentSpec.md
│ ├── Interaction.md
│ ├── agent_prompt.txt
│ ├── word_search.json
│ ├── main.py
│ └── README.md
│
└── README.md


---

## 🧠 Project Overview: Word Search Agent

The **Word Search Agent** is designed to:

- Parse a **grid-based word search puzzle**
- Match words in **all 8 possible directions**
  - Horizontal (→ ←)
  - Vertical (↓ ↑)
  - Diagonal (↘ ↗ ↙ ↖)
- Handle:
  - ✅ Multiple correct matches
  - ❌ Not found words
- Visually highlight results using **different colors**
- Clearly separate:
  - Found words
  - Not found words (displayed after the grid)

---

## 📄 Key Files Explained

### `AgentSpec.md`
Defines the agent’s:
- Role
- Goals
- Constraints
- Expected outputs

---

### `Interaction.md`
Describes:
- Agent reasoning steps
- Input → processing → output flow
- Decision logic for found vs not found words

---

### `agent_prompt.txt`
Contains the **system + task prompt** used by the LLM, including:
- Grid parsing rules
- Matching logic
- Output formatting requirements

---

### `word_search.json`
Structured input data:
```json
{
  "grid": [
    ["B","E","D","R","O","O","M"],
    ["H","O","L","L","O","W","P"],
    ["P","I","P","E","X","X","X"]
  ],
  "words": ["BEDROOM", "HOLLOWPIPE"]
}


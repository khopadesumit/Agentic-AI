# Agent Specification Document
## Word Search Puzzle Solver — DataStax Langflow

---

## 1. System Overview

The Word Search Puzzle Solver is a multi-agent system built using DataStax Langflow.  
It processes word search puzzle images, extracts a letter grid using a vision model, parses the grid deterministically, and solves the puzzle using a reliable algorithmic word-search engine.

The system strictly separates AI-based OCR from deterministic logic to prevent hallucination.

---

## 2. Agent Architecture

Chat Input (Image)  
→ OCR Vision Agent  
→ Grid Parser (Custom Component)  
→ Word Search Solver (Custom Component)  
→ Chat Output (HTML)

---

## 3. Agent Specifications

### Agent 1: OCR Vision Agent

**Type:** Built-in Vision Agent  
**Provider:** Groq / Google Gemini  
**Model:** meta-llama/llama-4-maverick-vision  
**Role:** Extract letter grid from puzzle image  
**Input:** Image (JPG / PNG / URL)  
**Output:** Plain text grid  
**Autonomy:** Fully autonomous  

#### Prompt
Extract ONLY the letter grid from the word search puzzle image.
Each row must be on a new line.
Letters must be separated by single spaces.
ALL letters must be uppercase.
No explanations, headers, or extra text.

---

### Agent 2: Grid Parser (Custom Component)

**Type:** Custom Langflow Component  
**Role:** Convert OCR text into a structured 2D grid  
**Autonomy:** Deterministic  

#### Responsibilities
- Split OCR text by lines
- Extract alphabetic characters only
- Handle space-separated and continuous text
- Normalize to uppercase
- Preserve per-row column length

---

### Agent 3: Word Search Solver (Custom Component)

**Type:** Custom Langflow Component  
**Role:** Find words in grid and generate highlighted HTML output  
**Autonomy:** Deterministic  

#### Algorithm
- Brute-force scan
- All cells × 8 directions
- Early exit on match
- Overlap-safe highlighting

#### Directions
→ ← ↓ ↑ ↘ ↙ ↗ ↖

---

## 4. Inter-Agent Communication

| From | To | Data |
|----|----|-----|
| Chat Input | OCR Agent | Image |
| OCR Agent | Grid Parser | Text |
| Grid Parser | Solver | Structured Grid |
| Solver | Chat Output | HTML |

---

## 5. Error Handling

- Invalid grid → "Invalid grid"
- Uneven rows → row-aware bounds checking
- Word not found → explicitly listed
- OCR errors → partial grid tolerated

---

## 6. Design Principles

- AI only for OCR
- No LLM solving
- Deterministic correctness
- Visual clarity for overlaps
- Explicit NOT FOUND results

---

## 7. Status

Production-ready  
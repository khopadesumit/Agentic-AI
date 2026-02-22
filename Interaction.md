# Interaction Flow Documentation
## Word Search Puzzle Solver

---

## 1. User Interaction Flow

1. User uploads or provides an image of a word search puzzle
2. User enters one or more words to find (comma or newline separated)
3. User clicks Run in Langflow Playground
4. System processes and returns:
   - Highlighted grid
   - Found words
   - Not found words

---

## 2. Step-by-Step Execution

### Step 1: Chat Input
- Accepts image input
- Accepts word list input

### Step 2: OCR Vision Agent
- Reads the image
- Extracts only the grid letters
- Outputs clean uppercase text

### Step 3: Grid Parser
- Validates OCR output
- Builds 2D grid
- Normalizes letters
- Parses word list

### Step 4: Word Search Solver
- Searches all words
- Assigns colors dynamically
- Handles overlaps safely
- Builds HTML output

### Step 5: Chat Output
- Displays grid as HTML table
- Highlights words
- Lists found and not found words

---

## 3. User Input Rules

- Words must be alphabetic
- Minimum length: 3
- No spaces inside a word
- Case-insensitive input

---

## 4. Output Rules

- Each found word has a unique color
- Overlapping cells show gradient background
- Not found words always appear in result section

---

## 5. Failure Scenarios

| Case | Result |
|----|------|
| Empty image | Empty grid |
| OCR noise | Partial grid |
| Word missing | Listed in NOT FOUND |
| Invalid grid | Error message |

---

## 6. UX Goals

- No silent failures
- Visual correctness
- Deterministic results
- Easy debugging
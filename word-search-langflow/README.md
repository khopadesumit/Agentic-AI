# Word Search Puzzle Solver — Langflow

A deterministic word search puzzle solver built using DataStax Langflow.

## Features
- OCR-based grid extraction
- Deterministic word search (no hallucination)
- Overlap-safe highlighting
- Explicit NOT FOUND reporting
- Production-ready custom components

## Architecture
Image → OCR → Grid Parser → Word Search Solver → HTML Output

## Requirements
- Python 3.10+
- DataStax Langflow

## Usage
1. Import components into Langflow
2. Connect OCR → Parser → Solver
3. Provide image + word list
4. Run flow

## Status
Production-ready
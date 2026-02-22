from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Message
import json
import re
from collections import defaultdict


class WordGridFinderComponent(Component):
    display_name = "Word Grid Finder"
    description = "Reliable word search with overlap-safe highlighting"
    icon = "grid-3x3"

    inputs = [
        MessageTextInput(
            name="grid_text",
            display_name="Grid (JSON or Plain Text)",
        ),
        MessageTextInput(
            name="word_list",
            display_name="Words (comma or newline separated)",
        ),
    ]

    outputs = [
        Output(
            name="html_output",
            display_name="HTML Output",
            type=Message,
            method="find_words",
        )
    ]

    # ---------------- SAFE TEXT EXTRACTION ----------------
    def get_text(self, value):
        if hasattr(value, "text"):
            return value.text
        return str(value)

    # ---------------- COLOR PALETTE ----------------
    def color_palette(self):
        return [
            "#FFD966", "#A4C2F4", "#B6D7A8", "#F4CCCC",
            "#D5A6BD", "#FFE599", "#9FC5E8", "#EAD1DC",
            "#B4A7D6", "#C9DAF8"
        ]

    # ---------------- ROBUST GRID PARSER ----------------
    def parse_grid(self, text):
        # Try JSON first
        try:
            grid = json.loads(text)
            if isinstance(grid, list):
                return [[str(c).upper() for c in row] for row in grid]
        except Exception:
            pass

        grid = []

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            line = line.replace("\t", " ")
            cells = [c.strip() for c in line.split(" ") if c.strip()]

            # Keep only valid letter rows
            if len(cells) > 3 and all(len(c) == 1 and c.isalpha() for c in cells):
                grid.append([c.upper() for c in cells])

        return grid

    # ---------------- WORD SEARCH ----------------
    def find_word(self, grid, word):
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    rr, cc = r, c
                    positions = []

                    for ch in word:
                        if (
                            0 <= rr < rows and
                            0 <= cc < cols and
                            grid[rr][cc] == ch
                        ):
                            positions.append((rr, cc))
                            rr += dr
                            cc += dc
                        else:
                            break

                    if len(positions) == len(word):
                        return positions

        return None

    # ---------------- MAIN FUNCTION ----------------
    def find_words(self) -> Message:
        grid_text = self.get_text(self.grid_text)
        word_text = self.get_text(self.word_list)

        grid = self.parse_grid(grid_text)

        if not grid:
            return Message(text="<b style='color:red'>Invalid grid</b>")

        # ---------------- SANITIZE WORD INPUT ----------------
        raw_parts = re.split(r"[,\n]", word_text)

        words = list(dict.fromkeys(
            w.strip().upper()
            for w in raw_parts
            if (
                w.strip()
                and w.strip().isalpha()
                and " " not in w.strip()
                and len(w.strip()) >= 3
            )
        ))

        palette = self.color_palette()
        found = {}
        not_found = []
        cell_colors = defaultdict(list)

        for word in words:
            positions = self.find_word(grid, word)

            if positions is not None and len(positions) > 0:
                color = palette[len(found) % len(palette)]
                found[word] = color
                for pos in positions:
                    cell_colors[pos].append(color)
            else:
                not_found.append(word)

        # ---------------- BUILD HTML ----------------
        html = "<table style='border-collapse:collapse;font-family:monospace;'>"

        for r, row in enumerate(grid):
            html += "<tr>"
            for c, ch in enumerate(row):
                colors = cell_colors.get((r, c))
                style = ""

                if colors:
                    if len(colors) == 1:
                        style = f"background:{colors[0]};"
                    else:
                        style = "background:linear-gradient(135deg," + ",".join(colors) + ");"

                html += f"<td style='border:1px solid #333;padding:4px;{style}'>{ch}</td>"

            html += "</tr>"

        html += "</table>"

        # Found words
        if found:
            html += "<p><b>Found words:</b></p><ul>"
            for word, color in found.items():
                html += f"<li style='color:{color}'>{word}</li>"
            html += "</ul>"

        # Not found words
        if not_found:
            html += "<p><b>Not found:</b></p><ul>"
            for word in not_found:
                html += f"<li style='color:red'>{word}</li>"
            html += "</ul>"

        return Message(text=html)
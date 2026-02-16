"""Regex-based filler word removal and text formatting."""

from __future__ import annotations

import re


# Filler words/phrases to remove (case-insensitive, word-boundary matched)
_FILLERS = [
    r"\bum\b",
    r"\buh\b",
    r"\buh huh\b",
    r"\bmm\b",
    r"\bhmm\b",
    r"\bmhm\b",
    r"\byou know\b",
    r"\bi mean\b",
    r"\bkind of\b",
    r"\bsort of\b",
    r"\bbasically\b",
    r"\bliterally\b",
    r"\bokay so\b",
    r"\byeah\b",
]

_FILLER_PATTERN = re.compile(
    "|".join(_FILLERS),
    re.IGNORECASE,
)

# Conjunctions that typically need a comma before them when joining clauses.
# Requires 3+ word chars before the conjunction to avoid "So ," at sentence starts.
_COMMA_BEFORE_CONJ = re.compile(
    r"(?<=[a-z]{3})(\s+)(but|and|so|yet|or|because|since|although|though|while)\s",
    re.IGNORECASE,
)


class RegexProcessor:
    """Removes filler words and cleans up transcription output."""

    def process(self, text: str) -> str:
        if not text or not text.strip():
            return ""

        result = _FILLER_PATTERN.sub("", text)

        # Collapse multiple spaces
        result = re.sub(r"\s{2,}", " ", result).strip()

        # Remove leading/trailing commas and spaces left by filler removal
        result = re.sub(r"(^[,\s]+|[,\s]+$)", "", result)
        result = re.sub(r"\s*,\s*,\s*", ", ", result)
        result = re.sub(r"^\s*,\s*", "", result)

        # Add commas before conjunctions joining clauses (if not already there)
        result = _COMMA_BEFORE_CONJ.sub(r", \2 ", result)

        # Clean up double commas or space-comma artifacts
        result = re.sub(r"\s+,", ",", result)
        result = re.sub(r",\s*,", ",", result)

        # Fix capitalization after commas: lowercase words after commas (mid-sentence)
        # This fixes ", So" and ", And" artifacts
        result = re.sub(
            r",\s+([A-Z])([a-z]+)(?!\s+[A-Z])",
            lambda m: ", " + m.group(1).lower() + m.group(2),
            result,
        )

        # Capitalize after sentence-ending punctuation
        result = re.sub(
            r"([.!?])\s+([a-z])",
            lambda m: m.group(1) + " " + m.group(2).upper(),
            result,
        )

        # Capitalize first letter
        if result:
            result = result[0].upper() + result[1:]

        # Ensure trailing period if no sentence-ending punctuation
        if result and result[-1] not in ".!?":
            result += "."

        return result

"""Reusable MCP prompts for PyVoicing music-theory workflows."""
from __future__ import annotations

from typing import Any


def analyze_voicing(pitches: str, root: str) -> list[dict[str, Any]]:
    """Prompt: Analyze a chord voicing and identify its chord tones.

    Args:
        pitches: Space-separated pitch strings, e.g. ``"C4 E4 G4 B4"``.
        root: Root chroma for analysis, e.g. ``"C"``.

    Returns:
        A list of MCP message dicts.
    """
    return [
        {
            "role": "user",
            "content": (
                f"Analyze the following chord voicing with root {root!r}:\n\n"
                f"Pitches: {pitches}\n\n"
                "Please identify:\n"
                "1. The chord tones (e.g. root, third, fifth, seventh, extensions)\n"
                "2. The chord quality and chord symbol\n"
                "3. Any tensions or color tones\n"
                "4. The voicing type (close, open, drop-2, etc.)\n\n"
                "Use the `voicing_tones` tool to get structured analysis data."
            ),
        }
    ]


def explain_pitch_spelling(pitch: str) -> list[dict[str, Any]]:
    """Prompt: Explain the enharmonic spelling choices for a pitch.

    Args:
        pitch: Pitch string, e.g. ``"C#4"`` or ``"Db4"``.

    Returns:
        A list of MCP message dicts.
    """
    return [
        {
            "role": "user",
            "content": (
                f"Explain the enharmonic spelling for the pitch {pitch!r}.\n\n"
                "Please cover:\n"
                "1. Both flat and sharp spellings (e.g. Db4 vs C#4)\n"
                "2. In which musical contexts each spelling is preferred\n"
                "3. Any functional differences (e.g. in different key signatures)\n\n"
                "Use the `pitch_spell` tool to retrieve both spellings."
            ),
        }
    ]


def suggest_chord_tones(pitches: str, root: str) -> list[dict[str, Any]]:
    """Prompt: Suggest chord-tone interpretation for a set of pitches given a root.

    Args:
        pitches: Space-separated pitch strings.
        root: Proposed root chroma.

    Returns:
        A list of MCP message dicts.
    """
    return [
        {
            "role": "user",
            "content": (
                f"Given root {root!r} and pitches {pitches!r}, suggest how to\n"
                "interpret these pitches as chord tones.\n\n"
                "Include:\n"
                "1. The scale degrees / chord-tone labels for each pitch\n"
                "2. A likely chord symbol\n"
                "3. Alternative root interpretations (slash chords, modes)\n\n"
                "Use the `voicing_tones` tool for analysis."
            ),
        }
    ]


def convert_voicing_description(pitches: str, root: str) -> list[dict[str, Any]]:
    """Prompt: Convert a voicing to a symbolic chord description and back.

    Args:
        pitches: Space-separated pitch strings.
        root: Root chroma.

    Returns:
        A list of MCP message dicts.
    """
    return [
        {
            "role": "user",
            "content": (
                f"Convert the voicing {pitches!r} (root: {root!r}) between\n"
                "representations:\n\n"
                "1. Identify the chord symbol (e.g. Cmaj7, G13, Dm7b5)\n"
                "2. List the chord tones in Roman-numeral / jazz notation\n"
                "3. Describe any reharmonization or substitution possibilities\n"
                "4. Suggest an alternative voicing (e.g. drop-2, rootless)\n\n"
                "Use `voicing_tones`, `voicing_drop2`, and `voicing_parse` as needed."
            ),
        }
    ]

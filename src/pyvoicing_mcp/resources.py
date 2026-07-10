"""MCP resources for PyVoicing: README, changelog, constants reference, API map."""
from __future__ import annotations

import importlib.resources
import json
from pathlib import Path

from pyvoicing.constants import CHROMA_OF, INTERVAL_OF, OFFSET_OF

# Resolve the package root (two parents up from this file)
_PKG_ROOT = Path(__file__).resolve().parents[2]
_README_PATH = _PKG_ROOT / "README.md"
_CHANGELOG_PATH = _PKG_ROOT / "CHANGELOG.md"


def get_readme() -> str:
    """Return the contents of the project README."""
    if _README_PATH.exists():
        return _README_PATH.read_text(encoding="utf-8")
    return "README not found."


def get_changelog() -> str:
    """Return the contents of the project CHANGELOG."""
    if _CHANGELOG_PATH.exists():
        return _CHANGELOG_PATH.read_text(encoding="utf-8")
    return "CHANGELOG not found."


def get_chroma_constants() -> str:
    """Return a JSON view of the chroma offset → name mapping."""
    data = {str(k): v for k, v in CHROMA_OF.items() if isinstance(k, int)}
    return json.dumps(data, indent=2)


def get_interval_constants() -> str:
    """Return a JSON view of the interval offset → name mapping."""
    data = {str(k): v for k, v in INTERVAL_OF.items() if isinstance(k, int)}
    return json.dumps(data, indent=2)


def get_offset_constants() -> str:
    """Return a JSON view of the name → offset mapping (excluding Rest keys)."""
    data = {k: v for k, v in OFFSET_OF.items() if isinstance(k, str) and isinstance(v, int)}
    return json.dumps(data, indent=2)


_API_QUICK_REFERENCE = """\
# PyVoicing API Quick Reference

## Pitch
- `Pitch(value, octave=4)` – create from MIDI int, string (e.g. "C4"), Chroma, or Pitch
- `.name` – chroma name respecting `Spelling.prefer_flat`
- `.octave` – octave number (C4 = octave 4)
- `.offset` – semitone offset within octave (0-11)
- `.midi` / `~pitch` – MIDI integer value
- `.freq` – frequency in Hz (A4 = 440 Hz)
- `.abc` / `.lilypond` – notation strings
- `.spell(prefer_flat)` – force a specific spelling
- `.enharmonic` – opposite spelling
- `.transpose(interval)` / `>>` – transpose up
- `.transpose_down(interval)` / `<<` – transpose down
- `.distance_to(other)` – returns Interval

## Chroma
- `Chroma(value)` – pitch class without octave
- `.offset` – semitone offset (0-11)
- `.spell(prefer_flat)` / `.enharmonic` – spelling helpers
- `.transpose(interval)` / `.transpose_down(interval)` – returns Chroma
- `.distance_to(other)` – returns Interval (modulo 12)

## Interval
- `Interval(value, octave=0)` – create from int (semitones), string (e.g. "M3"), or Chroma
- `.distance` – total semitone distance
- `.offset` – semitone within octave
- `.octave` – octave component
- `.interval` – name string (e.g. "M3")
- `.add(other)` / `.subtract(other)` – arithmetic

## Voicing
- `Voicing(pitches, root=None)` – list of pitches with optional root chroma
- `.pitches` – list of Pitch objects
- `.root` – Chroma or None
- `.tones` – chord-tone labels relative to root (e.g. ["1", "maj3", "5"])
- `.spell(prefer_flat)` – list of pitch name strings
- `.transpose(interval)` / `>>` – transpose entire voicing
- `.transpose_down(interval)` / `<<` – transpose entire voicing down
- `.add(pitch)` / `+` – add pitch, returns new Voicing
- `.remove(pitch)` / `-` – remove pitch, returns new Voicing
- `.find_interval(interval)` / `%` – find lower pitches forming interval
- `.to_root(target)` / `//` – move voicing so root lands on target
- `.drop2`, `.drop3`, `.drop24` – closed → open voicing transforms (4-note only)
- `~voicing` – list of MIDI values

## Spelling
- `Spelling.prefer_flat = True|False` – global flat/sharp preference

## Constants
- `CHROMA_OF` – offset (int) → chroma name (flat)
- `INTERVAL_OF` – offset (int) → interval name
- `OFFSET_OF` – name (str) → offset (int)
- `ABC_OF` – offset (int) → ABC notation string
"""


def get_api_reference() -> str:
    """Return a compact API quick-reference for PyVoicing."""
    return _API_QUICK_REFERENCE

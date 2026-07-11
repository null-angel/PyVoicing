"""Serialization helpers: convert PyVoicing objects to JSON-friendly dicts."""
from __future__ import annotations

from typing import Any

from pyvoicing import Chroma, Interval, Pitch, Voicing
from pyvoicing.rest import Rest


def pitch_to_dict(p: Pitch) -> dict[str, Any]:
    """Convert a Pitch to a JSON-serializable dict."""
    if isinstance(p.value, Rest):
        return {"type": "rest"}
    return {
        "name": p.name,
        "octave": p.octave,
        "midi": p.value,
        "offset": p.offset,
        "freq": p.freq,
    }


def chroma_to_dict(c: Chroma) -> dict[str, Any]:
    """Convert a Chroma to a JSON-serializable dict."""
    return {
        "name": str(c),
        "offset": c.offset,
    }


def interval_to_dict(i: Interval) -> dict[str, Any]:
    """Convert an Interval to a JSON-serializable dict."""
    return {
        "name": str(i),
        "interval": i.interval,
        "octave": i.octave,
        "distance": i.distance,
    }


def voicing_to_dict(v: Voicing) -> dict[str, Any]:
    """Convert a Voicing to a JSON-serializable dict."""
    return {
        "pitches": [pitch_to_dict(p) for p in v],
        "root": str(v.root) if v.root is not None else None,
        "midi": ~v,
        "spell": v.spell(),
    }

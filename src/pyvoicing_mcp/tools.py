"""MCP tools wrapping the PyVoicing public API."""
from __future__ import annotations

from typing import Any, Optional

from pyvoicing import (
    Chroma,
    Interval,
    Pitch,
    Voicing,
)
from pyvoicing.spelling import Spelling

from .serializers import (
    chroma_to_dict,
    interval_to_dict,
    pitch_to_dict,
    voicing_to_dict,
)


# ---------------------------------------------------------------------------
# Pitch tools
# ---------------------------------------------------------------------------


def pitch_parse(pitch: str, prefer_flat: bool = True) -> dict[str, Any]:
    """Parse a pitch string and return its properties.

    Args:
        pitch: Pitch string, e.g. ``"C4"``, ``"Eb5"``, ``"F#3"``.
        prefer_flat: Use flat spelling for enharmonic names (default True).

    Returns:
        Dict with ``name``, ``octave``, ``midi``, ``offset``, ``freq``,
        ``abc``, ``lilypond``, and ``enharmonic`` keys.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        p = Pitch(pitch)
        result = pitch_to_dict(p)
        if result.get("type") != "rest":
            result["abc"] = p.abc
            result["lilypond"] = p.lilypond
            result["enharmonic"] = p.enharmonic
        return result
    except Exception as exc:
        raise ValueError(f"Cannot parse pitch {pitch!r}: {exc}") from exc
    finally:
        Spelling.prefer_flat = prev


def pitch_transpose(
    pitch: str,
    interval: str,
    direction: str = "up",
    prefer_flat: bool = True,
) -> dict[str, Any]:
    """Transpose a pitch by an interval.

    Args:
        pitch: Source pitch, e.g. ``"C4"``.
        interval: Interval to transpose by, e.g. ``"M3"``, ``"P5"``, ``"12"`` (semitones).
        direction: ``"up"`` (default) or ``"down"``.
        prefer_flat: Use flat spelling for enharmonic names.

    Returns:
        Dict describing the transposed pitch.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        p = Pitch(pitch)
        i = Interval(interval) if not interval.lstrip("-").isdigit() else Interval(int(interval))
        result = p.transpose(i) if direction == "up" else p.transpose_down(i)
        out = pitch_to_dict(result)
        if out.get("type") != "rest":
            out["abc"] = result.abc
            out["lilypond"] = result.lilypond
        return out
    except Exception as exc:
        raise ValueError(
            f"Cannot transpose pitch {pitch!r} by {interval!r}: {exc}"
        ) from exc
    finally:
        Spelling.prefer_flat = prev


def pitch_distance(pitch_a: str, pitch_b: str) -> dict[str, Any]:
    """Return the interval distance from pitch_a to pitch_b.

    Args:
        pitch_a: Source pitch, e.g. ``"C4"``.
        pitch_b: Target pitch, e.g. ``"E4"``.

    Returns:
        Dict describing the interval between the two pitches.
    """
    try:
        a = Pitch(pitch_a)
        b = Pitch(pitch_b)
        return interval_to_dict(a.distance_to(b))
    except Exception as exc:
        raise ValueError(
            f"Cannot compute distance from {pitch_a!r} to {pitch_b!r}: {exc}"
        ) from exc


def pitch_spell(pitch: str, prefer_flat: Optional[bool] = None) -> dict[str, Any]:
    """Return both flat and sharp spellings of a pitch.

    Args:
        pitch: Pitch string, e.g. ``"C#4"``.
        prefer_flat: If provided, selects the spelling to use for the ``name``
            field; both spellings are always included.

    Returns:
        Dict with ``flat``, ``sharp``, and ``name`` keys.
    """
    try:
        p = Pitch(pitch)
        flat = p.spell(prefer_flat=True)
        sharp = p.spell(prefer_flat=False)
        name = p.spell(prefer_flat=prefer_flat) if prefer_flat is not None else p.name
        return {"flat": flat, "sharp": sharp, "name": name}
    except Exception as exc:
        raise ValueError(f"Cannot spell pitch {pitch!r}: {exc}") from exc


def pitch_notation(pitch: str, prefer_flat: bool = True) -> dict[str, Any]:
    """Return a pitch in multiple notations.

    Args:
        pitch: Pitch string.
        prefer_flat: Use flat spelling for enharmonic names.

    Returns:
        Dict with ``scientific`` (e.g. ``"C4"``), ``abc``, and ``lilypond`` keys.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        p = Pitch(pitch)
        return {
            "scientific": str(p),
            "abc": p.abc,
            "lilypond": p.lilypond,
        }
    except Exception as exc:
        raise ValueError(f"Cannot get notation for pitch {pitch!r}: {exc}") from exc
    finally:
        Spelling.prefer_flat = prev


# ---------------------------------------------------------------------------
# Chroma tools
# ---------------------------------------------------------------------------


def chroma_transpose(
    chroma: str,
    interval: str,
    direction: str = "up",
    prefer_flat: bool = True,
) -> dict[str, Any]:
    """Transpose a chroma (pitch class) by an interval.

    Args:
        chroma: Chroma name, e.g. ``"C"``, ``"Eb"``, ``"F#"``.
        interval: Interval name or semitone count.
        direction: ``"up"`` (default) or ``"down"``.
        prefer_flat: Use flat spelling for the result.

    Returns:
        Dict describing the transposed chroma.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        c = Chroma(chroma)
        i = Interval(interval) if not interval.lstrip("-").isdigit() else Interval(int(interval))
        result = c.transpose(i) if direction == "up" else c.transpose_down(i)
        return chroma_to_dict(result)
    except Exception as exc:
        raise ValueError(
            f"Cannot transpose chroma {chroma!r} by {interval!r}: {exc}"
        ) from exc
    finally:
        Spelling.prefer_flat = prev


def chroma_distance(chroma_a: str, chroma_b: str) -> dict[str, Any]:
    """Return the interval distance from chroma_a to chroma_b (modulo 12).

    Args:
        chroma_a: Source chroma name.
        chroma_b: Target chroma name.

    Returns:
        Dict describing the interval.
    """
    try:
        a = Chroma(chroma_a)
        b = Chroma(chroma_b)
        return interval_to_dict(a.distance_to(b))
    except Exception as exc:
        raise ValueError(
            f"Cannot compute distance from {chroma_a!r} to {chroma_b!r}: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# Interval tools
# ---------------------------------------------------------------------------


def interval_parse(interval: str) -> dict[str, Any]:
    """Parse an interval string and return its properties.

    Args:
        interval: Interval name (e.g. ``"M3"``, ``"P5"``) or integer semitone
            count (e.g. ``"14"``).

    Returns:
        Dict with ``name``, ``interval``, ``octave``, and ``distance`` keys.
    """
    try:
        i = Interval(interval) if not interval.lstrip("-").isdigit() else Interval(int(interval))
        return interval_to_dict(i)
    except Exception as exc:
        raise ValueError(f"Cannot parse interval {interval!r}: {exc}") from exc


def interval_add(interval_a: str, interval_b: str) -> dict[str, Any]:
    """Add two intervals together.

    Args:
        interval_a: First interval.
        interval_b: Second interval.

    Returns:
        Dict describing the resulting interval.
    """
    try:
        a = Interval(interval_a) if not interval_a.lstrip("-").isdigit() else Interval(int(interval_a))
        b = Interval(interval_b) if not interval_b.lstrip("-").isdigit() else Interval(int(interval_b))
        return interval_to_dict(a.add(b))
    except Exception as exc:
        raise ValueError(
            f"Cannot add intervals {interval_a!r} and {interval_b!r}: {exc}"
        ) from exc


def interval_subtract(interval_a: str, interval_b: str) -> dict[str, Any]:
    """Subtract interval_b from interval_a.

    Args:
        interval_a: Minuend interval.
        interval_b: Subtrahend interval.

    Returns:
        Dict describing the resulting interval.
    """
    try:
        a = Interval(interval_a) if not interval_a.lstrip("-").isdigit() else Interval(int(interval_a))
        b = Interval(interval_b) if not interval_b.lstrip("-").isdigit() else Interval(int(interval_b))
        return interval_to_dict(a.subtract(b))
    except Exception as exc:
        raise ValueError(
            f"Cannot subtract {interval_b!r} from {interval_a!r}: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# Voicing tools
# ---------------------------------------------------------------------------


def voicing_parse(pitches: str, root: Optional[str] = None) -> dict[str, Any]:
    """Parse a space-separated pitch list into a voicing.

    Args:
        pitches: Space-separated pitch strings, e.g. ``"C4 E4 G4 B4"``.
        root: Optional root chroma, e.g. ``"C"``.

    Returns:
        Dict describing the voicing.
    """
    try:
        v = Voicing(pitches, root=root)
        return voicing_to_dict(v)
    except Exception as exc:
        raise ValueError(f"Cannot parse voicing {pitches!r}: {exc}") from exc


def voicing_transpose(
    pitches: str,
    interval: str,
    root: Optional[str] = None,
    direction: str = "up",
    prefer_flat: bool = True,
) -> dict[str, Any]:
    """Transpose a voicing by an interval.

    Args:
        pitches: Space-separated pitch strings.
        interval: Interval name or semitone count.
        root: Optional root chroma.
        direction: ``"up"`` (default) or ``"down"``.
        prefer_flat: Use flat spelling for the result.

    Returns:
        Dict describing the transposed voicing.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        v = Voicing(pitches, root=root)
        i = Interval(interval) if not interval.lstrip("-").isdigit() else Interval(int(interval))
        result = v.transpose(i) if direction == "up" else v.transpose_down(i)
        return voicing_to_dict(result)
    except Exception as exc:
        raise ValueError(
            f"Cannot transpose voicing {pitches!r} by {interval!r}: {exc}"
        ) from exc
    finally:
        Spelling.prefer_flat = prev


def voicing_add(pitches: str, add_pitch: str, root: Optional[str] = None) -> dict[str, Any]:
    """Add a pitch to a voicing.

    Args:
        pitches: Space-separated pitch strings.
        add_pitch: Pitch to add, e.g. ``"B4"``.
        root: Optional root chroma.

    Returns:
        Dict describing the updated voicing.
    """
    try:
        v = Voicing(pitches, root=root)
        result = v.add(Pitch(add_pitch))
        return voicing_to_dict(result)
    except Exception as exc:
        raise ValueError(
            f"Cannot add pitch {add_pitch!r} to voicing {pitches!r}: {exc}"
        ) from exc


def voicing_remove(
    pitches: str, remove_pitch: str, root: Optional[str] = None
) -> dict[str, Any]:
    """Remove a pitch from a voicing.

    Args:
        pitches: Space-separated pitch strings.
        remove_pitch: Pitch to remove, e.g. ``"E4"``.
        root: Optional root chroma.

    Returns:
        Dict describing the updated voicing.
    """
    try:
        v = Voicing(pitches, root=root)
        result = v.remove(remove_pitch)
        return voicing_to_dict(result)
    except Exception as exc:
        raise ValueError(
            f"Cannot remove pitch {remove_pitch!r} from voicing {pitches!r}: {exc}"
        ) from exc


def voicing_find_interval(
    pitches: str, interval: str, root: Optional[str] = None
) -> dict[str, Any]:
    """Find pitches in a voicing that form a given interval with a higher pitch.

    Args:
        pitches: Space-separated pitch strings.
        interval: Interval name or semitone count to search for.
        root: Optional root chroma.

    Returns:
        Dict with ``lower_pitches`` (list of pitch dicts) and ``interval`` keys.
    """
    try:
        v = Voicing(pitches, root=root)
        i = Interval(interval) if not interval.lstrip("-").isdigit() else Interval(int(interval))
        lowers = v.find_interval(i)
        return {
            "lower_pitches": [pitch_to_dict(p) for p in lowers],
            "interval": interval_to_dict(i),
        }
    except Exception as exc:
        raise ValueError(
            f"Cannot find interval {interval!r} in voicing {pitches!r}: {exc}"
        ) from exc


def voicing_to_root(
    pitches: str,
    target: str,
    root: Optional[str] = None,
    prefer_flat: bool = True,
) -> dict[str, Any]:
    """Transpose a voicing so its root lands on the target pitch.

    Args:
        pitches: Space-separated pitch strings.
        target: Target pitch for the root, e.g. ``"C4"``.
        root: Root chroma of the voicing (required for this operation).
        prefer_flat: Use flat spelling for the result.

    Returns:
        Dict describing the transposed voicing.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        if root is None:
            raise ValueError("root is required for voicing_to_root")
        v = Voicing(pitches, root=root)
        target_pitch = Pitch(target)
        result = v.to_root(target_pitch)
        return voicing_to_dict(result)
    except Exception as exc:
        raise ValueError(
            f"Cannot move voicing {pitches!r} to root {target!r}: {exc}"
        ) from exc
    finally:
        Spelling.prefer_flat = prev


def voicing_tones(pitches: str, root: str) -> dict[str, Any]:
    """Analyze the chord tones of a voicing relative to its root.

    Args:
        pitches: Space-separated pitch strings.
        root: Root chroma for analysis, e.g. ``"C"``.

    Returns:
        Dict with ``tones`` (list of tone labels) and voicing info.
    """
    try:
        v = Voicing(pitches, root=root)
        tones = v.tones
        result = voicing_to_dict(v)
        result["tones"] = tones
        return result
    except Exception as exc:
        raise ValueError(
            f"Cannot analyze tones for voicing {pitches!r} with root {root!r}: {exc}"
        ) from exc


def voicing_drop2(
    pitches: str, root: Optional[str] = None, prefer_flat: bool = True
) -> dict[str, Any]:
    """Return the drop-2 voicing of a four-note voicing.

    Args:
        pitches: Space-separated pitch strings (must have exactly 4 pitches).
        root: Optional root chroma.
        prefer_flat: Use flat spelling for the result.

    Returns:
        Dict describing the drop-2 voicing.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        v = Voicing(pitches, root=root)
        if len(v) != 4:
            raise ValueError(f"drop2 requires exactly 4 pitches, got {len(v)}")
        return voicing_to_dict(v.drop2)
    except Exception as exc:
        raise ValueError(f"Cannot compute drop2 of voicing {pitches!r}: {exc}") from exc
    finally:
        Spelling.prefer_flat = prev


def voicing_drop3(
    pitches: str, root: Optional[str] = None, prefer_flat: bool = True
) -> dict[str, Any]:
    """Return the drop-3 voicing of a four-note voicing.

    Args:
        pitches: Space-separated pitch strings (must have exactly 4 pitches).
        root: Optional root chroma.
        prefer_flat: Use flat spelling for the result.

    Returns:
        Dict describing the drop-3 voicing.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        v = Voicing(pitches, root=root)
        if len(v) != 4:
            raise ValueError(f"drop3 requires exactly 4 pitches, got {len(v)}")
        return voicing_to_dict(v.drop3)
    except Exception as exc:
        raise ValueError(f"Cannot compute drop3 of voicing {pitches!r}: {exc}") from exc
    finally:
        Spelling.prefer_flat = prev


def voicing_drop24(
    pitches: str, root: Optional[str] = None, prefer_flat: bool = True
) -> dict[str, Any]:
    """Return the drop-2-and-4 voicing of a four-note voicing.

    Args:
        pitches: Space-separated pitch strings (must have exactly 4 pitches).
        root: Optional root chroma.
        prefer_flat: Use flat spelling for the result.

    Returns:
        Dict describing the drop-2-and-4 voicing.
    """
    prev = Spelling.prefer_flat
    try:
        Spelling.prefer_flat = prefer_flat
        v = Voicing(pitches, root=root)
        if len(v) != 4:
            raise ValueError(f"drop24 requires exactly 4 pitches, got {len(v)}")
        return voicing_to_dict(v.drop24)
    except Exception as exc:
        raise ValueError(f"Cannot compute drop24 of voicing {pitches!r}: {exc}") from exc
    finally:
        Spelling.prefer_flat = prev

"""PyVoicing MCP server – exposes the PyVoicing API as MCP tools, resources, and prompts."""
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from . import prompts as _prompts
from . import resources as _resources
from . import tools as _tools

mcp = FastMCP(
    "pyvoicing",
    instructions=(
        "PyVoicing MCP server: provides tools for symbolic music analysis "
        "including pitch manipulation, interval arithmetic, and chord voicing "
        "operations. All tools return structured JSON-serializable data. "
        "Use `pyvoicing://api-reference` for a quick API overview."
    ),
)

# ---------------------------------------------------------------------------
# Tools – Pitch
# ---------------------------------------------------------------------------


@mcp.tool(
    name="pitch_parse",
    description=(
        "Parse a pitch string (e.g. 'C4', 'Eb5', 'F#3') and return its "
        "properties: name, octave, MIDI value, frequency, ABC notation, "
        "LilyPond notation, and enharmonic spelling."
    ),
)
def pitch_parse(pitch: str, prefer_flat: bool = True) -> dict[str, Any]:
    return _tools.pitch_parse(pitch, prefer_flat=prefer_flat)


@mcp.tool(
    name="pitch_transpose",
    description=(
        "Transpose a pitch by an interval. "
        "interval can be an interval name like 'M3', 'P5', 'm7', or an integer "
        "semitone count like '7'. direction is 'up' (default) or 'down'."
    ),
)
def pitch_transpose(
    pitch: str,
    interval: str,
    direction: str = "up",
    prefer_flat: bool = True,
) -> dict[str, Any]:
    return _tools.pitch_transpose(pitch, interval, direction=direction, prefer_flat=prefer_flat)


@mcp.tool(
    name="pitch_distance",
    description=(
        "Return the interval distance from pitch_a to pitch_b. "
        "Returns interval name, semitone distance, and octave component."
    ),
)
def pitch_distance(pitch_a: str, pitch_b: str) -> dict[str, Any]:
    return _tools.pitch_distance(pitch_a, pitch_b)


@mcp.tool(
    name="pitch_spell",
    description=(
        "Return both flat and sharp spellings of a pitch. "
        "prefer_flat controls which spelling is used for the 'name' field; "
        "both spellings are always returned."
    ),
)
def pitch_spell(pitch: str, prefer_flat: Optional[bool] = None) -> dict[str, Any]:
    return _tools.pitch_spell(pitch, prefer_flat=prefer_flat)


@mcp.tool(
    name="pitch_notation",
    description=(
        "Return a pitch in multiple notations: scientific (e.g. 'C4'), "
        "ABC notation, and LilyPond notation."
    ),
)
def pitch_notation(pitch: str, prefer_flat: bool = True) -> dict[str, Any]:
    return _tools.pitch_notation(pitch, prefer_flat=prefer_flat)


# ---------------------------------------------------------------------------
# Tools – Chroma
# ---------------------------------------------------------------------------


@mcp.tool(
    name="chroma_transpose",
    description=(
        "Transpose a chroma (pitch class without octave, e.g. 'C', 'Eb', 'F#') "
        "by an interval. Returns the resulting chroma name and offset."
    ),
)
def chroma_transpose(
    chroma: str,
    interval: str,
    direction: str = "up",
    prefer_flat: bool = True,
) -> dict[str, Any]:
    return _tools.chroma_transpose(chroma, interval, direction=direction, prefer_flat=prefer_flat)


@mcp.tool(
    name="chroma_distance",
    description=(
        "Return the interval distance from chroma_a to chroma_b (modulo 12 / "
        "within one octave). Returns interval name and semitone distance."
    ),
)
def chroma_distance(chroma_a: str, chroma_b: str) -> dict[str, Any]:
    return _tools.chroma_distance(chroma_a, chroma_b)


# ---------------------------------------------------------------------------
# Tools – Interval
# ---------------------------------------------------------------------------


@mcp.tool(
    name="interval_parse",
    description=(
        "Parse an interval and return its properties. "
        "Accepts interval names like 'M3', 'P5', 'm7' or an integer "
        "semitone count like '14'."
    ),
)
def interval_parse(interval: str) -> dict[str, Any]:
    return _tools.interval_parse(interval)


@mcp.tool(
    name="interval_add",
    description="Add two intervals together and return the resulting interval.",
)
def interval_add(interval_a: str, interval_b: str) -> dict[str, Any]:
    return _tools.interval_add(interval_a, interval_b)


@mcp.tool(
    name="interval_subtract",
    description="Subtract interval_b from interval_a and return the resulting interval.",
)
def interval_subtract(interval_a: str, interval_b: str) -> dict[str, Any]:
    return _tools.interval_subtract(interval_a, interval_b)


# ---------------------------------------------------------------------------
# Tools – Voicing
# ---------------------------------------------------------------------------


@mcp.tool(
    name="voicing_parse",
    description=(
        "Parse a space-separated list of pitches into a voicing and return "
        "its properties. root is an optional chroma like 'C' or 'Bb'."
    ),
)
def voicing_parse(pitches: str, root: Optional[str] = None) -> dict[str, Any]:
    return _tools.voicing_parse(pitches, root=root)


@mcp.tool(
    name="voicing_transpose",
    description=(
        "Transpose a voicing by an interval. "
        "direction is 'up' (default) or 'down'."
    ),
)
def voicing_transpose(
    pitches: str,
    interval: str,
    root: Optional[str] = None,
    direction: str = "up",
    prefer_flat: bool = True,
) -> dict[str, Any]:
    return _tools.voicing_transpose(pitches, interval, root=root, direction=direction, prefer_flat=prefer_flat)


@mcp.tool(
    name="voicing_add",
    description="Add a pitch to a voicing and return the updated voicing.",
)
def voicing_add(
    pitches: str, add_pitch: str, root: Optional[str] = None
) -> dict[str, Any]:
    return _tools.voicing_add(pitches, add_pitch, root=root)


@mcp.tool(
    name="voicing_remove",
    description="Remove a pitch from a voicing and return the updated voicing.",
)
def voicing_remove(
    pitches: str, remove_pitch: str, root: Optional[str] = None
) -> dict[str, Any]:
    return _tools.voicing_remove(pitches, remove_pitch, root=root)


@mcp.tool(
    name="voicing_find_interval",
    description=(
        "Find all pitches in a voicing that form a given interval with "
        "a higher pitch in the same voicing."
    ),
)
def voicing_find_interval(
    pitches: str, interval: str, root: Optional[str] = None
) -> dict[str, Any]:
    return _tools.voicing_find_interval(pitches, interval, root=root)


@mcp.tool(
    name="voicing_to_root",
    description=(
        "Transpose a voicing so that its root lands on the given target pitch. "
        "root (chroma) is required."
    ),
)
def voicing_to_root(
    pitches: str,
    target: str,
    root: str,
    prefer_flat: bool = True,
) -> dict[str, Any]:
    return _tools.voicing_to_root(pitches, target, root=root, prefer_flat=prefer_flat)


@mcp.tool(
    name="voicing_tones",
    description=(
        "Analyze the chord tones of a voicing relative to its root. "
        "Returns tone labels like '1', 'maj3', '5', 'dom7', '9', '#11', etc."
    ),
)
def voicing_tones(pitches: str, root: str) -> dict[str, Any]:
    return _tools.voicing_tones(pitches, root)


@mcp.tool(
    name="voicing_drop2",
    description=(
        "Return the drop-2 voicing of a four-note closed voicing. "
        "The second-highest voice is dropped an octave."
    ),
)
def voicing_drop2(
    pitches: str, root: Optional[str] = None, prefer_flat: bool = True
) -> dict[str, Any]:
    return _tools.voicing_drop2(pitches, root=root, prefer_flat=prefer_flat)


@mcp.tool(
    name="voicing_drop3",
    description=(
        "Return the drop-3 voicing of a four-note closed voicing. "
        "The third-highest voice is dropped an octave."
    ),
)
def voicing_drop3(
    pitches: str, root: Optional[str] = None, prefer_flat: bool = True
) -> dict[str, Any]:
    return _tools.voicing_drop3(pitches, root=root, prefer_flat=prefer_flat)


@mcp.tool(
    name="voicing_drop24",
    description=(
        "Return the drop-2-and-4 voicing of a four-note closed voicing. "
        "The second- and fourth-highest voices are each dropped an octave."
    ),
)
def voicing_drop24(
    pitches: str, root: Optional[str] = None, prefer_flat: bool = True
) -> dict[str, Any]:
    return _tools.voicing_drop24(pitches, root=root, prefer_flat=prefer_flat)


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource(
    "pyvoicing://readme",
    name="PyVoicing README",
    description="Full project README with installation, usage examples, and API overview.",
    mime_type="text/markdown",
)
def resource_readme() -> str:
    return _resources.get_readme()


@mcp.resource(
    "pyvoicing://changelog",
    name="PyVoicing Changelog",
    description="Version history and release notes.",
    mime_type="text/markdown",
)
def resource_changelog() -> str:
    return _resources.get_changelog()


@mcp.resource(
    "pyvoicing://constants/chroma",
    name="Chroma constants",
    description="Mapping of semitone offset (0–11) to chroma name (flat-preferred).",
    mime_type="application/json",
)
def resource_chroma_constants() -> str:
    return _resources.get_chroma_constants()


@mcp.resource(
    "pyvoicing://constants/intervals",
    name="Interval constants",
    description="Mapping of semitone offset (0–11) to interval name.",
    mime_type="application/json",
)
def resource_interval_constants() -> str:
    return _resources.get_interval_constants()


@mcp.resource(
    "pyvoicing://constants/offsets",
    name="Offset constants",
    description="Mapping of pitch/interval name strings to semitone offset.",
    mime_type="application/json",
)
def resource_offset_constants() -> str:
    return _resources.get_offset_constants()


@mcp.resource(
    "pyvoicing://api-reference",
    name="PyVoicing API reference",
    description="Compact quick-reference for all PyVoicing classes and methods.",
    mime_type="text/markdown",
)
def resource_api_reference() -> str:
    return _resources.get_api_reference()


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@mcp.prompt(
    name="analyze_voicing",
    description=(
        "Analyze a chord voicing to identify chord tones, chord quality, "
        "tensions, and voicing type."
    ),
)
def prompt_analyze_voicing(pitches: str, root: str) -> list[dict[str, Any]]:
    return _prompts.analyze_voicing(pitches, root)


@mcp.prompt(
    name="explain_pitch_spelling",
    description=(
        "Explain the enharmonic spelling choices for a pitch, including "
        "flat vs. sharp usage in different musical contexts."
    ),
)
def prompt_explain_pitch_spelling(pitch: str) -> list[dict[str, Any]]:
    return _prompts.explain_pitch_spelling(pitch)


@mcp.prompt(
    name="suggest_chord_tones",
    description=(
        "Suggest chord-tone interpretation for a set of pitches given a root, "
        "including scale degrees, chord symbol, and alternative roots."
    ),
)
def prompt_suggest_chord_tones(pitches: str, root: str) -> list[dict[str, Any]]:
    return _prompts.suggest_chord_tones(pitches, root)


@mcp.prompt(
    name="convert_voicing_description",
    description=(
        "Convert a voicing to a symbolic chord description (chord symbol, "
        "jazz notation) and suggest alternative voicings or reharmonizations."
    ),
)
def prompt_convert_voicing_description(pitches: str, root: str) -> list[dict[str, Any]]:
    return _prompts.convert_voicing_description(pitches, root)


def main() -> None:
    """Entry point: run the PyVoicing MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()

"""Tests for pyvoicing_mcp tools, serializers, resources, and prompts."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pyvoicing_mcp import tools as t
from pyvoicing_mcp import resources as r
from pyvoicing_mcp import prompts as pr
from pyvoicing_mcp.serializers import (
    chroma_to_dict,
    interval_to_dict,
    pitch_to_dict,
    voicing_to_dict,
)
from pyvoicing import Chroma, Interval, Pitch, Voicing


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------


class TestSerializers:
    def test_pitch_to_dict_c4(self):
        d = pitch_to_dict(Pitch("C4"))
        assert d["name"] == "C"
        assert d["octave"] == 4
        assert d["midi"] == 60
        assert d["offset"] == 0
        assert abs(d["freq"] - 261.625) < 0.1

    def test_pitch_to_dict_rest(self):
        from pyvoicing.rest import Rest

        p = Pitch(0)
        p.value = Rest()
        d = pitch_to_dict(p)
        assert d == {"type": "rest"}

    def test_chroma_to_dict(self):
        d = chroma_to_dict(Chroma("G"))
        assert d == {"name": "G", "offset": 7}

    def test_interval_to_dict(self):
        d = interval_to_dict(Interval("M3"))
        assert d["name"] == "M3"
        assert d["distance"] == 4
        assert d["octave"] == 0

    def test_voicing_to_dict(self):
        v = Voicing("C4 E4 G4", root="C")
        d = voicing_to_dict(v)
        assert d["root"] == "C"
        assert d["midi"] == [60, 64, 67]
        assert len(d["pitches"]) == 3

    def test_voicing_to_dict_no_root(self):
        v = Voicing("C4 E4 G4")
        d = voicing_to_dict(v)
        assert d["root"] is None


# ---------------------------------------------------------------------------
# Pitch tools
# ---------------------------------------------------------------------------


class TestPitchTools:
    def test_pitch_parse_c4(self):
        d = t.pitch_parse("C4")
        assert d["midi"] == 60
        assert d["octave"] == 4
        assert d["name"] == "C"
        assert "abc" in d
        assert "lilypond" in d
        assert "enharmonic" in d

    def test_pitch_parse_eb5(self):
        d = t.pitch_parse("Eb5", prefer_flat=True)
        assert d["name"] == "Eb"
        assert d["octave"] == 5

    def test_pitch_parse_sharp(self):
        d = t.pitch_parse("C#4", prefer_flat=False)
        assert d["name"] == "C#"

    def test_pitch_parse_invalid(self):
        with pytest.raises(ValueError, match="Cannot parse pitch"):
            t.pitch_parse("ZZZ9")

    def test_pitch_transpose_up(self):
        d = t.pitch_transpose("C4", "M3")
        assert d["midi"] == 64

    def test_pitch_transpose_down(self):
        d = t.pitch_transpose("E4", "M3", direction="down")
        assert d["midi"] == 60

    def test_pitch_transpose_semitones(self):
        d = t.pitch_transpose("C4", "7")
        assert d["midi"] == 67

    def test_pitch_distance_ascending(self):
        d = t.pitch_distance("C4", "E4")
        assert d["distance"] == 4
        assert d["interval"] == "M3"

    def test_pitch_distance_descending(self):
        d = t.pitch_distance("E4", "C4")
        assert d["distance"] == -4

    def test_pitch_spell(self):
        d = t.pitch_spell("C#4")
        assert d["flat"] == "Db4"
        assert d["sharp"] == "C#4"

    def test_pitch_spell_prefer_flat(self):
        d = t.pitch_spell("C#4", prefer_flat=True)
        assert d["name"] == "Db4"

    def test_pitch_notation(self):
        d = t.pitch_notation("C4")
        assert d["scientific"] == "C4"
        assert "abc" in d
        assert "lilypond" in d


# ---------------------------------------------------------------------------
# Chroma tools
# ---------------------------------------------------------------------------


class TestChromaTools:
    def test_chroma_transpose_up(self):
        d = t.chroma_transpose("C", "P5")
        assert d["name"] == "G"
        assert d["offset"] == 7

    def test_chroma_transpose_down(self):
        d = t.chroma_transpose("G", "P5", direction="down")
        assert d["name"] == "C"

    def test_chroma_distance(self):
        d = t.chroma_distance("C", "G")
        assert d["distance"] == 7

    def test_chroma_distance_wraps(self):
        # Going from G to C is 5 semitones up (modulo 12)
        d = t.chroma_distance("G", "C")
        assert d["distance"] == 5


# ---------------------------------------------------------------------------
# Interval tools
# ---------------------------------------------------------------------------


class TestIntervalTools:
    def test_interval_parse_name(self):
        d = t.interval_parse("M3")
        assert d["distance"] == 4
        assert d["interval"] == "M3"
        assert d["octave"] == 0

    def test_interval_parse_semitones(self):
        d = t.interval_parse("14")
        assert d["distance"] == 14
        assert d["octave"] == 1

    def test_interval_add(self):
        d = t.interval_add("M3", "m3")
        assert d["distance"] == 7
        assert d["interval"] == "P5"

    def test_interval_subtract(self):
        d = t.interval_subtract("P5", "M3")
        assert d["distance"] == 3
        assert d["interval"] == "m3"


# ---------------------------------------------------------------------------
# Voicing tools
# ---------------------------------------------------------------------------


class TestVoicingTools:
    def test_voicing_parse(self):
        d = t.voicing_parse("C4 E4 G4", root="C")
        assert d["midi"] == [60, 64, 67]
        assert d["root"] == "C"

    def test_voicing_parse_no_root(self):
        d = t.voicing_parse("C4 E4 G4")
        assert d["root"] is None

    def test_voicing_transpose_up(self):
        d = t.voicing_transpose("C4 E4 G4", "M2", root="C")
        assert d["midi"] == [62, 66, 69]

    def test_voicing_transpose_down(self):
        d = t.voicing_transpose("D4 F#4 A4", "M2", root="D", direction="down")
        assert d["midi"] == [60, 64, 67]

    def test_voicing_add(self):
        d = t.voicing_add("C4 E4 G4", "B4", root="C")
        assert 71 in d["midi"]
        assert len(d["pitches"]) == 4

    def test_voicing_remove(self):
        d = t.voicing_remove("C4 E4 G4 B4", "E4", root="C")
        assert 64 not in d["midi"]
        assert len(d["pitches"]) == 3

    def test_voicing_find_interval(self):
        d = t.voicing_find_interval("C4 E4 G4 B4", "M3")
        # C4–E4 and G4–B4 are both M3
        assert len(d["lower_pitches"]) == 2

    def test_voicing_to_root(self):
        d = t.voicing_to_root("C4 E4 G4 B4", "G4", root="C")
        assert d["midi"][0] == 67  # root (C-equivalent) now at G4

    def test_voicing_to_root_requires_root(self):
        with pytest.raises(ValueError, match="root is required"):
            t.voicing_to_root("C4 E4 G4", "G4")

    def test_voicing_tones_cmaj7(self):
        d = t.voicing_tones("C4 E4 G4 B4", "C")
        assert d["tones"] == ["1", "maj3", "5", "maj7"]

    def test_voicing_tones_dm7b5(self):
        d = t.voicing_tones("B3 D4 F4 A4", "B")
        assert "min3" in d["tones"] or "b5" in d["tones"]

    def test_voicing_drop2(self):
        d = t.voicing_drop2("C4 E4 G4 B4", root="C")
        # Drop-2: second-highest (G4) drops an octave to G3
        assert 55 in d["midi"]  # G3

    def test_voicing_drop2_wrong_count(self):
        with pytest.raises(ValueError, match="drop2 requires exactly 4"):
            t.voicing_drop2("C4 E4 G4")

    def test_voicing_drop3(self):
        d = t.voicing_drop3("C4 E4 G4 B4", root="C")
        # Drop-3: third-highest (E4) drops an octave to E3
        assert 52 in d["midi"]  # E3

    def test_voicing_drop24(self):
        d = t.voicing_drop24("C4 E4 G4 B4", root="C")
        # Drop-2-and-4: C4 and G4 each drop an octave
        assert 48 in d["midi"]  # C3
        assert 55 in d["midi"]  # G3


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


class TestResources:
    def test_readme_contains_pyvoicing(self):
        text = r.get_readme()
        assert "PyVoicing" in text

    def test_changelog_contains_version(self):
        text = r.get_changelog()
        assert "0.1" in text

    def test_chroma_constants_json(self):
        text = r.get_chroma_constants()
        data = json.loads(text)
        assert data["0"] == "C"
        assert data["7"] == "G"

    def test_interval_constants_json(self):
        text = r.get_interval_constants()
        data = json.loads(text)
        assert data["4"] == "M3"
        assert data["7"] == "P5"

    def test_offset_constants_json(self):
        text = r.get_offset_constants()
        data = json.loads(text)
        assert data["C"] == 0
        assert data["G"] == 7

    def test_api_reference(self):
        text = r.get_api_reference()
        assert "Pitch" in text
        assert "Voicing" in text
        assert "Interval" in text


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


class TestPrompts:
    def test_analyze_voicing_prompt(self):
        msgs = pr.analyze_voicing("C4 E4 G4 B4", "C")
        assert len(msgs) == 1
        assert msgs[0]["role"] == "user"
        assert "C4 E4 G4 B4" in msgs[0]["content"]

    def test_explain_pitch_spelling_prompt(self):
        msgs = pr.explain_pitch_spelling("C#4")
        assert len(msgs) == 1
        assert "C#4" in msgs[0]["content"]

    def test_suggest_chord_tones_prompt(self):
        msgs = pr.suggest_chord_tones("C4 E4 G4", "C")
        assert len(msgs) == 1
        assert msgs[0]["role"] == "user"

    def test_convert_voicing_description_prompt(self):
        msgs = pr.convert_voicing_description("C4 E4 G4 B4", "C")
        assert len(msgs) == 1
        assert msgs[0]["role"] == "user"


# ---------------------------------------------------------------------------
# Server smoke test
# ---------------------------------------------------------------------------


class TestServerLoad:
    def test_server_imports(self):
        from pyvoicing_mcp.server import mcp

        tool_names = {tool.name for tool in mcp._tool_manager._tools.values()}
        expected = {
            "pitch_parse",
            "pitch_transpose",
            "pitch_distance",
            "pitch_spell",
            "pitch_notation",
            "chroma_transpose",
            "chroma_distance",
            "interval_parse",
            "interval_add",
            "interval_subtract",
            "voicing_parse",
            "voicing_transpose",
            "voicing_add",
            "voicing_remove",
            "voicing_find_interval",
            "voicing_to_root",
            "voicing_tones",
            "voicing_drop2",
            "voicing_drop3",
            "voicing_drop24",
        }
        assert expected.issubset(tool_names)

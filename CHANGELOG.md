# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Note: PyVoicing is currently in alpha; the API is subject to change.

## [0.1.5] - 2026-07-10
### Added
- MCP server package `pyvoicing_mcp` in `src/pyvoicing_mcp/`.
- 20 MCP tools wrapping Pitch, Chroma, Interval, and Voicing APIs.
- 6 MCP resources: README, changelog, chroma/interval/offset constants, API quick-reference.
- 4 MCP prompts: analyze_voicing, explain_pitch_spelling, suggest_chord_tones, convert_voicing_description.
- `[mcp]` optional dependency group with `mcp>=1.9.0`.
- `pyvoicing-mcp` console script entry point to run the server over stdio.
- Serialization helpers in `pyvoicing_mcp.serializers` for JSON-friendly output.
- 52 pytest tests covering tools, serializers, resources, and prompts.
- README section documenting MCP installation, configuration, tools, resources, and prompts.

## [0.1.4] - 2025-12-25
### Added
- Shared spelling preference via Spelling.prefer_flat.
- Pitch.lilypond with English LilyPond note names.
- Pitch.freq and pitch/chroma spell/enharmonic helpers.
- Named methods for transposition and voicing operations.
- Pytest-based tests for core types.

### Changed
- Operator usage aligned with named methods (transpose/add/remove).
- Voicing.tones replaces chord-tone output from ~voicing; ~voicing now returns MIDI values.

## [0.1.3] - 2025-04-30
### Fixed
- Rest.__str__()

## [0.1.2] - 2025-04-30
### Added
- Voicings.Drop2/3/24
- Voicings.int_list

## [0.1.1] - 2025-04-29
### Fixed
- Corrected ABC notation parsing in Pitch.

## [0.1.0] - 2025-04-28
### Added
- Initial release.

# Playlist Refactor

## Objective
Improve structure, readability, and duplication while preserving original behavior.

## Key Issues Identified
- Repeated `title;artist` parsing logic across multiple methods.
- `remove_song` relied on inline string conversion for comparison.
- Manual `open()` / `close()` file handling.
- Variable shadowing (`song` used as both class and variable name).
- Redundant comments describing obvious code behavior.

## Refactoring Steps
- Introduced `DELIM` and `_to_line()` to centralize the file-line representation of a song.
- Simplified `remove_song` to remove the first matching element safely using index-based removal.
- Replaced manual file handling with context managers (`with open(...)`).
- Improved naming to avoid shadowing and clarify intent.
- Simplified filtering logic in `get_songs_by_artist`.
- Removed redundant inline comments.

## Result
The class now has:
- Reduced duplication
- Clearer intent and naming
- Safer file handling
- More readable iteration and comparison logic

All changes preserve external behavior while improving maintainability.

## Tradeoffs & Future Considerations
- The class still mixes playlist behavior with file persistence. In a larger system, separating storage from domain logic would improve testability and flexibility.
- Songs are represented as delimited strings in the file format. Introducing a structured `Song` model (e.g., a dataclass) would further reduce parsing concerns.
- Input validation for malformed file lines is minimal; behavior was intentionally preserved rather than expanded.

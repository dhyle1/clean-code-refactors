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
- Introduced `_extract_title_artist` to centralize parsing logic.
- Simplified `remove_song` to remove the first matching element safely using index-based removal.
- Replaced manual file handling with context managers (`with open(...)`).
- Improved naming to avoid shadowing and clarify intent.
- Simplified filtering logic in `get_songs_by_artist`.
- Removed redundant inline comments.

## Result
The class now has:
- Reduced duplication
- Clearer separation of responsibilities
- Safer file handling
- More readable iteration and comparison logic

All changes preserve external behavior while improving maintainability.

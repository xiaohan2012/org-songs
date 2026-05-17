# Agent Guidelines

## Entry Point
- `main.py` — run directly with `python main.py`
- Org file path is hardcoded to `/Users/hanxiao/docs/notes/songs.org`

## Dependencies
- `pytube`, `pytubefix`, `orgparse`, `pydub` — install manually if missing

## Output
- Downloads go to `./downloads/` (gitignored)

## Audio Clipping
- Add `:start:` and `:end:` org properties (e.g., `start: 1:30`, `end: 3:45`) to clip downloaded audio
- Clipped audio replaces the original file

## Update Music Player
- `update.sh` runs `mpc` commands (unrelated to download logic)
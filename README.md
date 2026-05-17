# org-songs

Download YouTube audio files and clip them based on org-mode properties.

## Usage

```bash
python main.py
```

## Org File Format

```org
* Directory Name           <- creates folder in downloads/
** Song Title              <- single asterisk = song entry
https://www.youtube.com/watch?v=...

** Song with Clip
:PROPERTIES:
:start: 1:30
:end: 3:45
:END:
https://www.youtube.com/watch?v=...

** Clipped (skip re-clipping)
:PROPERTIES:
:start: 1:30
:end: 3:45
:clipped: true
:END:
https://www.youtube.com/watch?v=...

** Downloaded Externally
:PROPERTIES:
:downloaded: external
:END:
https://www.youtube.com/watch?v=...
```

Nested headings create subdirectories. `*` = section/directory, `**` = song entry.

## Org File Properties

- `start` / `end` — clip audio (format: `M:SS` or `H:MM:SS`)
- `clipped: true` — skip already clipped songs
- `downloaded: external` — song downloaded via external tool, skip download

## Dependencies

- pytube, pytubefix, orgparse
- ffmpeg (for clipping)

## External Download

For unavailable videos: https://vd6s.net/en5/
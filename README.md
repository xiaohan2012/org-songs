# org-songs

A YouTube audio downloader using an org-mode file as the song database.

## Concept

Songs are stored in an org file (`songs.org`) with their YouTube URLs. A Python script crawls the org file and downloads the audio files.

## Usage

```bash
python main.py  # downloads songs, clips by :start:/:end:, skips already downloaded/clipped
```

## Rescue Songs

```bash
python rescue.py  # writes rescue.org next to songs.org
```

Checklist of popular songs by the artists in `songs.org` (plus a list of same-era artists), minus songs already there, to jog memory.
Hot songs come from NetEase Cloud Music; Jay Chou's own songs are missing there (copyright), only collaborations show.

Then download the ticked songs:

```bash
python rescue_pick.py          # best YouTube match per ticked song -> rescue-review.org
# review rescue-review.org: fix wrong URLs, delete unwanted entries
python rescue_pick.py --apply  # append the reviewed songs to songs.org
python main.py                 # download them
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

- orgparse
- yt-dlp (`brew install yt-dlp`)
- ffmpeg (for clipping)

## External Download

For unavailable videos: https://vd6s.net/en5/
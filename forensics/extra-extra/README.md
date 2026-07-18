Title: Extra, Extra
Description: Someone archived some routine internal documents before their account was suspended. Nothing of note in the files themselves. Have a look anyway.
Category: Forensics
Difficulty: Easy

## Setup

```bash
docker compose up --build -d
```

Players download the file from:

    http://<host>:8093/challenge.zip

Tear down:

```bash
docker compose down
```

## Notes for organizers

- `generate.py` creates a ZIP archive containing four mundane decoy documents.
  The flag (base64-encoded) is stored in the ZIP file's archive-level comment
  field, disguised as a build/revision string: `INTERNAL // BUILD: ... // REV: <base64>`.
- The individual files contain no flag or hidden data — only the archive
  comment does.
- The comment is accessible via:
    - `python3 -c "import zipfile; print(zipfile.ZipFile('challenge.zip').comment)"`
    - `unzip -z challenge.zip`
    - `zipnote challenge.zip`
    - Any hex editor (look at the last ~100 bytes of the file)
- To use a different flag, edit `.env` and run `docker compose up --build -d`.
- See `solution.txt` for the walkthrough.

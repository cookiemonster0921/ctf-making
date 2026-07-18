Title: Lost Privileges
Description: We set up a new internal management server and gave you the most restricted account we could. There's nothing you can do with it anyway.
Category: PWN
Difficulty: Hard

## Setup

```bash
# .env already contains a real flag; replace the value if you want a custom one.
# .env.example has a placeholder if you need a clean starting point.
docker compose up --build -d
```

Players connect on port 9001:

```bash
nc <host> 9001
```

Tear down:

```bash
docker compose down
```

## Notes for organizers

- Container is Ubuntu 20.04 with `sudo 1.9.5p1` compiled from source — the last
  vulnerable release before the CVE-2021-3156 patch landed in 1.9.5p2.
- The player lands as `player`, a normal user with **no sudoers entry at all**.
  The point of this bug is that sudoers membership is irrelevant.
- Flag is at `/root/flag.txt` (mode 600, root:root) — unreadable without root.
- The image has `gcc`, `make`, `python3`, `wget`, `curl`, and `git` so players can
  fetch and compile a public PoC from inside the box (Docker containers have
  outbound internet by default).
- See `solution.txt` for the verified walkthrough.

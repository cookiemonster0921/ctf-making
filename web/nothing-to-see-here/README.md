Title: Nothing To See Here
Description: Management insists this website is completely boring and has absolutely nothing worth finding. We're sure they're right.
Category: WEB
Difficulty: Medium

## Setup

```bash
# .env already contains a real flag; replace the value if you want a custom one.
# .env.example has a placeholder if you need a clean starting point.
docker compose up --build -d
```

The challenge web server is on port 8080:

```bash
curl http://<host>:8080/
```

Tear down:

```bash
docker compose down
```

## Notes for organizers

- Runs `httpd:2.4.49`, the exact Apache version affected by CVE-2021-41773
  (path traversal via URL-encoded dot segments).
- The Dockerfile patches `<Directory />` from `Require all denied` (the secure
  default) to `Require all granted`, replicating the real-world misconfiguration
  that made the vulnerability exploitable in production at the time. The stock
  Docker image's config is otherwise untouched.
- The flag is written to `/usr/local/apache2/flag.txt` at container start from
  the `FLAG` environment variable. It is intentionally placed outside the
  document root (`htdocs/`) so it is not browseable normally.
- The working traversal path goes through the `cgi-bin` alias:
    curl --path-as-is http://<host>:8080/cgi-bin/.%2e/flag.txt
  `%2e` is the URL-encoding of `.`. Apache 2.4.49 fails to normalise this
  before resolving the filesystem path, allowing one `..` traversal out of
  the cgi-bin directory and into the apache2 root where the flag lives.
- See `solution.txt` for the verified walkthrough.

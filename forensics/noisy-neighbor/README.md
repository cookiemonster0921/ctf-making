Title: Noisy Neighbor
Description: Our IDS flagged some unusual traffic from a workstation last Tuesday. Here is the packet capture from that window. Probably nothing.
Category: Forensics
Difficulty: Hard

## Setup

```bash
docker compose up --build -d
```

Players download the file from:

    http://<host>:8092/challenge.pcap

Tear down:

```bash
docker compose down
```

## Notes for organizers

- `generate.py` base32-encodes the flag, splits it into 8-character chunks,
  and embeds each chunk as a subdomain of `exfil.corp` in DNS query packets.
  The exfiltration packets are interleaved with noise (legitimate-looking DNS
  queries to real domains from random internal IPs).
- The PCAP is generated at container start from the `FLAG` environment
  variable.  No code changes are needed to use a different flag — edit `.env`
  and run `docker compose up --build -d`.
- The suspicious traffic is distinguishable by destination IP and domain name:
  `*.exfil.corp` queries go to `185.220.101.42` while all other DNS goes to
  `8.8.8.8` or `1.1.1.1`.
- See `solution.txt` for the complete walkthrough (Wireshark GUI and tshark
  one-liner).

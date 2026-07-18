#!/usr/bin/env python3
"""
Generate a PCAP file containing simulated DNS exfiltration traffic.

The flag is base32-encoded and transmitted as sub-labels of a suspicious
domain (exfil.corp), interleaved with legitimate-looking DNS queries to
create plausible deniability.

Players must:
  1. Open the PCAP in Wireshark or tshark.
  2. Filter for DNS queries to *.exfil.corp.
  3. Extract the sub-labels in order, concatenate, base32-decode.
"""
import base64
import os
import random
import struct
import socket
import time

# ---------------------------------------------------------------------------
# Minimal raw PCAP writer (no scapy dependency)
# ---------------------------------------------------------------------------

PCAP_MAGIC   = 0xA1B2C3D4
SNAP_LEN     = 65535
LINK_ETHERNET = 1

def pcap_global_header() -> bytes:
    return struct.pack('<IHHiIII',
        PCAP_MAGIC, 2, 4,          # magic, version major/minor
        0, 0,                       # thiszone, sigfigs
        SNAP_LEN, LINK_ETHERNET)   # snaplen, network

def pcap_record(ts_sec: int, ts_usec: int, data: bytes) -> bytes:
    n = len(data)
    return struct.pack('<IIII', ts_sec, ts_usec, n, n) + data

def ip4(src: str, dst: str) -> bytes:
    return socket.inet_aton(src) + socket.inet_aton(dst)

def build_dns_query(qname: str) -> bytes:
    """Minimal DNS query (no answer, no checksum magic — Wireshark is lenient)."""
    header = struct.pack('>HHHHHH',
        random.randint(0x1000, 0xFFFF),  # transaction ID
        0x0100,   # flags: standard query + recursion desired
        1, 0, 0, 0)  # QDCOUNT=1, rest 0
    # QNAME: length-prefixed labels terminated by \x00
    labels = b''
    for label in qname.rstrip('.').split('.'):
        b = label.encode()
        labels += bytes([len(b)]) + b
    labels += b'\x00'
    question = labels + struct.pack('>HH', 1, 1)  # QTYPE=A, QCLASS=IN
    return header + question

def build_udp(sport: int, dns_payload: bytes) -> bytes:
    length = 8 + len(dns_payload)
    return struct.pack('>HHHH', sport, 53, length, 0) + dns_payload

def build_ipv4(src: str, dst: str, udp_payload: bytes) -> bytes:
    proto = 17  # UDP
    ihl   = 5
    total = 4 * ihl + len(udp_payload)
    return struct.pack('>BBHHHBBH4s4s',
        (4 << 4) | ihl, 0, total,
        random.randint(0, 0xFFFF),  # ID
        0x4000,   # Don't fragment
        64, proto, 0,
        socket.inet_aton(src),
        socket.inet_aton(dst)) + udp_payload

def build_ethernet(ip_payload: bytes) -> bytes:
    dst_mac = b'\xff\xff\xff\xff\xff\xff'
    src_mac = bytes([0x52, 0x54, 0x00,
                     random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255)])
    ethertype = b'\x08\x00'  # IPv4
    return dst_mac + src_mac + ethertype + ip_payload

def make_packet(src_ip: str, dst_ip: str, qname: str) -> bytes:
    dns  = build_dns_query(qname)
    udp  = build_udp(random.randint(1024, 65535), dns)
    ip   = build_ipv4(src_ip, dst_ip, udp)
    eth  = build_ethernet(ip)
    return eth

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

LEGIT_DOMAINS = [
    'google.com', 'microsoft.com', 'ubuntu.com',
    'github.com', 'stackoverflow.com', 'cloudflare.com',
    'aws.amazon.com', 'api.twitter.com',
]

INTERNAL_IPS = [f'10.0.0.{i}' for i in range(10, 30)]

def main():
    flag    = os.environ.get('FLAG', 'CSEC{placeholder_change_me}')
    out     = os.environ.get('OUTPUT', '/data/challenge.pcap')
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)

    # Encode flag: base32, lower-case, strip padding, split into 8-char chunks
    b32    = base64.b32encode(flag.encode()).decode().rstrip('=').lower()
    chunks = [b32[i:i+8] for i in range(0, len(b32), 8)]

    exfil_src = '10.0.0.50'
    exfil_dst = '185.220.101.42'  # Fake "C2" address

    packets: list[tuple[float, bytes]] = []
    base_ts = 1_700_000_000.0

    # Scatter noise packets throughout the capture
    for _ in range(len(chunks) * 4):
        ts  = base_ts + random.uniform(0, len(chunks) * 6)
        pkt = make_packet(
            random.choice(INTERNAL_IPS),
            random.choice(['8.8.8.8', '1.1.1.1']),
            random.choice(LEGIT_DOMAINS))
        packets.append((ts, pkt))

    # Exfiltration packets in order (each separated by a few seconds)
    for i, chunk in enumerate(chunks):
        ts  = base_ts + i * 5.0 + random.uniform(0.1, 0.8)
        qname = f'{chunk}.exfil.corp'
        pkt = make_packet(exfil_src, exfil_dst, qname)
        packets.append((ts, pkt))

    # Sort by timestamp
    packets.sort(key=lambda x: x[0])

    with open(out, 'wb') as f:
        f.write(pcap_global_header())
        for ts, pkt in packets:
            sec  = int(ts)
            usec = int((ts - sec) * 1_000_000)
            f.write(pcap_record(sec, usec, pkt))

    print(f'Generated {out}  ({len(packets)} packets, {len(chunks)} exfil chunks)')
    print(f'Flag encodes to {len(chunks)} DNS subdomain chunks under *.exfil.corp')

if __name__ == '__main__':
    main()

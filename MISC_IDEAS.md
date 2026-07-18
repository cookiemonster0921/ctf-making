# Miscellaneous CTF Challenge Ideas

These are challenge concepts that don't fit neatly into Web / PWN / Rev / Crypto / Forensics.
They are ideas only — not yet implemented — and vary in difficulty.

---

## 1. SSTV Radio Transmission
**Category:** Signals / Misc  
**Difficulty:** Medium

Provide a WAV or OGG audio file containing a Slow Scan Television (SSTV) transmission.
SSTV is an analogue protocol used by amateur radio operators to send images over voice
frequencies. When decoded with software (QSSTV on Linux, Robot36 on Android, or
browser-based decoders), the audio reveals an image that contains the flag.

**Why obscure:** Most participants will try to listen to or analyse the waveform;
the idea that audio is actually a picture is non-obvious. The decoding tool is free
but not commonly known.

**Implementation:** Generate the SSTV signal using the `pySSTV` Python library. Embed
the flag in an image (e.g., as text on a background) and encode it in the Martin M1
or Scottie S1 SSTV mode. Host via Docker + HTTP.

---

## 2. Whitespace Language
**Category:** Misc / Rev  
**Difficulty:** Medium

Give players a file that appears to be blank or empty — it contains only spaces, tabs,
and newlines. This is actually a valid program in the Whitespace esoteric programming
language. When run with a Whitespace interpreter, it prints the flag.

**Why obscure:** Most text editors collapse whitespace or display it invisibly. Players
must realise the "blank" file is executable code and find a Whitespace interpreter.

**Implementation:** Write a Whitespace program using an online generator that pushes
and prints flag characters. The flag value can be parametrised by generating the
Whitespace program at container start from the `FLAG` env var. No Docker needed if
the generated file is committed directly.

---

## 3. QR Code Repair
**Category:** Misc  
**Difficulty:** Medium-Hard

Provide a QR code image that has been partially corrupted (a rectangular region
of modules replaced with noise or zeros). QR codes include Reed-Solomon error
correction capable of recovering up to 30% of damaged data (level H). Players
must:
1. Recognise it as a corrupted QR code
2. Use error-correction-aware QR tools (or manually reconstruct modules)
3. Decode the QR to get the flag

**Why obscure:** Players instinctively try to scan the damaged QR directly and fail.
The solution requires knowing QR error correction exists and using specialised tools.

**Implementation:** Generate a clean QR code of the flag using `qrcode` (Python),
then zero out a rectangular region covering ≤ 30% of codewords. Docker generates
the corrupted image; players download and repair it.

---

## 4. Machine Identification Code (Printer Dots)
**Category:** Forensics / Misc  
**Difficulty:** Hard

Provide a high-resolution scan of a printed document (as a PNG or TIFF). The
document contains an array of tiny yellow dots — the Machine Identification Code
(MIC, also called "yellow dots" or "tracking dots") printed by colour laser
printers. In this challenge, the dots encode the flag using the known ECI-based
MIC pattern, rather than a real printer serial number.

**Why obscure:** MIC dots are invisible at normal viewing distance and scale, and
virtually unknown outside niche forensics circles. The solution requires magnifying
the yellow channel of the image and decoding a grid pattern.

**Implementation:** Synthetically add the dot pattern to a document image at build
time. Provide a reference to the known MIC grid format (e.g., from the EFF's
research) so the challenge is solvable without proprietary knowledge.

---

## 5. Blockchain Event Log
**Category:** Blockchain / Misc  
**Difficulty:** Medium

Deploy a smart contract on an Ethereum testnet (Sepolia or Holesky) that emits
the flag as a `FlagCaptured(string flag)` event in its constructor. Players receive
the contract address and must query blockchain history to find the flag embedded
in the event log.

**Why obscure:** Players who have never used Etherscan or Web3 tools will need to
learn a new environment. The flag is not in the contract's current state — only in
historical transaction logs — so reading the ABI alone isn't enough.

**Tools for players:** Etherscan (block explorer UI), `cast logs` (Foundry CLI),
or a short `web3.py` script.

**No Docker needed.** The flag is fixed at deploy time so this challenge cannot
accept a dynamic flag without redeployment; suitable for static flag competitions.

---

## 6. Custom Binary Protocol
**Category:** Misc / Pwn  
**Difficulty:** Hard

A Docker service that listens on a TCP port and speaks a custom binary protocol.
The "handshake" requires sending a specific sequence of bytes in the right format.
Players interact with the service using `nc` or Python sockets, observe the binary
responses (error codes, length-prefixed messages), reverse-engineer the request
format, and craft the correct "UNLOCK" command to receive the flag.

**Why obscure:** Players must think about packet structure (magic bytes, length
fields, command opcodes, checksums) without source code. The service gives
meaningful error codes that guide the reverse engineering.

**Implementation:** A simple Python asyncio server with a 3-step handshake:
(1) receive magic + version, (2) receive a challenge-response (XOR or CRC), (3)
receive UNLOCK command with correct password derived from the challenge. Flag is
returned on success.

---

## 7. Brainfuck or Esoteric Language
**Category:** Misc  
**Difficulty:** Easy

Provide a program in an esoteric language — Brainfuck, Befunge, Malbolge, or
Piet — that when executed prints a modified version of the flag (ROT13, reversed,
or base64). Players must: (1) recognise the language from its distinctive syntax,
(2) find an interpreter online or locally, (3) run the program, (4) decode the output.

**Why it works as a beginner challenge:** The esoteric language aspect is daunting
but execution is trivial once they find a web-based interpreter (e.g., copy-paste
into an online Brainfuck runner). The extra decoding step prevents trivial solutions.

**Implementation:** Generate the esoteric source at build time using a known
transpiler or generate.py that converts the flag to Brainfuck instructions. No
Docker needed if the source is committed directly.

---

## 8. Polyglot File
**Category:** Forensics / Misc  
**Difficulty:** Hard

Provide a file that is simultaneously valid in two file formats. For example, a
file that is both a valid JPEG image and a valid ZIP archive (this is possible due
to how each format's magic bytes and structure are located). The JPEG shows a
decoy image; the ZIP contains a file with a clue, but the flag is in a third
layer — for example, in the comment field of the ZIP (which is also a polyglot).

**Why obscure:** Players see an image, assume it is forensics-style stego, and chase
red herrings. The trick is recognising the file has multiple valid interpretations.

**Tools:** `file` command, hex editor, `unzip`, `binwalk`.

**Implementation:** Construct the polyglot manually with Python's struct module or
use the `polyglot` tool. Host via Docker + HTTP.

---

## 9. Timecode Steganography
**Category:** Misc / Forensics  
**Difficulty:** Medium

Provide a short video file. The flag is encoded in the SMPTE timecode track or
embedded in closed-caption / subtitle metadata (SRT / WebVTT embedded in the
container). Casual viewers see normal video; the flag is invisible unless the
player examines the subtitle stream or timecode metadata.

**Why obscure:** Players will look at the video frames and audio; extracting
subtitle/timecode tracks requires knowing they exist and using `ffprobe` or
`ffmpeg -map` to extract them.

**Implementation:** Create a short MP4 using FFmpeg with a subtitle track that
contains the flag hidden among fake subtitles, encoded in a non-default encoding
(e.g., the subtitle text is hex or base64 of the flag).

---

## 10. Geographic Flag
**Category:** OSINT / Misc  
**Difficulty:** Easy-Medium

Provide a set of GPS coordinates (latitude and longitude). When looked up on
Google Maps / OpenStreetMap, the coordinates point to a specific named location.
The first letters of each location name (road, suburb, landmark) in order spell
out the flag, or the place name itself IS the flag (e.g., a street named after
something that encodes the answer).

Multiple coordinates → multiple initials → reassemble into CSEC{...}.

**Why it works:** Players must bridge physical geography with the challenge; the
decoding step (initial letters of place names) is not obvious until they visit the
first location and notice the pattern.

**No Docker or server needed.** The coordinates can be embedded in the challenge
description or a text file.

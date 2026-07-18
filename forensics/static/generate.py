#!/usr/bin/env python3
"""
Generate a WAV file whose spectrogram contains the flag as readable text.

Technique: for each pixel in a text-rendered image, synthesise a sine wave
burst at the corresponding frequency and time position. The result sounds like
noise but reveals the flag when viewed in Audacity (spectrogram mode) or
plotted with scipy / matplotlib.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
import os, sys

SAMPLE_RATE = 22050
FREQ_MIN    = 1000   # Hz — bottom of the text band
FREQ_MAX    = 8000   # Hz — top of the text band
SAMPLES_PER_COL = 256  # audio samples per image column (time resolution)
IMG_HEIGHT  = 120    # pixel rows = frequency resolution


def load_font(size: int):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def render_text_image(text: str, height: int, font) -> np.ndarray:
    """Return a (height, width) uint8 array with white text on black."""
    dummy_draw = ImageDraw.Draw(Image.new('L', (1, 1)))
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    padding = 30
    width = text_w + 2 * padding

    img = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(img)
    y = (height - text_h) // 2
    draw.text((padding, y), text, fill=255, font=font)
    return np.array(img).astype(np.float32)


def image_to_audio(img: np.ndarray) -> np.ndarray:
    """Synthesise audio whose spectrogram mirrors the given grayscale image."""
    h, w = img.shape
    n_samples = w * SAMPLES_PER_COL
    audio = np.zeros(n_samples, dtype=np.float64)

    for row in range(h):
        # Row 0 in PIL = top of image = FREQ_MAX; row h-1 = FREQ_MIN
        freq = FREQ_MAX - (row / h) * (FREQ_MAX - FREQ_MIN)
        # Per-column amplitude envelope
        amplitude_cols = img[row] / 255.0          # shape (w,)
        envelope = np.repeat(amplitude_cols, SAMPLES_PER_COL)  # shape (n_samples,)
        t = np.arange(n_samples) / SAMPLE_RATE
        audio += 0.04 * envelope * np.sin(2.0 * np.pi * freq * t)

    # Mild background hiss so the silence outside the text isn't a giveaway
    audio += np.random.normal(0, 0.006, n_samples)

    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.75

    return audio


def main():
    flag = os.environ.get('FLAG', 'CSEC{placeholder_change_me}')
    out  = os.environ.get('OUTPUT', '/data/challenge.wav')

    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)

    font  = load_font(22)
    img   = render_text_image(flag, IMG_HEIGHT, font)
    audio = image_to_audio(img)

    audio_i16 = (audio * 32767).astype(np.int16)
    wavfile.write(out, SAMPLE_RATE, audio_i16)
    print(f'Generated {out}  ({len(audio_i16)/SAMPLE_RATE:.1f}s, {audio_i16.shape[0]} samples)')


if __name__ == '__main__':
    main()

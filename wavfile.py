#!/usr/bin/python3
import numpy as np
import sys, wave

# Read a tone from a wave file.
def read_wave(filename):
    w = wave.open(filename, "rb")
    info = w.getparams()
    fbytes = w.readframes(info.nframes)
    w.close()
    sampletypes = {
        1: np.uint8,
        2: np.int16,
        4: np.int32,
    }
    if info.sampwidth not in sampletypes:
        raise IOException(f"unsupported sample width {info.swampwidth}")
    sampletype = sampletypes[info.sampwidth]
    samples = np.frombuffer(fbytes, dtype=sampletype)
    frames = np.reshape(samples, (-1, info.nchannels))
    return (info, frames)

inner = False
for fname in sys.argv[1:]:
    if inner:
        print()
    else:
        inner = True

    try:
        info, wav = read_wave(fname)
    except Exception as e:
        print(f"{fname}: {e}")
        continue
    print(f"name={fname}")
    print(f"channels={info.nchannels}")
    print(f"framerate={info.framerate}")
    print(f"samplewidth={8 * info.sampwidth}")
    print(f"frames={info.nframes}")
    formats = {
        1: ("u8", -128, 128),
        2: ("s16L", -0x8000, 0),
        4: ("s32L", -0x80000000, 0)
    }
    if info.sampwidth not in formats:
        continue
    format_name, format_min, format_mid = formats[info.sampwidth]
    print(f"format={format_name}")
    samples = wav.reshape(-1)

    sample_min = np.min(samples)
    print(f"min={sample_min}")
    splo = (sample_min - format_mid) / format_min
    if splo > 0:
        print(f"min_fraction={splo:.3}")

    sample_max = np.max(samples)
    print(f"max={sample_max}")
    format_max = -format_min - 1
    sphi = (sample_max - format_mid) / format_max
    if sphi > 0:
        print(f"max_fraction={sphi:.3}")

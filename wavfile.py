#!/usr/bin/python3
from collections import namedtuple
import numpy as np
import sys, soundfile
WaveInfo = namedtuple(
    "WaveInfo",
    "nchannels samptype sampwidth sampbytes framerate nframes",
)

# Read a tone from a wave file.
def read_wave(filename):
    with soundfile.SoundFile(filename) as f:
        if f.format != 'WAV':
            raise IOException(f"unknown file format {f.format}")
        nchannels = f.channels
        framerate = f.samplerate
        nframes = f.frames
        if f.subtype.startswith('PCM_'):
            samptype = 'fixed'
            sampwidth = int(f.subtype[4:])
            if sampwidth <= 8:
                sampbytes = 1
                dtype = 'uint8'
            elif sampwidth <= 16:
                sampbytes = 2
                dtype = 'int16'
            elif sampwidth <= 32:
                sampbytes = 4
                dtype = 'int32'
            else:
                raise IOException(f"unknown PCM size {nbits}")
            data = f.read(dtype=dtype, always_2d=True)
        elif f.subtype == 'FLOAT':
            samptype = 'float'
            sampwidth = 32
            sampbytes = 4
            data = f.read(dtype='float32', always_2d=True)
        elif f.subtype == 'DOUBLE':
            samptype = 'float'
            sampwidth = 64
            sampbytes = 8
            data = f.read(dtype='float64', always_2d=True)
        else:
            raise IOException(f"unknown sample type {info.subtype}")
    info = WaveInfo(
        nchannels,
        samptype,
        sampwidth,
        sampbytes,
        framerate,
        nframes,
    )
    return (info, data)

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
    print(f"format={info.samptype}")
    print(f"samplewidth={info.sampwidth}")
    print(f"frames={info.nframes}")
    samples = wav.reshape(-1)

    format_mid = 0
    if info.samptype == 'fixed':
        if info.sampbytes == 1:
            format_mid = 1 << (info.sampwidth - 1)
            format_min = 0
            format_max = (1 << info.sampwidth) - 1
        else:
            format_min = -(1 << (info.sampwidth - 1))
            format_max = -format_min + 1
    elif info.samptype == 'float':
        format_min = -1.0
        format_max = 1.0
    else:
        continue

    sample_min = np.min(samples)
    print(f"min={sample_min}")
    splo = (sample_min - format_mid) / format_min
    if splo > 0:
        print(f"min_fraction={splo:.3}")

    sample_max = np.max(samples)
    print(f"max={sample_max}")
    sphi = (sample_max - format_mid) / format_max
    if sphi > 0:
        print(f"max_fraction={sphi:.3}")

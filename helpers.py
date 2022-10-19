

def infinite_bpm_sequence(bpm):
    """Generate an infinite series of BPM time values."""

    beat_time = 60/bpm
    sixteenth_time = beat_time / 4
    current_time = 0

    while True:
        current_time = current_time + sixteenth_time
        yield current_time
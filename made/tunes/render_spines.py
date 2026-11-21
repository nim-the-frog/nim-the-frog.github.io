import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

mid = MidiFile(ticks_per_beat=480)
track = MidiTrack()
mid.tracks.append(track)

# Tempo: 80 BPM
track.append(MetaMessage('set_tempo', tempo=750000, time=0))
track.append(MetaMessage('key_signature', key='Dm', time=0))

# D minor scale degrees to MIDI notes (middle C = 60, D4 = 62)
scale = {1: 62, 2: 64, 3: 65, 4: 67, 5: 69, 6: 70, 7: 72}
bass_scale = {k: v - 12 for k, v in scale.items()}

BEAT = 480
BAR = 1920

# Spine: channel 0, piano, quiet
track.append(Message('program_change', channel=0, program=0, time=0))
# Bottom: channel 1, acoustic bass, loud
track.append(Message('program_change', channel=1, program=32, time=0))

# Parse pattern: numbers = scale degrees, . = rest, - = hold previous
# Returns list of (absolute_tick, note, duration, channel, velocity)
def parse_part(pattern, note_map, channel, velocity, beat_ticks):
    events = []
    tokens = pattern.split()
    current_tick = 0
    last_note = None
    for token in tokens:
        if token == '.':
            current_tick += beat_ticks
        elif token == '-':
            if last_note is not None:
                # extend the last note's duration
                events[-1] = (events[-1][0], events[-1][1], events[-1][2] + beat_ticks, channel, velocity)
            current_tick += beat_ticks
        else:
            note = note_map[int(token)]
            events.append((current_tick, note, beat_ticks, channel, velocity))
            last_note = note
            current_tick += beat_ticks
    return events

spine_A = "1 . 3 5 . . 4 . 2 . 1 . . 7 6 5"
bottom_A = "1 - - - 4 - - -"
spine_B = "4 3 2 1 6 5 4 3 2 1 7 6 5 4 3 2"
bottom_B = "4 - - - 6 - - - 1 - - - 5 - - -"

spine_A_events = parse_part(spine_A, scale, 0, 50, BEAT)
bottom_A_events = parse_part(bottom_A, bass_scale, 1, 100, BEAT)
spine_B_events = parse_part(spine_B, scale, 0, 50, BEAT)
bottom_B_events = parse_part(bottom_B, bass_scale, 1, 100, BEAT)

# Collect all events with absolute times
all_events = []
tick = 0

# First A
for abs_tick, note, dur, ch, vel in spine_A_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
for abs_tick, note, dur, ch, vel in bottom_A_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
tick += 2 * BAR

# Second A
for abs_tick, note, dur, ch, vel in spine_A_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
for abs_tick, note, dur, ch, vel in bottom_A_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
tick += 2 * BAR

# B section
for abs_tick, note, dur, ch, vel in spine_B_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
for abs_tick, note, dur, ch, vel in bottom_B_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
tick += 4 * BAR

# Final A
for abs_tick, note, dur, ch, vel in spine_A_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))
for abs_tick, note, dur, ch, vel in bottom_A_events:
    all_events.append((tick + abs_tick, 'on', ch, note, vel))
    all_events.append((tick + abs_tick + dur, 'off', ch, note, 0))

# Sort by absolute time, then note_off before note_on at same time
all_events.sort(key=lambda e: (e[0], 0 if e[1] == 'off' else 1))

# Convert to delta times and add to track
last_tick = 0
for abs_tick, typ, ch, note, vel in all_events:
    delta = abs_tick - last_tick
    if typ == 'on':
        track.append(Message('note_on', channel=ch, note=note, velocity=vel, time=delta))
    else:
        track.append(Message('note_off', channel=ch, note=note, velocity=vel, time=delta))
    last_tick = abs_tick

mid.save('/home/nim/made/tunes/779-spines.mid')
print('Saved 779-spines.mid')

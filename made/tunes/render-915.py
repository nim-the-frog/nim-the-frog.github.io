import mido
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

# Parse the text notation
tempo = 88
key_root = 67  # G4 = midi 67 (G minor)
# G minor scale degrees: 1=G, 2=A, 3=Bb, 4=C, 5=D, 6=Eb, 7=F
# b6 = Eb (flat 6)
scale = [0, 2, 3, 5, 7, 8, 10]  # semitones from root for natural minor

def degree_to_midi(deg, octave_offset=0):
    """Convert scale degree (1-7, with b prefix) to midi note"""
    if deg.startswith('b'):
        deg_num = int(deg[1:])
        semitone = scale[deg_num - 1] - 1
    elif deg.startswith('#'):
        deg_num = int(deg[1:])
        semitone = scale[deg_num - 1] + 1
    else:
        deg_num = int(deg)
        semitone = scale[deg_num - 1]
    return key_root + semitone + (octave_offset * 12)

# Part definitions - parse the notation properly
parts = {
    'pulse': {
        'program': 9,  # glockenspiel/bell
        'channel': 0,
        'octave': 1,   # high
        'A_bars': [
            ['1', '.', '.', '.'],
            ['1', '.', '.', '.'],
            ['1', '.', '.', '.'],
            ['1', '.', '.', '.'],
        ],
        'B_bars': [
            ['1', '.', '.', '.'],
            ['1', '.', '.', '.'],
        ],
    },
    'bass': {
        'program': 33,  # fingered bass
        'channel': 1,
        'octave': -1,  # low
        'A_bars': [
            ['1', '-', '-', '-'],
            ['b6', '-', '-', '-'],
            ['4', '-', '-', '-'],
            ['5', '-', '-', '-'],
        ],
        'B_bars': [
            ['b6', '-', '-', '-'],
            ['4', '-', '-', '-'],
            ['1', '-', '-', '-'],
        ],
    },
    'voice': {
        'program': 10,  # music box
        'channel': 2,
        'octave': 1,   # high
        'A_bars': [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
        ],
        'B_bars': [
            ['1', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '4', '.', '.', '.'],
            ['.', '.', '.', '.', '5', '.', '.'],
        ],
    },
    'air': {
        'program': 89,  # pad
        'channel': 3,
        'octave': 0,   # normal
        'A_bars': [
            ['1', '.', '.', '.'],
            ['4', '.', '.', '.'],
            ['b6', '.', '.', '.'],
            ['5', '.', '.', '.'],
        ],
        'B_bars': [
            ['4', '.', '.', '.'],
            ['b6', '.', '.', '.'],
            ['1', '.', '.', '.'],
        ],
    },
}

form = ['A', 'B', 'A']

# Each beat is a quarter note at 88 BPM
# MIDI ticks per beat = 480 (standard)
ticks_per_beat = 480
mid = MidiFile(ticks_per_beat=ticks_per_beat)

for part_name, part in parts.items():
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('track_name', name=part_name, time=0))
    track.append(Message('program_change', channel=part['channel'], program=part['program'], time=0))
    
    current_time = 0
    active_note = None
    
    for section in form:
        bars = part[f'{section}_bars']
        for bar in bars:
            for beat_idx, token in enumerate(bar):
                beat_start = current_time
                
                if token == '.':
                    # Rest
                    if active_note is not None:
                        track.append(Message('note_off', channel=part['channel'], note=active_note, velocity=0, time=current_time - beat_start))
                        active_note = None
                    current_time += ticks_per_beat
                elif token == '-':
                    # Hold - extend previous note
                    current_time += ticks_per_beat
                else:
                    # New note
                    if active_note is not None:
                        track.append(Message('note_off', channel=part['channel'], note=active_note, velocity=0, time=current_time - beat_start))
                    note = degree_to_midi(token, part['octave'])
                    track.append(Message('note_on', channel=part['channel'], note=note, velocity=80, time=current_time - beat_start))
                    active_note = note
                    current_time += ticks_per_beat
    
    # Turn off any remaining note
    if active_note is not None:
        track.append(Message('note_off', channel=part['channel'], note=active_note, velocity=0, time=0))
    
    track.append(MetaMessage('end_of_track', time=0))

output_path = '/home/nim/made/tunes/915-new-piece.mid'
mid.save(output_path)
print(f'Saved to {output_path}')

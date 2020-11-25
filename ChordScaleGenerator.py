from music21 import stream, chord, meter, pitch
import numpy as np
import copy
from enum import Enum

"""cycle matrices - these data structures contain the distances each chord tone should move to based on the patterns
derived from the different cycles, they will have to be expanded once support for four note chords is added. the order
in each row is top, middle, bottom."""

cycle2matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle2matrix[0, 0, :] = [-2, -1, -1]
cycle2matrix[0, 1, :] = [-1, -2, -1]
cycle2matrix[0, 2, :] = [-1, -1, -2]

cycle2matrix[1, 0, :] = cycle2matrix[0, 2, :]
cycle2matrix[1, 1, :] = cycle2matrix[0, 0, :]
cycle2matrix[1, 2, :] = cycle2matrix[0, 1, :]

cycle2matrix[2, 0, :] = cycle2matrix[0, 1, :]
cycle2matrix[2, 1, :] = cycle2matrix[0, 2, :]
cycle2matrix[2, 2, :] = cycle2matrix[0, 0, :]

# it is possible to define these matrices all based on the cycle2 ones defined previously, however for the sake of
# clarity and debugging it defining the first one separately was chosen
cycle7matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle7matrix[0, 0, :] = [1, 1, 2]
cycle7matrix[0, 1, :] = [1, 2, 1]
cycle7matrix[0, 2, :] = [2, 1, 1]

cycle7matrix[1, 0, :] = cycle7matrix[0, 1, :]
cycle7matrix[1, 1, :] = cycle7matrix[0, 2, :]
cycle7matrix[1, 2, :] = cycle7matrix[0, 0, :]

cycle7matrix[2, 0, :] = cycle7matrix[0, 2, :]
cycle7matrix[2, 1, :] = cycle7matrix[0, 0, :]
cycle7matrix[2, 2, :] = cycle7matrix[0, 1, :]

cycle4matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle4matrix[0, 0, :] = [0, 1, 1]
cycle4matrix[0, 1, :] = [1, 0, 1]
cycle4matrix[0, 2, :] = [1, 1, 0]

cycle4matrix[1, 0, :] = cycle4matrix[0, 2, :]
cycle4matrix[1, 1, :] = cycle4matrix[0, 0, :]
cycle4matrix[1, 2, :] = cycle4matrix[0, 1, :]

cycle4matrix[2, 0, :] = cycle4matrix[0, 1, :]
cycle4matrix[2, 1, :] = cycle4matrix[0, 2, :]
cycle4matrix[2, 2, :] = cycle4matrix[0, 0, :]

cycle5matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle5matrix[0, 0, :] = [-1, -1, 0]
cycle5matrix[0, 1, :] = [-1, 0, -1]
cycle5matrix[0, 2, :] = [0, -1, -1]

cycle5matrix[1, 0, :] = cycle5matrix[0, 1, :]
cycle5matrix[1, 1, :] = cycle5matrix[0, 2, :]
cycle5matrix[1, 2, :] = cycle5matrix[0, 0, :]

cycle5matrix[2, 0, :] = cycle5matrix[0, 2, :]
cycle5matrix[2, 1, :] = cycle5matrix[0, 0, :]
cycle5matrix[2, 2, :] = cycle5matrix[0, 1, :]

cycle3matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle3matrix[0, 0, :] = [-1, 0, 0]
cycle3matrix[0, 1, :] = [0, -1, 0]
cycle3matrix[0, 2, :] = [0, 0, -1]

cycle3matrix[1, 0, :] = cycle3matrix[0, 2, :]
cycle3matrix[1, 1, :] = cycle3matrix[0, 0, :]
cycle3matrix[1, 2, :] = cycle3matrix[0, 1, :]

cycle3matrix[2, 0, :] = cycle3matrix[0, 1, :]
cycle3matrix[2, 1, :] = cycle3matrix[0, 2, :]
cycle3matrix[2, 2, :] = cycle3matrix[0, 0, :]

cycle6matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle6matrix[0, 0, :] = [0, 0, 1]
cycle6matrix[0, 1, :] = [0, 1, 0]
cycle6matrix[0, 2, :] = [1, 0, 0]

cycle6matrix[1, 0, :] = cycle6matrix[0, 1, :]
cycle6matrix[1, 1, :] = cycle6matrix[0, 2, :]
cycle6matrix[1, 2, :] = cycle6matrix[0, 0, :]

cycle6matrix[2, 0, :] = cycle6matrix[0, 2, :]
cycle6matrix[2, 1, :] = cycle6matrix[0, 0, :]
cycle6matrix[2, 2, :] = cycle6matrix[0, 1, :]


class Voicing(Enum):
    Closed = 1
    Drop2 = 2


class Range:
    class ReturnValue(Enum):
        BelowRange = -1
        InRange = 0
        AboveRange = 1

    def __init__(self, lowest_pitch, highest_pitch):
        self.lowest_pitch = lowest_pitch
        self.highest_pitch = highest_pitch

    def is_pitch_in_range(self, p):
        if p.ps > self.highest_pitch.ps:
            return Range.ReturnValue.AboveRange
        elif p.ps < self.lowest_pitch.ps:
            return Range.ReturnValue.BelowRange
        else:
            return Range.ReturnValue.InRange


# class GuitarRange:
#     # this class is used to limit the chord voicings to keep them from open strings to the 14th fret
#     E_string_low = Range(pitch.Pitch('E2'), pitch.Pitch('F#3'))
#     A_string = Range(pitch.Pitch('A2'), pitch.Pitch('B3'))
#     D_string = Range(pitch.Pitch('D3'), pitch.Pitch('E4'))
#     G_string = Range(pitch.Pitch('G3'), pitch.Pitch('A4'))
#     B_string = Range(pitch.Pitch('B3'), pitch.Pitch('C#5'))
#     E_string_high = Range(pitch.Pitch('E4'), pitch.Pitch('F#5'))

class GuitarRange:
    # this class is used to limit the chord voicings to keep them from open strings to the 14th fret
    # the note values here correspond to how guitar is notated as opposed to how it's actually pitched
    E_string_low = Range(pitch.Pitch('E3'), pitch.Pitch('G4'))
    A_string = Range(pitch.Pitch('A3'), pitch.Pitch('C5'))
    D_string = Range(pitch.Pitch('D4'), pitch.Pitch('F5'))
    G_string = Range(pitch.Pitch('G4'), pitch.Pitch('Bb5'))
    B_string = Range(pitch.Pitch('B4'), pitch.Pitch('D6'))
    E_string_high = Range(pitch.Pitch('E5'), pitch.Pitch('G6'))


guitar_range = [
    Range(pitch.Pitch('E2'), pitch.Pitch('F#3')),
    Range(pitch.Pitch('A2'), pitch.Pitch('B3')),
    Range(pitch.Pitch('D3'), pitch.Pitch('E4')),
    Range(pitch.Pitch('G3'), pitch.Pitch('A4')),
    Range(pitch.Pitch('B3'), pitch.Pitch('C#5')),
    Range(pitch.Pitch('E4'), pitch.Pitch('F#5'))
]


def transpose_chord_as_list(chord_as_list, interval):
    for chord_tone in chord_as_list:
        chord_tone.transpose(interval, inPlace=True)


def apply_row_to_chord(row, chord_as_list, sc):
    for j in range(0, len(chord_as_list)):
        if row[j] == 0:
            continue
        elif row[j] < 0:
            chord_as_list[j] = sc.next(chord_as_list[j], 'descending', abs(row[j]))
        else:
            chord_as_list[j] = sc.next(chord_as_list[j], 'ascending', row[j])


def generate_drop2_matrix_page(cycle_matrix_page):
    # given that a drop 2 triad has the order of chord tones changed, modify the cycle matrix to adjust accordingly.
    # this equates to swapping the columns as the columns indicate the position of the note in the chord but since it's
    # still following the same pattern of half/whole steps
    # TODO: figure out how to to this with matrix operations/multiplication
    drop2_matrix_page = np.zeros((3, 3), dtype=np.int)
    drop2_matrix_page[:, 0] = cycle_matrix_page[:, 0]
    drop2_matrix_page[:, 1] = cycle_matrix_page[:, 2]
    drop2_matrix_page[:, 2] = cycle_matrix_page[:, 1]

    return drop2_matrix_page


def generate_sub_cycle(starting_chord, cycle_matrix_page, sc):
    # TODO: Clean up the names of the arguments here
    chord_as_list = list(starting_chord.pitches)
    measure = stream.Measure()
    # make it a 7/4 measure as there are 7 chords to a sub-cycle
    # measure.append(meter.TimeSignature('7/4'))
    # add the first chord before generating the rest of the cycle
    measure.append(chord.Chord(starting_chord))

    # apply the rules of the cycle matrix to generate the rest of the chords. since we're dealing with diatonic chords
    # at the moment, the cycle will need to be run twice to generate the remaining six chords
    for i in range(0, 2):
        for row in cycle_matrix_page:
            apply_row_to_chord(row, chord_as_list, sc)
            measure.append(chord.Chord(chord_as_list))
    return measure


# def generate_full_cycle(starting_chord, cycle_matrix_page, sc):
#     # the starting chord is set to the last chord produced by the cycle
#     full_cycle = stream.Stream()
#     full_cycle.append(meter.TimeSignature('7/4'))
#
#     chord_as_list = list(starting_chord.pitches)
#
#     # lets start generating the cycle
#     full_cycle.append(starting_chord)
#     # the length of this range could be more generalized to the number of notes in the passed scale
#     for i in range(0, 20):
#         # use modular arithmetic here in preparation for expanding to 7th chords
#         apply_row_to_chord(cycle_matrix_page[i % len(cycle_matrix_page)], chord_as_list, sc)
#         full_cycle.append(chord.Chord(chord_as_list))
#
#     apply_row_to_chord(cycle_matrix_page[20 % len(cycle_matrix_page)], chord_as_list, sc)
#
#     return full_cycle, chord.Chord(chord_as_list)


def generate_full_cycle(starting_chord, cycle_matrix_page, sc, note_range=()):
    # the starting chord is set to the last chord produced by the cycle
    full_cycle = stream.Stream()
    full_cycle.append(meter.TimeSignature('7/4'))

    chord_as_list = list(starting_chord.pitches)

    # lets start generating the cycle
    full_cycle.append(starting_chord)
    # the length of this range could be more generalized to the number of notes in the passed scale
    for i in range(0, 20):
        # use modular arithmetic here in preparation for expanding to 7th chords
        apply_row_to_chord(cycle_matrix_page[i % len(cycle_matrix_page)], chord_as_list, sc)
        # check to see if the new chord is within the specified range if ranges are specified
        if len(note_range) != 0:
            for string, chord_tone in zip(note_range, chord_as_list):
                ret = string.is_pitch_in_range(chord_tone)
                if ret == Range.ReturnValue.BelowRange:
                    # transpose the chord up an octave
                    transpose_chord_as_list(chord_as_list, 12)
                    break
                elif ret == Range.ReturnValue.AboveRange:
                    transpose_chord_as_list(chord_as_list, -12)
                    break
        # add the chord to the cycle since it should be in the specified range now
        full_cycle.append(chord.Chord(chord_as_list))

    apply_row_to_chord(cycle_matrix_page[20 % len(cycle_matrix_page)], chord_as_list, sc)

    return full_cycle, chord.Chord(chord_as_list)


# def generate_cycle_pairs2(starting_chord, sc, pair_type, voicing_type=Voicing.Closed):
#     # Todo: Re-write this to use a reversing scheme to make this even more generic as a pair of cycles really is just
#     #  one cycle follow the its reverse
#     cycle_pair = stream.Stream()
#
#     if pair_type == "2/7":
#         first_cycle_matrix_page = cycle2matrix[:, :, 0]
#         second_cycle_matrix_page = cycle7matrix[:, :, 0]
#     elif pair_type == "4/5":
#         first_cycle_matrix_page = cycle4matrix[:, :, 0]
#         second_cycle_matrix_page = cycle5matrix[:, :, 0]
#     elif pair_type == "3/6":
#         first_cycle_matrix_page = cycle3matrix[:, :, 0]
#         second_cycle_matrix_page = cycle6matrix[:, :, 0]
#     else:
#         raise Exception("pair_type passed is an invalid value")
#
#     if voicing_type == Voicing.Drop2:
#         first_cycle_matrix_page = generate_drop2_matrix_page(first_cycle_matrix_page)
#         second_cycle_matrix_page = generate_drop2_matrix_page(second_cycle_matrix_page)
#
#     first_cycle, next_chord = generate_full_cycle(copy.deepcopy(starting_chord), first_cycle_matrix_page, sc)
#     second_cycle = generate_full_cycle(next_chord, second_cycle_matrix_page, sc)[0]
#
#     cycle_pair.append(first_cycle)
#     cycle_pair.append(second_cycle)
#
#     return cycle_pair


def generate_cycle_pairs(starting_chord, sc, pair_type, string_ranges=(), voicing_type=Voicing.Closed):
    # Todo: clean up the variable names here to be more accurate
    cycle_pair = stream.Stream()

    if pair_type == "2/7":
        first_cycle_matrix_page = cycle2matrix[:, :, 0]
        second_cycle_matrix_page = cycle7matrix[:, :, 0]
    elif pair_type == "4/5":
        first_cycle_matrix_page = cycle4matrix[:, :, 0]
        second_cycle_matrix_page = cycle5matrix[:, :, 0]
    elif pair_type == "3/6":
        first_cycle_matrix_page = cycle3matrix[:, :, 0]
        second_cycle_matrix_page = cycle6matrix[:, :, 0]
    else:
        raise Exception("pair_type passed is an invalid value")

    if voicing_type == Voicing.Drop2:
        first_cycle_matrix_page = generate_drop2_matrix_page(first_cycle_matrix_page)
        second_cycle_matrix_page = generate_drop2_matrix_page(second_cycle_matrix_page)

    first_cycle, next_chord = generate_full_cycle(copy.deepcopy(starting_chord), first_cycle_matrix_page, sc, string_ranges)
    second_cycle = generate_full_cycle(next_chord, second_cycle_matrix_page, sc, string_ranges)[0]

    cycle_pair.append(first_cycle)
    cycle_pair.append(second_cycle)

    return cycle_pair

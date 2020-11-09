from music21 import stream, chord, meter
import numpy as np
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


def apply_row_to_chord(row, chord_as_list, sc):
    for j in range(0, len(chord_as_list)):
        if row[j] == 0:
            continue
        elif row[j] < 0:
            chord_as_list[j] = sc.next(chord_as_list[j], 'descending', abs(row[j]))
        else:
            chord_as_list[j] = sc.next(chord_as_list[j], 'ascending', row[j])


def generate_drop2_matrix(cycle_matrix):
    # given that a drop 2 triad has the order of chord tones changed, modify the cycle matrix to adjust accordingly.
    # this equates to swapping the columns as the columns indicate the position of the note in the chord but since it's
    # still following the same pattern of half/whole steps
    # TODO: figure out how to to this with matrix operations/multiplication
    drop2_matrix = np.zeros((3, 3), dtype=np.int)
    drop2_matrix[:, 0] = cycle_matrix[:, 0]
    drop2_matrix[:, 1] = cycle_matrix[:, 2]
    drop2_matrix[:, 2] = cycle_matrix[:, 1]

    return drop2_matrix


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


def generate_full_cycle(starting_chord, cycle_matrix, sc):
    # starting chord should be in root position
    full_cycle = stream.Stream()
    if (cycle_matrix == cycle2matrix).all() or (cycle_matrix == cycle3matrix).all() or (cycle_matrix == cycle4matrix).all():
        starting_chord.inversion(0)
        full_cycle.append(generate_sub_cycle(starting_chord.transpose(0), cycle_matrix[0], sc))

        starting_chord.inversion(2)
        # take it down an octave as the inversion() method only creates inversions in the "ascending manner"
        full_cycle.append(generate_sub_cycle(starting_chord.transpose(-12), cycle_matrix[2], sc))

        starting_chord.inversion(1)
        # -24 is used here for the transposition to counter act the inversions being done out of order
        full_cycle.append(generate_sub_cycle(starting_chord.transpose(-24), cycle_matrix[1], sc))
    elif (cycle_matrix == cycle5matrix).all() or (cycle_matrix == cycle6matrix).all() or (cycle_matrix == cycle7matrix).all():
        starting_chord.inversion(0)
        full_cycle.append(generate_sub_cycle(starting_chord.transpose(0), cycle_matrix[0], sc))

        starting_chord.inversion(1)
        full_cycle.append(generate_sub_cycle(starting_chord.transpose(0), cycle_matrix[1], sc))

        starting_chord.inversion(2)
        full_cycle.append(generate_sub_cycle(starting_chord.transpose(0), cycle_matrix[2], sc))
    else:
        raise Exception("cycle_matrix passed doesn't match any of the pre-defined patterns")

    return full_cycle


def generate_full_cycle2(starting_chord, cycle_matrix_page, sc):
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
        full_cycle.append(chord.Chord(chord_as_list))

    apply_row_to_chord(cycle_matrix_page[20 % len(cycle_matrix_page)], chord_as_list, sc)

    return full_cycle, chord.Chord(chord_as_list)


def generate_cycle_pairs(starting_chord, sc, pair_type):
    cycle_pair = stream.Stream()
    # cycle_pair.append(meter.TimeSignature('7/4')) # 7/4 as there are 7 chords to each sub-cycle

    if pair_type == "2/7":
        cycle2, next_chord = generate_full_cycle2(starting_chord.transpose(0), cycle2matrix[:, :, 0], sc)
        cycle7 = generate_full_cycle2(next_chord, cycle7matrix[:, :, 0], sc)[0]
        cycle_pair.append(cycle2)
        cycle_pair.append(cycle7)
    elif pair_type == "4/5":
        cycle4, next_chord = generate_full_cycle2(starting_chord.transpose(0), cycle4matrix[:, :, 0], sc)
        cycle5 = generate_full_cycle2(next_chord, cycle5matrix[:, :, 0], sc)[0]
        cycle_pair.append(cycle4)
        cycle_pair.append(cycle5)
    elif pair_type == "3/6":
        cycle3, next_chord = generate_full_cycle2(starting_chord.transpose(0), cycle3matrix[:, :, 0], sc)
        cycle6 = generate_full_cycle2(next_chord, cycle6matrix[:, :, 0], sc)[0]
        cycle_pair.append(cycle3)
        cycle_pair.append(cycle6)
    else:
        raise Exception("pair_type passed is an invalid value")
    return cycle_pair

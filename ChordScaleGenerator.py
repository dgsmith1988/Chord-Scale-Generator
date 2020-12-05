from music21 import stream, chord, meter, pitch, metadata, layout
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

# cycle3matrix = np.zeros((3, 3, 3), dtype=np.int)
# cycle3matrix[0, 0, :] = [-1, 0, 0]
# cycle3matrix[0, 1, :] = [0, -1, 0]
# cycle3matrix[0, 2, :] = [0, 0, -1]
#
# cycle3matrix[1, 0, :] = cycle3matrix[0, 2, :]
# cycle3matrix[1, 1, :] = cycle3matrix[0, 0, :]
# cycle3matrix[1, 2, :] = cycle3matrix[0, 1, :]
#
# cycle3matrix[2, 0, :] = cycle3matrix[0, 1, :]
# cycle3matrix[2, 1, :] = cycle3matrix[0, 2, :]
# cycle3matrix[2, 2, :] = cycle3matrix[0, 0, :]

cycle3matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle3matrix[0, 0, :] = [-1, 0, 0]
cycle3matrix[0, 1, :] = [0, -1, 0]
cycle3matrix[0, 2, :] = [0, 0, -1]

cycle3matrix[2, 0, :] = cycle3matrix[0, 2, :]
cycle3matrix[2, 1, :] = cycle3matrix[0, 0, :]
cycle3matrix[2, 2, :] = cycle3matrix[0, 1, :]

cycle3matrix[1, 0, :] = cycle3matrix[0, 1, :]
cycle3matrix[1, 1, :] = cycle3matrix[0, 2, :]
cycle3matrix[1, 2, :] = cycle3matrix[0, 0, :]

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


class NoteRange:
    class ReturnValue(Enum):
        BelowRange = -1
        InRange = 0
        AboveRange = 1

    def __init__(self, lowest_pitch, highest_pitch):
        self.lowest_pitch = lowest_pitch
        self.highest_pitch = highest_pitch

    def is_pitch_in_range(self, p):
        if p.ps > self.highest_pitch.ps:
            return NoteRange.ReturnValue.AboveRange
        elif p.ps < self.lowest_pitch.ps:
            return NoteRange.ReturnValue.BelowRange
        else:
            return NoteRange.ReturnValue.InRange


class GuitarString(NoteRange):
    # Todo: Rethink this name for the class
    class StringNumber(Enum):
        E_string_low = 6
        A_string = 5
        D_string = 4
        G_string = 3
        B_string = 2
        E_string_high = 1

    def __init__(self, lowest_pitch, highest_pitch, number):
        self.number = number
        NoteRange.__init__(self, lowest_pitch, highest_pitch)


class GuitarRange:
    # this class is used to limit the chord voicings to keep them from open strings to the 14th fret. the note values
    # here correspond to how guitar is notated as opposed to how it's actually pitched to make reading the scores easier
    E_string_low = GuitarString(pitch.Pitch('E3'), pitch.Pitch('G4'), GuitarString.StringNumber.E_string_low)
    A_string = GuitarString(pitch.Pitch('A3'), pitch.Pitch('C5'), GuitarString.StringNumber.A_string)
    D_string = GuitarString(pitch.Pitch('D4'), pitch.Pitch('F5'), GuitarString.StringNumber.D_string)
    G_string = GuitarString(pitch.Pitch('G4'), pitch.Pitch('Bb5'), GuitarString.StringNumber.G_string)
    B_string = GuitarString(pitch.Pitch('B4'), pitch.Pitch('D6'), GuitarString.StringNumber.B_string)
    E_string_high = GuitarString(pitch.Pitch('E5'), pitch.Pitch('G6'), GuitarString.StringNumber.E_string_high)

    @staticmethod
    def get_string(string_number):
        if string_number < 1 or string_number > 6:
            raise Exception("index passed needs to be between 1 and 6")
        elif string_number == GuitarString.StringNumber.E_string_high.value:
            return GuitarRange.E_string_high
        elif string_number == GuitarString.StringNumber.B_string.value:
            return GuitarRange.B_string
        elif string_number == GuitarString.StringNumber.G_string.value:
            return GuitarRange.G_string
        elif string_number == GuitarString.StringNumber.D_string.value:
            return GuitarRange.D_string
        elif string_number == GuitarString.StringNumber.A_string.value:
            return GuitarRange.A_string
        elif string_number == GuitarString.StringNumber.E_string_low.value:
            return GuitarRange.E_string_low


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


def check_note_ranges_and_transpose(chord_as_list, note_ranges):
    # check to see if the new chord is within the specified range if ranges are specified
    # transpose the pitches in the chord up or down an octave so they match accordingly
    # Todo: consider writing this to be more "intelligent" about how it transposes a chord to an arbitrary range, it
    #  seems as if the transposeAboveTarget() and transposeBelowTarget() would be functions we could use here
    for note_range, chord_tone in zip(note_ranges, chord_as_list):
        is_in_range = note_range.is_pitch_in_range(chord_tone)
        if is_in_range == NoteRange.ReturnValue.BelowRange:
            # transpose the chord up an octave
            transpose_chord_as_list(chord_as_list, 12)
            break
        elif is_in_range == NoteRange.ReturnValue.AboveRange:
            transpose_chord_as_list(chord_as_list, -12)
            break


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


def generate_sub_cycle(root_scale, starting_chord, cycle_matrix_page, note_ranges=()):
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
            apply_row_to_chord(row, chord_as_list, root_scale)
            # check to see if the new chord is within the specified range if ranges are specified
            if len(note_ranges) != 0:
                check_note_ranges_and_transpose(chord_as_list, note_ranges)
            measure.append(chord.Chord(chord_as_list))
    return measure


def generate_sub_cycle_2(root_scale, starting_chord, cycle_matrix_page, note_ranges=()):
    chord_as_list = list(starting_chord.pitches)
    measure = stream.Measure()
    # make it a 7/4 measure as there are 7 chords to a sub-cycle
    measure.append(meter.TimeSignature('7/4'))
    # add the first chord before generating the rest of the cycle
    measure.append(chord.Chord(starting_chord))

    # apply the rules of the cycle matrix to generate the rest of the chords. since we're dealing with diatonic chords
    # at the moment, the cycle will need to be run twice to generate the remaining six chords
    for i in range(0, 2):
        for row in cycle_matrix_page:
            apply_row_to_chord(row, chord_as_list, root_scale)
            # check to see if the new chord is within the specified range if ranges are specified
            if len(note_ranges) != 0:
                check_note_ranges_and_transpose(chord_as_list, note_ranges)
            measure.append(chord.Chord(chord_as_list))

    apply_row_to_chord(cycle_matrix_page[6 % len(cycle_matrix_page)], chord_as_list, root_scale)

    return measure, chord.Chord(chord_as_list)


def generate_full_cycle_2(root_scale, starting_chord, cycle_matrix, note_ranges=()):
    # the starting chord is set to the last chord produced by the cycle
    full_cycle = stream.Stream()

    # the length of this range could be more generalized to the number of notes in the passed scale
    seed_chord = starting_chord
    for i in range(0, 3):
        sub_cycle, next_chord = generate_sub_cycle_2(root_scale, seed_chord, cycle_matrix[i], note_ranges)
        # the time signature is already taken care of in the first measure, so remove it from the sub-sequent measures
        if i > 0:
            sub_cycle.pop(0)
        full_cycle.append(sub_cycle)
        seed_chord = next_chord

    # this was put here as it appears there's a bug in the append() function when adding a measure to a stream where
    # there's a time signature object already
    # full_cycle.insert(0, meter.TimeSignature('7/4'))
    return full_cycle, next_chord


def generate_full_cycle(root_scale, starting_chord, cycle_matrix_page, note_ranges=()):
    # the starting chord is set to the last chord produced by the cycle
    full_cycle = stream.Stream()
    full_cycle.append(meter.TimeSignature('7/4'))

    chord_as_list = list(starting_chord.pitches)

    # lets start generating the cycle
    full_cycle.append(starting_chord)
    # the length of this range could be more generalized to the number of notes in the passed scale
    for i in range(0, 20):
        # use modular arithmetic here in preparation for expanding to 7th chords
        apply_row_to_chord(cycle_matrix_page[i % len(cycle_matrix_page)], chord_as_list, root_scale)
        # check to see if the new chord is within the specified range if ranges are specified
        if len(note_ranges) != 0:
            check_note_ranges_and_transpose(chord_as_list, note_ranges)
        # add the chord to the cycle since it should be in the specified range now
        full_cycle.append(chord.Chord(chord_as_list))

    apply_row_to_chord(cycle_matrix_page[20 % len(cycle_matrix_page)], chord_as_list, root_scale)

    return full_cycle, chord.Chord(chord_as_list)


def generate_cycle_pairs(root_scale, starting_chord, pair_type, note_ranges=(), voicing_type=Voicing.Closed):
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

    first_cycle, next_chord = generate_full_cycle(root_scale, copy.deepcopy(starting_chord), first_cycle_matrix_page,
                                                  note_ranges)
    second_cycle = generate_full_cycle(root_scale, next_chord, second_cycle_matrix_page, note_ranges)[0]

    # add notation to make the score easier to read
    first_cycle[1].lyric = "First cycle starts"
    second_cycle[1].lyric = "Second cycle starts"

    # sl = layout.SystemLayout(isNew=True)
    first_cycle.append(layout.SystemLayout(isNew=True))
    cycle_pair.append(first_cycle)
    # remove the time signature from the second cycle as it will mess up the formatting since the combined stream is
    # flattened when returned
    second_cycle.pop(0)
    cycle_pair.append(second_cycle)

    return cycle_pair


def generate_cycle_pairs2(root_scale, starting_chord, pair_type, note_ranges=(), voicing_type=Voicing.Closed):
    cycle_pair = stream.Stream()

    if pair_type == "2/7":
        first_cycle_matrix = cycle2matrix
        second_cycle_matrix = cycle7matrix
    elif pair_type == "4/5":
        first_cycle_matrix = cycle4matrix
        second_cycle_matrix = cycle5matrix
    elif pair_type == "3/6":
        first_cycle_matrix = cycle3matrix
        second_cycle_matrix = cycle6matrix
    else:
        raise Exception("pair_type passed is an invalid value")

    if voicing_type == Voicing.Drop2:
        first_cycle_matrix = generate_drop2_matrix_page(first_cycle_matrix)
        second_cycle_matrix = generate_drop2_matrix_page(second_cycle_matrix)

    first_cycle, next_chord = generate_full_cycle_2(root_scale, copy.deepcopy(starting_chord), first_cycle_matrix,
                                                    note_ranges)
    second_cycle = generate_full_cycle_2(root_scale, next_chord, second_cycle_matrix, note_ranges)[0]

    # add notation to make the score easier to read
    first_cycle[0][1].lyric = "First cycle starts"
    second_cycle[0][1].lyric = "Second cycle starts"

    # sl = layout.SystemLayout(isNew=True)
    first_cycle.append(layout.SystemLayout(isNew=True))
    cycle_pair.append(first_cycle)
    # remove the time signature from the second cycle as it will mess up the formatting since the combined stream is
    # flattened when returned
    second_cycle[0].pop(0)
    cycle_pair.append(second_cycle)

    return cycle_pair


def generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type):
    for i in range(1, 5):
        string_set = (GuitarRange.get_string(i+2), GuitarRange.get_string(i+1), GuitarRange.get_string(i))
        # generate the starting chord for this particular string set
        triad_root = pitch.Pitch(tonic)
        triad_root.octave = string_set[0].highest_pitch.octave
        triad_root.transposeBelowTarget(string_set[0].highest_pitch, inPlace=True)
        tonic_triad = chord.Chord(root_scale.pitchesFromScaleDegrees([1, 3, 5], triad_root, triad_root.transpose(11)))
        cycle_pair = generate_cycle_pairs(root_scale, tonic_triad, pair_type, string_set)
        cycle_pair.metadata = metadata.Metadata()
        cycle_pair.metadata.title = "Cycle " + pair_type + " Progression in " + root_scale.name + "\nString Set: " + \
            str(string_set[0].number.value) + "-" + str(string_set[1].number.value) + "-" + \
            str(string_set[2].number.value) + " - Closed Triads"
        cycle_pair.metadata.composer = "Graham's Chord Cycle Generation Software"
        cycle_pair.definesExplicitSystemBreaks = True
        cycle_pair.show()
        # cycle_pair.write("MusicXML", "C:\\Temp\\Cycle36_progression3")

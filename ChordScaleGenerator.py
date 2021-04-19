from music21 import stream, chord, meter, pitch, metadata, layout, duration, note
import numpy as np
import copy
from enum import Enum

"""cycle matrices - these data structures contain the distances each chord tone should move to based on the patterns
derived from the different cycles, they will have to be expanded once support for four note chords is added. the order
in each row is top, middle, bottom. the order of the pages corresponds doesn't correspond necessarily to the starting
chord inversion, but more the order of sub_cycles which appear in the cycles naturally"""

cycle2matrix = np.zeros((3, 3, 3), dtype=np.int)
cycle2matrix[0, 0, :] = [-2, -1, -1]
cycle2matrix[0, 1, :] = [-1, -2, -1]
cycle2matrix[0, 2, :] = [-1, -1, -2]

cycle2matrix[1, 0, :] = cycle2matrix[0, 1, :]
cycle2matrix[1, 1, :] = cycle2matrix[0, 2, :]
cycle2matrix[1, 2, :] = cycle2matrix[0, 0, :]

cycle2matrix[2, 0, :] = cycle2matrix[0, 2, :]
cycle2matrix[2, 1, :] = cycle2matrix[0, 0, :]
cycle2matrix[2, 2, :] = cycle2matrix[0, 1, :]


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

cycle4matrix[1, 0, :] = cycle4matrix[0, 1, :]
cycle4matrix[1, 1, :] = cycle4matrix[0, 2, :]
cycle4matrix[1, 2, :] = cycle4matrix[0, 0, :]

cycle4matrix[2, 0, :] = cycle4matrix[0, 2, :]
cycle4matrix[2, 1, :] = cycle4matrix[0, 0, :]
cycle4matrix[2, 2, :] = cycle4matrix[0, 1, :]

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
    Drop2_A_form = 2
    Drop2_B_form = 3

    @staticmethod
    def to_string(voicing):
        if voicing == Voicing.Closed:
            return "Closed"
        elif voicing == Voicing.Drop2_A_form or voicing == Voicing.Drop2_B_form:
            return "Drop 2"
        else:
            raise Exception("invalid voicing passed")


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


class ChordCompareReturn(Enum):
    Lower = -1
    Same = 0
    Higher = 1


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
    # this class is used to limit the chord voicings to keep them from open strings to the 15th fret. the note values
    # here correspond to how guitar is notated as opposed to how it's actually pitched to make reading the scores easier
    E_string_low = GuitarString(pitch.Pitch('F3'), pitch.Pitch('G#4'), GuitarString.StringNumber.E_string_low)
    A_string = GuitarString(pitch.Pitch('Bb3'), pitch.Pitch('C#5'), GuitarString.StringNumber.A_string)
    D_string = GuitarString(pitch.Pitch('D#4'), pitch.Pitch('F#5'), GuitarString.StringNumber.D_string)
    G_string = GuitarString(pitch.Pitch('G#4'), pitch.Pitch('B5'), GuitarString.StringNumber.G_string)
    B_string = GuitarString(pitch.Pitch('C5'), pitch.Pitch('E6'), GuitarString.StringNumber.B_string)
    E_string_high = GuitarString(pitch.Pitch('F5'), pitch.Pitch('G#6'), GuitarString.StringNumber.E_string_high)

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


def apply_row_to_chord(row, chord_as_list, sc):
    for j in range(0, len(chord_as_list)):
        if row[j] == 0:
            # continue
            # perform a deep copy here so each chord has a unique instance of it's pitches, otherwise you run into
            # issues when having to transpose chords to fit a range and there are shared pitch objects
            chord_as_list[j] = copy.deepcopy(chord_as_list[j])
        elif row[j] < 0:
            chord_as_list[j] = sc.next(chord_as_list[j], 'descending', abs(row[j]))
        else:
            chord_as_list[j] = sc.next(chord_as_list[j], 'ascending', row[j])


def transpose_chord_as_list(chord_as_list, interval):
    for chord_tone in chord_as_list:
        chord_tone.transpose(interval, inPlace=True)


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


def generate_drop2_matrix(cycle_matrix):
    drop2_matrix = np.zeros((3, 3, 3), dtype=np.int)
    drop2_matrix[0, :, :] = generate_drop2_matrix_page(cycle_matrix[0, :, :])
    drop2_matrix[1, :, :] = generate_drop2_matrix_page(cycle_matrix[1, :, :])
    drop2_matrix[2, :, :] = generate_drop2_matrix_page(cycle_matrix[2, :, :])

    return drop2_matrix


def generate_sub_cycle(root_scale, starting_chord, cycle_matrix_page, note_ranges=()):
    chord_as_list = list(starting_chord.pitches)
    measure = stream.Measure()
    # make it a 7/4 measure as there are 7 chords to a sub-cycle
    measure.append(meter.TimeSignature('7/4'))
    # add the first chord before generating the rest of the cycle
    if len(note_ranges) != 0:
        check_note_ranges_and_transpose(starting_chord.pitches, note_ranges)
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


def generate_full_cycle(root_scale, starting_chord, cycle_matrix, note_ranges=()):
    full_cycle = stream.Stream()

    seed_chord = starting_chord
    for i in range(0, 3):
        sub_cycle, next_chord = generate_sub_cycle(root_scale, seed_chord, cycle_matrix[i], note_ranges)
        # the time signature is already taken care of in the first measure, so remove it from the sub-sequent measures
        if i > 0:
            sub_cycle.pop(0)
        full_cycle.append(sub_cycle)
        seed_chord = next_chord

    return full_cycle, next_chord


def generate_cycle_pair(root_scale, starting_chord, pair_type, note_ranges=(), voicing_type=Voicing.Closed):
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

    if voicing_type == Voicing.Drop2_A_form or voicing_type == Voicing.Drop2_B_form:
        first_cycle_matrix = generate_drop2_matrix(first_cycle_matrix)
        second_cycle_matrix = generate_drop2_matrix(second_cycle_matrix)

    first_cycle, next_chord = generate_full_cycle(root_scale, copy.deepcopy(starting_chord), first_cycle_matrix,
                                                  note_ranges)
    second_cycle = generate_full_cycle(root_scale, next_chord, second_cycle_matrix, note_ranges)[0]

    cycle_pair.append(first_cycle)
    # remove the time signature from the second cycle as it will mess up the formatting
    second_cycle[0].pop(0)
    cycle_pair.append(second_cycle)

    return cycle_pair


def generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing=Voicing.Closed):
    cycle_pairs = []
    for strings in iteration_function(voicing):
        string_set = (GuitarRange.get_string(strings[0]), GuitarRange.get_string(strings[1]), GuitarRange.get_string(strings[2]))

        tonic_triad = generate_tonic_triad(root_scale, tonic, string_set, voicing)

        cycle_pair = generate_cycle_pair(root_scale, tonic_triad, pair_type, string_set, voicing)

        # populate all the metadata to make the titling and everything automatic
        cycle_pair.metadata = metadata.Metadata()
        cycle_pair.metadata.title = "Cycle " + pair_type + " Progression in " + root_scale.name + "\nString Set: " + \
            str(string_set[0].number.value) + "-" + str(string_set[1].number.value) + "-" + \
            str(string_set[2].number.value) + "; " + Voicing.to_string(voicing) + " Triads"
        cycle_pair.metadata.composer = "Graham Smith"
        cycle_pair.metadata.date = "2020"

        # add system breaks at the end each measure to make it one measure per line
        cycle_pair.definesExplicitSystemBreaks = True
        for s in cycle_pair.getElementsByClass(stream.Stream):
            measures = s.getElementsByClass(stream.Measure)
            for m in measures:
                m.append(layout.SystemLayout(isNew=True))
        cycle_pair.definesExplicitSystemBreaks = True

        # add notation to make the score easier to read
        cycle_pair[1][0][1].lyric = "First cycle starts"
        cycle_pair[2][0][0].lyric = "Second cycle starts"

        # add an ending measure to make the line breaks and formatting a bit cleaner/more consistent
        m = stream.Measure()
        last_chord_as_list = list(tonic_triad.pitches)
        check_note_ranges_and_transpose(last_chord_as_list, string_set)
        last_chord = chord.Chord(last_chord_as_list)
        last_chord.duration = duration.Duration(4.0)
        m.append(last_chord)
        r = note.Rest()
        r.duration = duration.Duration(2.0)
        m.append(r)

        cycle_pair[2].append(m)

        ensure_unique_chords(cycle_pair)
        # cycle_pair.show()
        cycle_pairs.append(cycle_pair)

    return cycle_pairs


def iteration_function(voicing):
    # this function is just used a scrap for figuring out the logic related to generating the
    # different string permutations
    tuples = []

    if voicing == Voicing.Closed:
        for i in range(1, 5):
            tuples.append((i+2, i+1, i))
    elif voicing == Voicing.Drop2_A_form:
        for i in range(1, 4):
            tuples.append((i+3, i+2, i))
    elif voicing == Voicing.Drop2_B_form:
        for i in range(1, 4):
            tuples.append((i+3, i+1, i))
    else:
        raise Exception("Invalid voicing passed")

    return tuples


def write_cycle_to_xml(cycle, directory_path):
    # TODO: figure out better naming here as this isn't limited to just cycles
    # This function assumes there is meta-data which can be extracted to form the filename as well as that the passed
    # directory path already exists
    filename = cycle.metadata.title.replace('/', '')
    filename = filename.replace('\n', '; ')
    filename = filename.replace(':', '')
    file_path = directory_path + filename
    cycle.write("MusicXML", file_path)


def generate_tonic_triad(root_scale, tonic, string_set, voicing):
    # generate the starting chord for this particular string set
    triad_root = pitch.Pitch(tonic)
    triad_root.octave = string_set[0].lowest_pitch.octave
    triad_root.transposeAboveTarget(string_set[0].lowest_pitch, inPlace=True)

    if voicing == Voicing.Closed:
        tonic_triad = chord.Chord(root_scale.pitchesFromScaleDegrees([1, 3, 5], triad_root, triad_root.transpose(11)))
    elif voicing == Voicing.Drop2_A_form or voicing == Voicing.Drop2_B_form:
        tonic_triad = chord.Chord([triad_root, triad_root.transpose(7), triad_root.transpose(16)])
    else:
        raise Exception("invalid voicing passed")

    return tonic_triad


def compare_chords(chord_1, chord_2):
    # this could be re-written in a a much slicker fashion in the future, you could always overload the comparison
    # operators...

    if len(chord_1) != len(chord_2):
        raise Exception("chords passed are different lengths")

    if chord_1 == chord_2:
        return ChordCompareReturn.Same

    compare_pitches = []
    for chord_tone_1, chord_tone_2 in zip(chord_1.pitches, chord_2.pitches):
        compare_pitches.append(chord_tone_1 > chord_tone_2)

    if sum(compare_pitches) == 0:
        # as we've already established that the chords differ by at least one note then if the array returned from the
        # previous comparison is all false, we can conclude that chord_1 is "lower" than chord_2
        return ChordCompareReturn.Lower
    else:
        # given that compare_pitches can only contain positive integers, if its sum isn't zero then it must be positive
        # which would then mean that chord_1 is "higher" than chord_2
        return ChordCompareReturn.Higher


def find_lowest_chord(stream_to_check):
    # scan through a stream "s" and find the lowest chord. i reckon this could easily be modified to handle the
    # searching for other extreme (i.e. the highest chord as well). work on the naming for the argument passed. there
    # might be a way to sort the data ahead of time to make this more efficient/elegant
    chords = stream_to_check.recurse(includeSelf=True, classFilter='Chord')
    lowest = chords[0]
    for c in chords[1:]:
        if compare_chords(c, lowest) == ChordCompareReturn.Lower:
            lowest = c

    return lowest


def ensure_unique_chords(stream_to_check):
    lowest = find_lowest_chord(stream_to_check)
    upper_bound = lowest.transpose(12)
    for c in stream_to_check.recurse(includeSelf=True, classFilter='Chord'):
        if compare_chords(c, upper_bound) != ChordCompareReturn.Lower:
            c.transpose(-12, inPlace=True)

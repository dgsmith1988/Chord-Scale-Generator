from ChordScaleGenerator import *
from music21 import scale, chord, key, stream, metadata
from copy import deepcopy


def check_note_ranges_test():
    string_set = (GuitarRange.A_string, GuitarRange.D_string, GuitarRange.G_string)

    # test case 1: chord is within the specified note ranges
    test_chord = chord.Chord(['E4', 'G4', 'B4'])
    chord_as_list = list(deepcopy(test_chord.pitches))
    check_note_ranges_and_transpose(chord_as_list, string_set)
    test_1 = stream.Measure()
    test_1.append(test_chord)
    test_1.append(chord.Chord(chord_as_list))
    test_1.show()

    # test case 2: chord is above the specified note ranges,
    test_chord = chord.Chord(['E5', 'G5', 'B5'])
    chord_as_list = list(deepcopy(test_chord.pitches))
    check_note_ranges_and_transpose(chord_as_list, string_set)
    test_2 = stream.Measure()
    test_2.append(test_chord)
    test_2.append(chord.Chord(chord_as_list))
    test_2.show()

    # test case 3: chord is below the specified note ranges, transpose it up an octave
    test_chord = chord.Chord(['E3', 'G3', 'B3'])
    chord_as_list = list(deepcopy(test_chord.pitches))
    check_note_ranges_and_transpose(chord_as_list, string_set)
    test_3 = stream.Measure()
    test_3.append(test_chord)
    test_3.append(chord.Chord(chord_as_list))
    test_3.show()


def sub_cycle_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)

    first_chord = chord.Chord([root.transpose(12), root.transpose(4+12), root.transpose(7+12)])
    sub_cycle = generate_sub_cycle(sc, first_chord, cycle2matrix[0])
    sub_cycle.show()

    first_chord = chord.Chord([root.transpose(4), root.transpose(7), root.transpose(12)])
    sub_cycle = generate_sub_cycle(sc, first_chord, cycle2matrix[1])
    sub_cycle.show()

    first_chord = chord.Chord([root.transpose(7), root.transpose(12), root.transpose(12+4)])
    sub_cycle = generate_sub_cycle(sc, first_chord, cycle2matrix[2])
    sub_cycle.show()


def full_cycle_test():
    string_set = (GuitarRange.A_string, GuitarRange.D_string, GuitarRange.G_string)

    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(4), root.transpose(7)])

    cycle = generate_full_cycle(sc, tonic_triad, cycle2matrix[0], string_set)[0]
    cycle.show()


def cycle36_drop2_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(7), root.transpose(16)])
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6", voicing_type=Voicing.Drop2)
    cycle.show()


def cycle36_drop3_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(16), root.transpose(20)])
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6")
    cycle.show()


def cycle36_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs2(sc, tonic_triad, "3/6")
    cycle.show()


def cycle36_write_file_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6")
    cycle.metadata = metadata.Metadata()
    cycle.metadata.title = "Cycle 3/6 progression in C Major"
    cycle.metadata.composer = "Chord Cycle Generation Software"
    cycle.write("MusicXML", "C:\\Temp\\Cycle36_progression")


def cycle45_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "4/5")
    cycle.show()


def cycle27_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "2/7")
    cycle.show()


def cycle36_arbitrary_scale_test():
    # use the ascending version of the melodic minor scale so you get a different set of harmonies compared to the
    # the natural minor version
    sc = scale.ConcreteScale(pitches=['E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D#5'])
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'E5', 'D#6'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6")
    cycle.show()


def cycle36_ab_test():
    sc = scale.MajorScale('Ab')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'Ab4', 'G5'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6")
    cycle.insert(0, key.KeySignature(-4))
    cycle.show()


def cycle36_a_harmonic_minor_test():
    sc = scale.HarmonicMinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6")
    cycle.insert(0, key.KeySignature(0))
    cycle.show()


def cycle36_a_minor_test():
    sc = scale.MinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pairs(sc, tonic_triad, "3/6")
    cycle.insert(0, key.KeySignature(0))
    cycle.show()


def transpose_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    measure = stream.Measure()

    # use a deep copy based on how music21 stores/handles the various memory values
    measure.append(deepcopy(tonic_triad))
    chord_as_list = list(tonic_triad.pitches)
    transpose_chord_as_list(chord_as_list, -12)
    measure.append(chord.Chord(chord_as_list))
    measure.show()


def range_check_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    # create a string set to do the range checking with
    string_set = (GuitarRange.A_string, GuitarRange.D_string, GuitarRange.G_string)
    cycle = generate_cycle_pairs(sc, tonic_triad, "2/7", string_set)
    cycle.show()


def generate_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '2/7'
    generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type)


def new_generate_sub_cycle_test():
    # string_set = (GuitarRange.A_string, GuitarRange.D_string, GuitarRange.G_string)
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(4), root.transpose(7)])
    # sub_cycle = generate_sub_cycle(sc, tonic_triad, cycle2matrix[0], string_set)
    sub_cycle, next_chord = generate_sub_cycle_2(sc, tonic_triad, cycle2matrix[0])
    sub_cycle.append(next_chord)
    sub_cycle.show()


def new_generate_full_cycle_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    root.transpose(12, inPlace=True)
    tonic_triad = chord.Chord([root, root.transpose(4), root.transpose(7)])

    cycle, next_chord = generate_full_cycle_2(sc, tonic_triad, cycle3matrix)
    m = stream.Measure()
    m.append(next_chord)
    cycle.append(m)
    cycle.show()


# check_note_ranges_test()
# sub_cycle_test()
# full_cycle_test()
# cycle27_test()
cycle36_test()
# cycle45_test()
# cycle36_drop3_test()
# cycle36_drop2_test()
# cycle36_Ab_test()
# cycle36_a_harmonic_minor_test()
# cycle36_a_minor_test()
# cycle36_arbitrary_scale_test()
# transpose_test()
# range_check_test()
# cycle36_write_file_test()
# generate_cycles_for_all_string_sets_test()
# new_generate_sub_cycle_test()
# new_generate_full_cycle_test()

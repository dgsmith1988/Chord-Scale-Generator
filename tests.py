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


def drop2_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(7), root.transpose(16)])

    cycle = generate_cycle_pair(sc, tonic_triad, "3/6", voicing_type=Voicing.Drop2_A_form)
    cycle.show()

    cycle = generate_cycle_pair(sc, tonic_triad, "4/5", voicing_type=Voicing.Drop2_A_form)
    cycle.show()

    cycle = generate_cycle_pair(sc, tonic_triad, "2/7", voicing_type=Voicing.Drop2_A_form)
    cycle.show()


def cycle36_drop2_range_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    string_set = (GuitarRange.get_string(4), GuitarRange.get_string(3), GuitarRange.get_string(1))
    # generate the starting chord for this particular string set
    triad_root = pitch.Pitch(tonic)
    triad_root.octave = string_set[0].highest_pitch.octave
    triad_root.transposeBelowTarget(string_set[0].highest_pitch, inPlace=True)
    tonic_triad = chord.Chord([triad_root, triad_root.transpose(7), triad_root.transpose(16)])
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6", note_ranges=string_set, voicing_type=Voicing.Drop2_A_form)
    cycle.show()


def cycle3_drop2_range_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    string_set = (GuitarRange.get_string(4), GuitarRange.get_string(3), GuitarRange.get_string(1))
    triad_root = pitch.Pitch(tonic)
    triad_root.octave = string_set[0].highest_pitch.octave
    triad_root.transposeBelowTarget(string_set[0].highest_pitch, inPlace=True)
    tonic_triad = chord.Chord([triad_root, triad_root.transpose(7), triad_root.transpose(16)])
    cycle = generate_full_cycle(sc, tonic_triad, generate_drop2_matrix(cycle3matrix), note_ranges=string_set)[0]
    cycle.show()


def cycle6_drop2_range_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    string_set = (GuitarRange.get_string(4), GuitarRange.get_string(3), GuitarRange.get_string(1))
    triad_root = pitch.Pitch(tonic)
    triad_root.octave = string_set[0].highest_pitch.octave
    triad_root.transposeBelowTarget(string_set[0].highest_pitch, inPlace=True)
    tonic_triad = chord.Chord([triad_root, triad_root.transpose(7), triad_root.transpose(16)])
    cycle = generate_full_cycle(sc, tonic_triad, generate_drop2_matrix(cycle6matrix), note_ranges=string_set)[0]
    cycle.show()


def cycle36_drop3_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(16), root.transpose(20)])
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.show()


def cycle36_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.show()


def cycle36_write_file_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.metadata = metadata.Metadata()
    cycle.metadata.title = "Cycle 3/6 progression in C Major"
    cycle.metadata.composer = "Chord Cycle Generation Software"
    cycle.write("MusicXML", "C:\\Temp\\Cycle36_progression")


def cycle45_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C4', 'B4'))
    cycle = generate_cycle_pair(sc, tonic_triad, "4/5")
    cycle.show()


def cycle27_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "2/7")
    cycle.show()


def cycle36_arbitrary_scale_test():
    # use the ascending version of the melodic minor scale so you get a different set of harmonies compared to the
    # the natural minor version
    sc = scale.ConcreteScale(pitches=['E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D#5'])
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'E5', 'D#6'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.show()


def cycle36_ab_test():
    sc = scale.MajorScale('Ab')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'Ab4', 'G5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.insert(0, key.KeySignature(-4))
    cycle.show()


def cycle36_a_harmonic_minor_test():
    sc = scale.HarmonicMinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.insert(0, key.KeySignature(0))
    cycle.show()


def cycle36_a_minor_test():
    sc = scale.MinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
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
    cycle = generate_cycle_pair(sc, tonic_triad, "2/7", string_set)
    cycle.show()


def generate_drop2_A_form_36_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '3/6'
    voicing = Voicing.Drop2_A_form
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_drop2_A_form_27_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '2/7'
    voicing = Voicing.Drop2_A_form
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_drop2_A_form_45_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '4/5'
    voicing = Voicing.Drop2_A_form
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_drop2_B_form_36_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '3/6'
    voicing = Voicing.Drop2_B_form
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_drop2_B_form_27_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '2/7'
    voicing = Voicing.Drop2_B_form
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_drop2_B_form_45_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '4/5'
    voicing = Voicing.Drop2_B_form
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_closed_36_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '3/6'
    voicing = Voicing.Closed
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_closed_27_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '2/7'
    voicing = Voicing.Closed
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def generate_closed_45_cycles_for_all_string_sets_test():
    tonic = 'C'
    root_scale = scale.MajorScale(tonic)
    pair_type = '4/5'
    voicing = Voicing.Closed
    cycle_pairs = generate_cycle_pairs_for_all_string_sets(root_scale, tonic, pair_type, voicing)
    for pair in cycle_pairs:
        write_cycle_to_xml(pair, ".\\Examples\\")


def drop2_542_cycle36_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    voicing = Voicing.Drop2_A_form
    # create a string set to do the range checking with
    string_set = (GuitarRange.A_string, GuitarRange.D_string, GuitarRange.B_string)
    tonic_triad = generate_tonic_triad(sc, tonic, string_set, voicing)

    # check_note_ranges_and_transpose(tonic_triad.pitches, string_set)
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6",  string_set, voicing)
    ensure_unique_chords_test(cycle)
    cycle.show()


def drop2_532_cycle36_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    voicing = Voicing.Drop2_B_form
    # create a string set to do the range checking with
    string_set = (GuitarRange.A_string, GuitarRange.G_string, GuitarRange.B_string)
    tonic_triad = generate_tonic_triad(sc, tonic, string_set, voicing)

    # check_note_ranges_and_transpose(tonic_triad.pitches, string_set)
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6",  string_set, voicing)
    ensure_unique_chords_test(cycle)
    cycle.show()


def drop2_431_cycle36_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    voicing = Voicing.Drop2_A_form
    # create a string set to do the range checking with
    string_set = (GuitarRange.D_string, GuitarRange.G_string, GuitarRange.E_string_high)
    tonic_triad = generate_tonic_triad(sc, tonic, string_set, voicing)

    # check_note_ranges_and_transpose(tonic_triad.pitches, string_set)
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6",  string_set, voicing)
    ensure_unique_chords(cycle)
    cycle.show()


def closed_543_cycle27_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    voicing = Voicing.Closed
    # create a string set to do the range checking with
    string_set = (GuitarRange.A_string, GuitarRange.D_string, GuitarRange.G_string)
    tonic_triad = generate_tonic_triad(sc, tonic, string_set, voicing)

    # check_note_ranges_and_transpose(tonic_triad.pitches, string_set)
    cycle = generate_cycle_pair(sc, tonic_triad, "2/7", string_set, voicing)
    ensure_unique_chords(cycle)
    cycle.show()


def compare_chords_test():
    chord_1 = chord.Chord(["E3", "C4", "G4"])
    chord_2 = chord.Chord(["C3", "E-3", "G3"])
    chord_3 = chord.Chord(["E3", "C4", "G#4"])
    chord_4 = chord.Chord(["F3", "C4", "G#4"])
    chord_5 = chord.Chord(["E3", "C4", "G#4"])

    if compare_chords(chord_1, chord_2) == ChordCompareReturn.Higher:
        print(compare_chords_test.__name__ + "() - test 1 passed")
    else:
        raise Exception("chord_1 should be higher than chord_2")

    if compare_chords(chord_1, chord_3) == ChordCompareReturn.Lower:
        print(compare_chords_test.__name__ + "() - test 2 passed")
    else:
        raise Exception("chord_1 should be higher than chord_3")

    if compare_chords(chord_1, chord_1) == ChordCompareReturn.Same:
        print(compare_chords_test.__name__ + "() - test 3 passed")
    else:
        raise Exception("chord_1 should be the same as chord_1")


def find_lowest_chord_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    voicing = Voicing.Drop2_B_form
    # create a string set to do the range checking with
    string_set = (GuitarRange.A_string, GuitarRange.G_string, GuitarRange.B_string)
    tonic_triad = generate_tonic_triad(sc, tonic, string_set, voicing)

    # check_note_ranges_and_transpose(tonic_triad.pitches, string_set)
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6",  string_set, voicing)
    cycle.show()

    lowest = find_lowest_chord(cycle)
    lowest.show()


def ensure_unique_chords_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    voicing = Voicing.Drop2_A_form
    # create a string set to do the range checking with
    string_set = (GuitarRange.A_string, GuitarRange.G_string, GuitarRange.B_string)
    tonic_triad = generate_tonic_triad(sc, tonic, string_set, voicing)

    # check_note_ranges_and_transpose(tonic_triad.pitches, string_set)
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6",  string_set, voicing)
    cycle.show()

    ensure_unique_chords(cycle)
    cycle.show()


def generate_examples():
    output_dir = ".\\Examples\\"

    # Example 1 - cycle 2/7 for C major
    sc = scale.MajorScale('C')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "2/7")
    cycle.insert(0, key.KeySignature(0))
    cycle.metadata = metadata.Metadata()
    cycle.metadata.title = "Example 1 - Cycle 2/7 in C Major"
    cycle.write("MusicXML", output_dir + "Example 1")

    # Example 2 - cycle 4/5 for D major
    sc = scale.MajorScale('D')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'D4', 'C5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "4/5")
    cycle.insert(0, key.KeySignature(2))
    cycle.metadata = metadata.Metadata()
    cycle.metadata.title = "Example 2 - Cycle 4/5 in D Major"
    cycle.write("MusicXML", output_dir + "Example 2")

    # Example 3 - cycle 3/6 for A harmonic minor
    sc = scale.HarmonicMinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6")
    cycle.insert(0, key.KeySignature(0))
    cycle.metadata = metadata.Metadata()
    cycle.metadata.title = "Example 3 - Cycle 3/6 in A Harmonic Minor"
    cycle.write("MusicXML", output_dir + "Example 3")

    # Example 4 - cycle 3/6 for C major but with drop 2 chords
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(7), root.transpose(16)])
    cycle = generate_cycle_pair(sc, tonic_triad, "3/6", voicing_type=Voicing.Drop2_A_form)
    cycle.insert(0, key.KeySignature(0))
    cycle.metadata = metadata.Metadata()
    cycle.metadata.title = "Example 4 - Cycle 3/6 in C Major\nDrop 2 voicings"
    cycle.write("MusicXML", output_dir + "Example 4")


# compare_chords_test()
# find_lowest_chord_test()
# ensure_unique_chords_test()
# check_note_ranges_test()
# sub_cycle_test()
# full_cycle_test()
# cycle27_test()
# cycle36_test()
# cycle45_test()
# cycle36_drop3_test()
# drop2_test()
# cycle36_Ab_test()
# cycle36_a_harmonic_minor_test()
# cycle36_a_minor_test()
# cycle36_arbitrary_scale_test()
# transpose_test()
# range_check_test()
# cycle36_write_file_test()
# cycle36_drop2_range_test()
# cycle3_drop2_range_test()
# cycle6_drop2_range_test()
# drop2_542_cycle36_test()
# drop2_532_cycle36_test()
# drop2_431_cycle36_test()
# closed_543_cycle27_test()
generate_drop2_A_form_36_cycles_for_all_string_sets_test()
generate_drop2_A_form_27_cycles_for_all_string_sets_test()
generate_drop2_A_form_45_cycles_for_all_string_sets_test()
generate_drop2_B_form_36_cycles_for_all_string_sets_test()
generate_drop2_B_form_27_cycles_for_all_string_sets_test()
generate_drop2_B_form_45_cycles_for_all_string_sets_test()
generate_closed_36_cycles_for_all_string_sets_test()
generate_closed_27_cycles_for_all_string_sets_test()
generate_closed_45_cycles_for_all_string_sets_test()
generate_examples()

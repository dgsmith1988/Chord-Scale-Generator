from ChordScaleGenerator import *
from music21 import scale, chord, key, stream
from copy import deepcopy


def cycle36_drop2_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(7), root.transpose(16)])
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6", voicing_type=Voicing.Drop2)
    cycle.show()


def cycle36_drop3_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(16), root.transpose(20)])
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.show()


def cycle36_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.show()


def cycle45_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "4/5")
    cycle.show()


def cycle27_test():
    tonic = 'C'
    sc = scale.MajorScale(tonic)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "2/7")
    cycle.show()


def cycle36_arbitrary_scale_test():
    # use the ascending version of the melodic minor scale so you get a different set of harmonies compared to the
    # the natural minor version
    sc = scale.ConcreteScale(pitches=['E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D#5'])
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'E5', 'D#6'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.show()


def cycle36_ab_test():
    sc = scale.MajorScale('Ab')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'Ab4', 'G5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.insert(0, key.KeySignature(-4))
    cycle.show()


def cycle36_a_harmonic_minor_test():
    sc = scale.HarmonicMinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.insert(0, key.KeySignature(0))
    cycle.show()


def cycle36_a_minor_test():
    sc = scale.MinorScale('A')
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'A4', 'G5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
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
    cycle = generate_full_cycle_range(tonic_triad, cycle2matrix[0], sc, string_set)[0]
    cycle.show()


cycle27_test()
# cycle36_test()
# cycle45_test()
# cycle36_drop3_test()
# cycle36_drop2_test()
# cycle36_Ab_test()
# cycle36_a_harmonic_minor_test()
# cycle36_a_minor_test()
# cycle36_arbitrary_scale_test()
# transpose_test()
range_check_test()

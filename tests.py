from ChordScaleGenerator import *
from music21 import scale, chord


def cycle3_drop2_test():
    key = 'C'
    sc = scale.MajorScale(key)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(7), root.transpose(16)])
    cycle = generate_full_cycle2(tonic_triad, generate_drop2_matrix(cycle3matrix[0, :, :]), sc)[0]
    cycle.show()


def cycle36_drop3_test():
    key = 'C'
    sc = scale.MajorScale(key)
    root = sc.pitchFromDegree(1)
    tonic_triad = chord.Chord([root, root.transpose(16), root.transpose(20)])
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.show()


def cycle36_test():
    key = 'C'
    sc = scale.MajorScale(key)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "3/6")
    cycle.show()


def cycle45_test():
    key = 'C'
    sc = scale.MajorScale(key)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "4/5")
    cycle.show()


def cycle27_test():
    key = 'C'
    sc = scale.MajorScale(key)
    tonic_triad = chord.Chord(sc.pitchesFromScaleDegrees([1, 3, 5], 'C5', 'B5'))
    cycle = generate_cycle_pairs(tonic_triad, sc, "2/7")
    cycle.show()


# cycle27_test()
# cycle36_test()
# cycle45_test()
# cycle36_drop3_test()
# cycle3_drop2_test()

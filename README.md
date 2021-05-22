# Chord-Scale-Generator
This is a tool for generate different chord scale sequences that can be used for study/practice. The idea came about after completing Chris Buono's TrueFire Course for ["Triad Chord Scales"](https://truefire.com/guitar-gym/triad-chord-scales-major/c753). I quite liked the concept but didn't want to have to manually write out the different chord scales for each different key so I wrote a piece of software to automate the task. On the way I also expanded it to support drop 2 triads (know as "spread triads" in some circles) as well as support for other scale types (like harmonic minor or melodic minor). Code is also included to enforce the range conditions for particular string sets. This makes it so only one voicing for each chord will appear in the cycle and you won't get any voicing being an octave higher/lower than any other (similar to what Chris does in his course). The range restrictions don't need to be used if you don't want and theoretically could be adapted for any other instrument (stringed or not).

The output files are MusicXML so you need something like MuseScore to read them.


# Theory
If you're interested in the theory behind how this works I've included my worklog. The early entries show how the voice leading patterns were derived from Chris's examples. After that, you can see how I worked out translating these ideas into music21 code.

This could easily be expanded to 7th chords (something I plan to take a look at) as well as more exotic scales (i.e. octotonic). The basis for this is the relative ordering of the scale tones to each other and how you move each note throughout the scale so the the possibilities are quite vast if you're look for ways to systematically generate different harmonizations of an arbitrary scale. For instance you could change the starting structure and voice leading patterns to generate sus2 chords instead of triads. In fact any harmonic structure you wanted could be used. The tool could be applied in a similar way to how Slonimsky devised all the different ways to divide up an octave in his "Thesaurus Of Scales and Melodic Patterns". The difference is here you're dealing with voice leading patterns for each note in a harmonic structure as applied to an arbitrary scale. I haven't taken it that far yet as I want to get the more common cases done first, but it's all there if you're feeling adventurous.

# Examples
I've included some examples in the "\Examples" directory to help illustrate things. The code to generate these can be found in tests.py in the "generate_examples()" function as well as any of the other functions which start with "generate". The basic examples are the following:

* Example 1 - Cycle 2/7 in C Major
* Example 2 - Cycle 4/5 in D Major
* Example 3 - Cycle 3/6 in A Harmonic Minor
* Example 4 - Cycle 3/6 in C Major - Drop 2 voicings

The other examples are a full set of of all the different string sets/chord voicings/cycle types in C Major.

from music21 import stream, scale, pitch, chord, stream

#create a score to hold all the parts
s = stream.Score(id='mainScore')

#arbitrary key for the moment
key = 'G'

#Create a scale based on the key to generate chords from
#for now just use a basic major scale to get things up and running
sc = scale.MajorScale(key)

#now that we have a scale in place, let's get the pitch "pointers" setup to the starting pitches
chordTones = [pitch.Pitch('g5'), pitch.Pitch('b5'), pitch.Pitch('d6')]

#cycle matrices - these date structures contain the distances each chord tone should move to
#based on the patterns derived from the different cycles, they will have to be expanded once
#support for four note chords is added
cycle2matrix = [[-2, -1, -1], [-1, -2, -1], [-1, -1, -2]]


#now what do we do? create a chord from each set of pitches and then store this chord in a
#measure and generate the next chord

#think of a better name for these variables afterwards
m1 = stream.Measure()
m1.append(chord.Chord(chordTones))

#generate the next chord based on the rules from the chart, for now complete the cycle2 progressions
for j in range(0, 2):
    for row in cycle2matrix:
        for i in range(len(chordTones)):
            if row[i] < 0:
                chordTones[i] = sc.next(chordTones[i], 'descending' , abs(row[i]))
            else:
                chordTones[i] = sc.next(chordTones[i], 'ascending' , row[i])
        #now that we've updated the chord tones, create a new chord and append it to the measure
        m1.append(chord.Chord(chordTones))
m1.show()

#take everything up an octave and then generate the next part of the cycle (admittedly this isn't the cleanest way to handle this long term as you'll need to figure out
#where it's necessary to transpose things where you run out of frets and take the string sets you're working on into consideration)
for tone in chordTones:
    tone.transpose('P8', inPlace=True)
m2 = stream.Measure()

for j in range(0, 2):
    for row in cycle2matrix:
        for i in range(len(chordTones)):
            if row[i] < 0:
                chordTones[i] = sc.next(chordTones[i], 'descending' , abs(row[i]))
            else:
                chordTones[i] = sc.next(chordTones[i], 'ascending' , row[i])
        #now that we've updated the chord tones, create a new chord and append it to the measure
        m2.append(chord.Chord(chordTones))
m2.show()

#setup all the data structures to be populated
p1 = stream.Part()
m1 = stream.Measure()
m2 = stream.Measure()
m3 = stream.Measure()
p1.append(m1)
p1.append(m2)
p1.append(m3)

m1.append(chord.Chord(chordTones))
k = 0
for i in range(20): #20 is used as there are 21 chords in total but we already start with one in the previous line
    for j in range(len(chordTones)):
        if cycle2Matrix[j][i] < 0:
            chordTones[i] = sc.next(chordTones[i], 'descending', abs(row[

# coding=utf-8

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# return: 'C#'
# id: 1
def note_with_id(id):
    return NOTES[id]


# return: 1
# key_name: 'C#'
def id_with_note(note):
    note = note.upper()
    hit = NOTES.index(note[0])
    if len(note) == 2:
        if note[1].lower() == 'b':
            hit -= 1
        elif note[1].lower() == '#':
            hit += 1
    return hit % 12


# return : {note_id: note_name, note_id: note_name, ...}    eg. {0:'C', 1:'D',..}
# mt: "C#" , "C"
def scale_major(start_note):
    dict_scales = {}
    assert len(start_note) <= 2

    hit = NOTES.index(start_note[0].upper())
    if hit == -1:
        return None
    if len(start_note) == 2:
        if start_note[1].lower() == 'b':
            hit -= 1
        elif start_note[1].lower() == '#':
            hit += 1

    assert (0 <= hit) and (hit < 12)

    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 1
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]
    return dict_scales


def scale_major_with_id(id):
    return scale_major(NOTES[id])


# return : {note_id: note_name, note_id: note_name, ...}
# mt: "C#" , "C"
def scale_minor(start_note):
    dict_scales = {}
    assert len(start_note) <= 2

    hit = NOTES.index(start_note[0].upper())
    if hit == -1:
        return None
    if len(start_note) == 2:
        if start_note[1].lower() == 'b':
            hit -= 1
        elif start_note[1].lower() == '#':
            hit += 1

    assert (0 <= hit) and (hit < 12)

    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 1
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 1
    dict_scales[hit % 12] = NOTES[hit % 12]

    hit += 2
    dict_scales[hit % 12] = NOTES[hit % 12]
    return dict_scales


def scale_minor_with_id(id):
    return scale_minor(NOTES[id])

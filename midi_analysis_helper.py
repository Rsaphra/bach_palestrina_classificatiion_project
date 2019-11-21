import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import logging
import music21
from scraper import *
from collections import Counter


def get_parts(score):
    """
        Takes in a music21.stream.score object as a parameter and
        returns a list of music.stream.Part objects corresponding to
        each instrment in the score

        Params: score: music.stream.Score object
        Returns: list of part objects from that score
    """

    score_parts = []
    score_elements = score.elements
    for element in score_elements:
        if isinstance(element, music21.stream.Part):
            score_parts.append(element)

    return score_parts


def get_parts_dict(c_parts: list):
    """
        Given a list of the parts of a midi score, returns a dictionary
        where the key is the name of each instrument, and the remaining
        data of that part is the key

        Params: list of music21.stream.Part objects
        Returns: dictionary with key->InstrumentName, key-> part data
    """
    parts_dict = {}
    for part in c_parts:
        instrument = part[0]
        instrument_name = instrument.partName
        parts_dict[instrument_name] = part[1:]
    return parts_dict


def get_all_measures(parts_dict: dict):
    """
        returns a reorganized parts_dict, such that it is a list of each measure,
        and each measure is a dict with the measure number and that measure's data

        Params: a dictionary where each key is an instrument name
        Returns: a list of dicts
    """

    all_measures = []
    for key, value in parts_dict.items():
        measure_dict = {}
        measures = value.elements
        for measure in measures:
            measure_number = measure.measureNumber
            measure_dict[measure_number] = measure.elements
        parts_dict[key] = measure_dict
        all_measures.append(measure_dict)
    return all_measures

def get_max_range(parts_dict: dict):
    """
        Determines the total range of measure numbers
        Since the keys for each measure are ints, this method
        takes the keys of the value in the dict and returns the max

    """
    for part_name, value in parts_dict.items():
        return max(value.keys())

def get_notes_by_measure(parts_dict: dict):
    measure_notes = {}

    total_measures = get_max_range(parts_dict)
    for measure_number in range(total_measures):
        try:
            measure_notes[measure_number] = []
            for part_name, part_info in parts_dict.items():
                measure_info = part_info[measure_number]
                for note in measure_info:
                    if type(note) is music21.note.Note:
                        measure_notes[measure_number].append(note.name)
        except:
            print()
    return measure_notes

def is_note(note):
    return len(note)==1 or len(note) == 2

def remove_rests_from_measure(measure_notes):
    return [note for note in measure_notes if is_note(note)]

def remove_rests_from_measure_dict(measure_notes_dict):
    for meas_num, notes in measure_notes_dict.items():
        measure_notes_dict[meas_num] = remove_rests_from_measure(notes)
    return measure_notes_dict

def get_only_note(most_common_tuples: list):
    """
        returns only the note letter in the tuple that would be returned
        by the most_common method from counter

        Returns: list of note letters
    """
    most_common_notes = []
    for note in most_common_tuples:
        most_common_notes.append(note[0])
    return most_common_notes

def most_frequent(note_list):
    occurence_count = Counter(note_list)
    most_common_notes = occurence_count.most_common(3)
    return get_only_note(most_common_notes)

def get_measure_triad(measure_dict_notes: dict):
    """
        Given a dictionary of measures with values of each of their notes,
        return a dictionary with measure num as key
        and 3 most common notes as values

        Params: a dictionary with keys of measure numbers and values of a list of str
        representing notes in that chord
    """

    measure_chord_dict = {}

    for measure_num, notes in measure_dict_notes.items():
        top_3_notes = most_frequent(notes)
        measure_chord_dict[measure_num] = top_3_notes
    return measure_chord_dict



def get_chord_name(triad):

    #returns the common chord name of a triad
    try:
        c1 = chord.Chord(triad)
        return c1.pitchedCommonName
    except:
        return None

def add_chord_name(measure_triad_dict: dict):
    """
        Given a dictionary where the key is a measure number and the value
        is the most common triad found in that measure, returns the common name
        for that chord based on the music21 modules

        Params: dict with keys of measure numbers, values of most common triads
        Returns: dict with keys of measure numbers, values with index 0 being triad
        and index 1 being the corresponding chord name
    """

    for measure_num, triad in measure_triad_dict.items():
        chord_name = get_chord_name(triad)
        measure_triad_dict[measure_num] = [triad, chord_name]
    return measure_triad_dict

def process_score_vertically(score):
    score_parts = get_parts(score)
    parts_dict = get_parts_dict(score_parts)
    all_measures = get_all_measures(parts_dict)
    measure_notes = get_notes_by_measure(parts_dict)
    measure_notes = remove_rests_from_measure_dict(measure_notes)
    measure_chord_dict = get_measure_triad(measure_notes)
    return add_chord_name(measure_chord_dict)

def get_beat_1_notes(measure_dict_notes: dict):
    """
        Given a dictionary of measures and the notes container therein,
        returns the triadic representation of the notes that occur on the first beat

    """

    measure_beat1_dict = {}

    for measure_num, notes in measure_dict_notes.items():
        print(notes)

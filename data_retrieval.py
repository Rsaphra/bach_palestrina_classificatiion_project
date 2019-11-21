
def get_full_path(path: str):
    # Adds maestro-v2.0.0 to file path for accessing
    return './maestro-v2.0.0/' + path

def get_midi_from_path(path: str):
    full_path = get_full_path(path)
    pm = pretty_midi.PrettyMIDI(full_path)
    return pm

def get_music21_from_path(path: str):
    full_path = get_full_path(path)
    m21 = converter.parse(full_path)
    return m21

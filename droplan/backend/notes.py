import os
import json
import time
import hashlib
NOTES_FILE = os.path.join(os.path.dirname(__file__), 'notes.json')

# Ensure notes.json exists and contains valid JSON
def _ensure_notes_file():
    if not os.path.exists(NOTES_FILE) or os.path.getsize(NOTES_FILE) == 0:
        with open(NOTES_FILE, 'w') as f:
            json.dump({}, f)

_ensure_notes_file()

def _load_notes():
    if not os.path.exists(NOTES_FILE) or os.path.getsize(NOTES_FILE) == 0:
        return {}
    try:
        with open(NOTES_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Error reading notes.json: {e}")
        return {}
    
def _save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=4)

def add_note_to_bucket(content):
    note_hash = hashlib.sha256(content.encode()).hexdigest()
    notes = _load_notes()
    
    if note_hash in notes:
        return note_hash  # Note already exists

    notes[note_hash] = {
        'content': content,
        'timestamp': time.time(),
    }
    
    _save_notes(notes)
    return note_hash

def get_notes():
    notes = _load_notes()
    now = time.time()
    valid_notes = {}
    
    for note_hash, data in notes.items():
        if now - data['timestamp'] < 1800:  # 30 minutes validity
            valid_notes[note_hash] = data
    
    return valid_notes

def expire_old_notes():
    now = time.time()
    notes = _load_notes()
    expired = []
    updated = {}
    for k, v in notes.items():
        if now - v['timestamp'] >= 1800:
            expired.append(k)
        else:
            updated[k] = v
    _save_notes(updated)
    return expired

def delete_note_by_hash(note_hash):
    notes = _load_notes()
    if note_hash in notes:
        del notes[note_hash]
        _save_notes(notes)
        return True
    return False

def clear_all_notes():
    notes = _load_notes()
    count = len(notes)
    _save_notes({})
    return count
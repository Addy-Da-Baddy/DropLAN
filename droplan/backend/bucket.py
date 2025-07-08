import os
import time
import hashlib
import json

BUCKET_DIR = os.path.join(os.path.dirname(__file__), 'bucket')
META_FILE = os.path.join(BUCKET_DIR, 'meta.json')

os.makedirs(BUCKET_DIR, exist_ok=True)

if not os.path.exists(META_FILE):
    with open(META_FILE, 'w') as f:
        json.dump({"files": {}, "notes": {}}, f)

def _load_meta():
    with open(META_FILE, 'r') as f:
        return json.load(f)

def _save_meta(meta):
    with open(META_FILE, 'w') as f:
        json.dump(meta, f, indent=4)

def _hash_file(file_obj):
    file_obj.seek(0)  # Ensure we read from the start of the file
    hasher = hashlib.sha256()
    while chunk := file_obj.read(4096):
        hasher.update(chunk)
    file_obj.seek(0)  # Reset file pointer after reading
    return hasher.hexdigest()

def add_file_to_bucket(file):
    file_hash = _hash_file(file)
    filename = file.filename
    file_path = os.path.join(BUCKET_DIR, file_hash)
    file.save(file_path)

    #meta szaveit

    meta = _load_meta()
    meta['files'][file_hash] = {
        'name': filename,
        'timestamp': time.time(),
    }
    _save_meta(meta)
    return file_hash


def get_valid_files():
    meta = _load_meta()
    now = time.time()
    valid = {}
    files = meta.get('files', {})
    for h, data in files.items():
        if now - data['timestamp'] < 1800:
            valid[h] = data
    return valid


def get_all_files_metadata():
    return _load_meta()

def get_file_path_by_hash(file_hash):
    meta = _load_meta()
    if file_hash not in meta['files']:
        return None
    if time.time() - meta['files'][file_hash]['timestamp'] > 1800:
        return None
    path = os.path.join(BUCKET_DIR, file_hash)
    if not os.path.exists(path):
        return None
    return path


def delete_file_by_hash(file_hash):
    meta = _load_meta()
    if file_hash in meta['files']:
        del meta['files'][file_hash]
        _save_meta(meta)
        file_path = os.path.join(BUCKET_DIR, file_hash)
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    return False

def clear_all_files():
    meta = _load_meta()
    file_count = len(meta.get('files', {}))
    
    # Delete all physical files
    for file_hash in meta.get('files', {}):
        file_path = os.path.join(BUCKET_DIR, file_hash)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Clear files from metadata
    meta['files'] = {}
    _save_meta(meta)
    
    return file_count
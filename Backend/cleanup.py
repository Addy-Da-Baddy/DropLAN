from apscheduler.schedulers.background import BackgroundScheduler
import time
from bucket import get_all_files_metadata, delete_file_by_hash
from notes import expire_old_notes

EXPIRY_TIME = 1800

def cleanup(socketio=None):
    now = time.time()

    # Files
    meta = get_all_files_metadata()
    files = meta.get('files', {})
    for file_hash, data in list(files.items()):
        if now - data["timestamp"] >= EXPIRY_TIME:
            delete_file_by_hash(file_hash)
            if socketio:
                socketio.emit("file_expired", {"file_hash": file_hash})

    # Notes
    expired_notes = expire_old_notes()
    for note_hash in expired_notes:
        if socketio:
            socketio.emit("note_expired", {"note_hash": note_hash})

def start_cleanup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup, "interval", seconds=30)
    scheduler.start()

def bind_socketio_cleanup(socketio):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: cleanup(socketio), "interval", seconds=30)
    scheduler.start()

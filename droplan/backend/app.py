from flask import Flask, request, jsonify, send_file, send_from_directory, redirect
from flask_cors import CORS
from bucket import add_file_to_bucket, get_valid_files, get_file_path_by_hash, get_all_files_metadata, delete_file_by_hash
from notes import add_note_to_bucket, get_notes, delete_note_by_hash, clear_all_notes
from utils import get_QR
from cleanup import start_cleanup_scheduler, bind_socketio_cleanup
from flask_socketio import SocketIO,emit
import os
import socket
import subprocess

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Get the path to the templates directory
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
if os.path.exists(template_dir):
    app.template_folder = template_dir

@app.route('/')
def root():
    return redirect('/LAN_Drop')

@app.route('/api/upload/file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'file not found'}), 400
    file = request.files['file']
    file_hash = add_file_to_bucket(file)
    socketio.emit('file_uploaded', {'file_hash': file_hash})
    return jsonify({"hash":file_hash, "status":"success"}), 201

@app.route('/api/upload/note', methods=['POST'])
def upload_note():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'content not found'}), 400
    note_hash = add_note_to_bucket(content)
    socketio.emit('note_uploaded', {'note_hash': note_hash})
    return jsonify({"hash": note_hash, "status":"success"}), 201

@app.route('/api/bucket/files', methods=['GET'])
def get_files():
    files = get_valid_files()
    return jsonify(files), 200


@app.route('/api/bucket/notes', methods=['GET'])
def get_notes_route():
    notes = get_notes()
    return jsonify(notes), 200

@app.route('/api/download/<file_hash>', methods=['GET'])
def download_file(file_hash):
    file_path = get_file_path_by_hash(file_hash)
    if not file_path:
        return jsonify({'error': 'file not found'}), 404
    
    # Get filename from metadata
    meta = get_all_files_metadata()
    filename = meta.get('files', {}).get(file_hash, {}).get('name', 'download')
    
    return send_file(file_path, as_attachment=True, download_name=filename)

@app.route('/api/delete/file/<file_hash>', methods=['DELETE'])
def delete_file_endpoint(file_hash):
    success = delete_file_by_hash(file_hash)
    if success:
        socketio.emit('file_deleted', {'file_hash': file_hash})
        return jsonify({'status': 'success', 'message': 'File deleted'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/delete/note/<note_hash>', methods=['DELETE'])
def delete_note_endpoint(note_hash):
    success = delete_note_by_hash(note_hash)
    if success:
        socketio.emit('note_deleted', {'note_hash': note_hash})
        return jsonify({'status': 'success', 'message': 'Note deleted'}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

@app.route('/api/clear/files', methods=['DELETE'])
def clear_all_files():
    from bucket import clear_all_files as clear_files_func
    count = clear_files_func()
    socketio.emit('files_cleared', {'count': count})
    return jsonify({'status': 'success', 'message': f'Cleared {count} files'}), 200

@app.route('/api/clear/notes', methods=['DELETE'])
def clear_all_notes_endpoint():
    count = clear_all_notes()
    socketio.emit('notes_cleared', {'count': count})
    return jsonify({'status': 'success', 'message': f'Cleared {count} notes'}), 200

@app.route('/api/clear/bucket', methods=['DELETE'])
def clear_entire_bucket():
    from bucket import clear_all_files as clear_files_func
    file_count = clear_files_func()
    note_count = clear_all_notes()
    socketio.emit('bucket_cleared', {'file_count': file_count, 'note_count': note_count})
    return jsonify({'status': 'success', 'message': f'Cleared {file_count} files and {note_count} notes'}), 200

@app.route('/api/network-info', methods=['GET'])
def get_network_info():
    try:
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Get Wi-Fi network name (SSID) - Linux specific
        wifi_name = "Unknown Network"
        try:
            # Try nmcli first (NetworkManager)
            result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('yes:'):
                        wifi_name = line.split(':', 1)[1]
                        break
        except:
            # Fallback: try iwgetid
            try:
                result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    wifi_name = result.stdout.strip()
            except:
                pass
        
        return jsonify({
            'ip': local_ip,
            'wifi_name': wifi_name,
            'hostname': socket.gethostname()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Could not detect network info: {str(e)}'}), 500

@app.route('/api/qr/', methods=['GET'])
def generate_qr():
    try:
        # Check if manual IP is provided
        manual_ip = request.args.get('ip')
        if manual_ip:
            # Use manually provided IP
            target_ip = manual_ip.strip()
        else:
            # Auto-detect local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            target_ip = s.getsockname()[0]
            s.close()
        
        return get_QR(f"http://{target_ip}:5000/LAN_Drop")
    except Exception as e:
        return jsonify({'error': f'Could not generate QR code: {str(e)}'}), 500
    

#WebSocket stuff
@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# Frontend serving routes
@app.route('/LAN_Drop')
def serve_frontend():
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
    if os.path.exists(template_path):
        return send_file(template_path)
    else:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'index.html')

@app.route('/LAN_Drop/')
def serve_frontend_slash():
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
    if os.path.exists(template_path):
        return send_file(template_path)
    else:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), filename)

if __name__ == '__main__':
    start_cleanup_scheduler()
    bind_socketio_cleanup(socketio)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    print("Server is running on http://localhost:5000")

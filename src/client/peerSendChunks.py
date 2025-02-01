from flask import Flask, request, send_file
import os

app = Flask(__name__)
CHUNKS_DIR = "C:\\Peers\\chunks"

@app.route('/get_chunk', methods=['GET'])
def send_chunk():
    chunk_name = request.args.get('chunk_name')
    
    chunk_path = os.path.join(CHUNKS_DIR, chunk_name)
    
    print(f"Resolved chunk path: {chunk_path}")
    
    if os.path.exists(chunk_path):
        return send_file(chunk_path, as_attachment=True)
    else:
        return "Chunk not found", 404

if __name__ == "__main__":
    app.run(port=5001, debug=True)
from flask import Flask, request, send_file
import os

app = Flask(__name__)
FILES_DIRECTORY = "C:/Peers/Files"

@app.route('/get_chunk', methods=['GET'])
def get_chunk():
    chunk_name = request.args.get("chunk_name")
    chunk_path = os.path.join(FILES_DIRECTORY, chunk_name)

    if os.path.exists(chunk_path):
        print(f"Sending chunk: {chunk_name}")
        return send_file(chunk_path, as_attachment=True)
    else:
        print(f"Chunk not found: {chunk_name}")
        return "Chunk not found", 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000) #localhost

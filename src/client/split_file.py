import os
import zipfile

def split_file_into_chunks(file_path, chunk_size=20 * 1024 * 1024, peer_directory="C:/Peers/Files"):
    with open(file_path, 'rb') as f:
        chunk_number = 0
        while chunk := f.read(chunk_size):
            # Define the filename for the current chunk
            chunk_filename = f"{os.path.basename(file_path)}_chunk_{chunk_number}"
            chunk_filepath = os.path.join(peer_directory, chunk_filename)
            
            # Save the chunk to a file
            with open(chunk_filepath, 'wb') as chunk_file: 
                chunk_file.write(chunk)
            
            # Create a separate ZIP file for each chunk
            zip_filename = os.path.join(peer_directory, f"{os.path.basename(file_path)}_chunk_{chunk_number}.zip")
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(chunk_filepath, os.path.relpath(chunk_filepath, peer_directory))  # Add the chunk file to the ZIP
                print(f"Chunk created and zipped: {zip_filename}")
            
            # Delete the chunk file after it's added to the ZIP
            os.remove(chunk_filepath)
            chunk_number += 1

        print(f"All chunks have been zipped individually.")
    return chunk_number


# Example of use:
# file_path = r"C:\Users\rotem\Desktop\sunset.jpg"
# split_file_into_chunks(file_path)

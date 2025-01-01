import os
import zipfile

def merge_chunks_to_file(output_file_path, file_name, total_chunks, peer_directory="C:/Peers/Files"):
    "Merge the split chunks back into a single file after extracting them from ZIPs."
    with open(output_file_path, 'wb') as output_file:
        for i in range(total_chunks):
            # Define the path to the ZIP file for the current chunk
            zip_filename = os.path.join(peer_directory, f"{file_name}_chunk_{i}.zip")
            
            with zipfile.ZipFile(zip_filename, 'r') as zipf:
                # Assume each ZIP contains a single chunk, get the file name inside the ZIP
                chunk_filename_in_zip = os.path.basename(zip_filename).replace(".zip", "")
                
                # Extract the chunk from the ZIP to a temporary location
                zipf.extract(chunk_filename_in_zip, peer_directory)
                
                # Read the extracted chunk file and write its content to the output file
                extracted_chunk_path = os.path.join(peer_directory, chunk_filename_in_zip)
                with open(extracted_chunk_path, 'rb') as chunk_file:
                    output_file.write(chunk_file.read())
                
                # Delete the extracted chunk file after merging
                os.remove(extracted_chunk_path)
                print(f"Chunk {i} merged successfully from {zip_filename}")
    
    print(f"Merged file created: {output_file_path}")

# Example of use:
output_file_path = r"C:\Peers\Files\Merged_Charlie_and_the_chocolate_factory.avi"
file_name = "Charlie_and_the_chocolate_factory.avi"  # The original filename used when splitting
total_chunks = 35  # Total number of chunks that were created
merge_chunks_to_file(output_file_path, file_name, total_chunks)

def split_file_into_chunks(file_path, chunk_size=20 * 1024 * 1024):
    with open(file_path, 'rb') as f:
        chunk_number = 0
        while chunk := f.read(chunk_size):
            chunk_filename = f"{file_path}_chunk_{chunk_number}"
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
            print(f"Chunk created: {chunk_filename}")
            chunk_number += 1

file_path = r"C:\Users\rotem\Desktop\bittorent\movie\Charlie_and_the_chocolate_factory.avi"
split_file_into_chunks(file_path)
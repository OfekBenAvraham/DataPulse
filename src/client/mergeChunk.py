def merge_chunks_to_file(output_file_path, chunk_prefix, total_chunks):
    "Merge the split chunks back into a single file."
    with open(output_file_path, 'wb') as output_file:
        for i in range(total_chunks):
            chunk_filename = f"{chunk_prefix}_chunk_{i}"
            with open(chunk_filename, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
    print(f"Merged file created: {output_file_path}")

output_file_path = r"C:\Users\rotem\Desktop\bittorent\movie\Merged_Charlie_and_the_chocolate_factory.avi"
chunk_prefix = r"C:\Users\rotem\Desktop\bittorent\movie\Charlie_and_the_chocolate_factory.avi"
merge_chunks_to_file(output_file_path, chunk_prefix, 35)
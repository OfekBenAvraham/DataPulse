from fastapi import APIRouter, HTTPException, Body, Depends
from app.models.file import FileModel, FileCheckRequest
from app.database.connection import peer_collection, file_collection
from app.utils.auth import get_current_peer

router = APIRouter()

@router.post("/add_file")
async def add_file(file_data: FileModel, current_peer=Depends(get_current_peer)):
    """
    Add a new file to the system.
    name: str
    type: str
    total_chunks: int
    Input:
        file_data: {
            "name": "example_video"
            "type": "mp4"
            "total_chunks": 31,
        }
    Expected result:
        File is saved in the database.
    """
    # Check if the file already exists
    existing_file = await file_collection.find_one({"name": file_data.name, "type": file_data.type})
    if existing_file:
        raise HTTPException(status_code=400, detail="File already exists")

    chunks = [{"order": i, "peers": [current_peer["email"]]} for i in range(file_data.total_chunks)]
    new_file = {
        "file_name": file_data.name,
        "total_chunks": file_data.total_chunks,
        "type": file_data.type,
        "chunks": chunks
    }
    # Save the file
    await file_collection.insert_one(new_file)
    return {"message": "File added successfully"}


@router.post("/update_chunks")
async def update_chunks(data: dict = Body(...), current_peer=Depends(get_current_peer)):
    """
    Update chunk ownership for a peer.

    Input:
        {
            "file_name": "file123",
            "type": "type",
            "chunks": [1, 2],
        }
    Expected result:
        File's chunk ownership is updated in the database.
    """
    email = current_peer["email"]
    file_name = data["file_name"]
    type = data["type"]
    chunks = data["chunks"]

    # Check if peer exists and is logged in
    peer = await peer_collection.find_one({"email": email, "logged_in": True})
    if not peer:
        raise HTTPException(status_code=401, detail="Peer not logged in")

    # Update chunk ownership
    for chunk_order in chunks:
        await file_collection.update_one(
            {"file_name": file_name, "type": type, "chunks.order": chunk_order},
            {
                "$addToSet": {"chunks.$.peers": email}
            }
        )

    return {"message": "Chunks updated successfully"}

@router.post("/get_peers")
async def get_peers(data: dict = Body(...), current_peer=Depends(get_current_peer)):
    """
    Get peers for file chunks.

    Input:
        {
            "name": "file123",
            "chunks": Optional[List[int]],
            "type": "mp4"
        }
    Output:
        List of peers owning the requested chunks.
    """
    type = data["type"]
    file_name = data["name"]
    requested_chunks = data.get("chunks", None)
    file = await file_collection.find_one({"file_name": file_name, "type": type})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Fetch chunks
    chunks_to_return = file["chunks"] if requested_chunks is None else [
        chunk for chunk in file["chunks"] if chunk["order"] in requested_chunks
    ]

    result = []
    valid_peers = []
    for chunk_data in chunks_to_return:
        for peer_email  in chunk_data["peers"]:
            if len(valid_peers) == 5:
                break
            peer = await peer_collection.find_one_and_update({"email": peer_email , "logged_in": True, "is_busy": False }, {"$set": {"is_busy": True}})
            if peer:
                valid_peers.append({"email": peer["email"], "ip": peer["ip"], "port": peer["port"]})

        result.append({"chunk": chunk_data["order"], "peers": valid_peers})

    return {"peers": result}


@router.post("/check_file")
async def check_existing_file(file_data: FileCheckRequest, current_peer=Depends(get_current_peer)):
    """
    Check if a file already exists by name and type.

    Input:
        name: str - The name of the file.
        type: str - The type of the file.
    Output:
        exist: bool - True if the file exists, False otherwise.
    """
    # Query the database for a file with the given name and type
    existing_file = await file_collection.find_one({
        "file_name": file_data.name,
        "type": file_data.type
    })

    if existing_file:
        raise HTTPException(status_code=404, detail="File already exist!")
    # Return the existence status
    return

@router.post("/get_file")
async def get_file(file_data: FileCheckRequest):
    existing_file = await file_collection.find_one({
        "file_name": file_data.name,
        "type": file_data.type
    })
    
    if not existing_file:
        raise HTTPException(status_code=404, detail="File not exist!")
    # Convert MongoDB document to a JSON-serializable dictionary
    if "_id" in existing_file:
        existing_file["_id"] = str(existing_file["_id"])

    # Return the JSON-serializable file
    return existing_file

@router.get("/files_summary")
async def get_files_summary():
    """
    Get a summary of all files with their title, category, and image.

    Output:
        List of objects containing:
        - title: The file name.
        - category: The category of the file (movies, games, programs).
        - image: The image URL associated with the category.
    """
    files = await file_collection.find().to_list(length=None)  # Retrieve all files from the database

    def get_category_and_image(file_type):
        if file_type in ["mp4", "avi", "mkv"]:
            return "movies", "../../../assets/images/movie.jpg"
        elif file_type in ["exe", "iso"]:
            return "games", "../../../assets/images/game.jpg"
        elif file_type in ["7z", "zip", "rar"]:
            return "programs", "../../../assets/images/program.jpg"
        else:
            return "more", "../../../assets/images/more.jpg"

    files_summary = []
    for file in files:
        category, image = get_category_and_image(file["type"])
        files_summary.append({
            "title": file["file_name"],
            "category": category,
            "image": image,
            "type": file["type"],
            "size": file["total_chunks"] * 20
        })

    return files_summary

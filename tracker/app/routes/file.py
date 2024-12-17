from fastapi import APIRouter, HTTPException, Body, Depends
from app.models.file import FileModel
from app.database.connection import peer_collection, file_collection
from app.utils.auth import get_current_peer

router = APIRouter()

@router.post("/add_file")
async def add_file(file_data: FileModel, current_peer=Depends(get_current_peer)):
    """
    Add a new file to the system.

    Input:
        file_data: {
            "file_name": "example_video.mp4",
            "chunks": [
                { "order": 1, "peers": ["peer1@example.com"] },
                { "order": 2, "peers": ["peer1@example.com"] }
            ]
        }
    Expected result:
        File is saved in the database.
    """
    # Check if the file already exists
    existing_file = await file_collection.find_one({"file_id": file_data.file_id})
    if existing_file:
        raise HTTPException(status_code=400, detail="File already exists")

    chunks = [{"order": i, "peers": [current_peer["email"]]} for i in range(file_data.total_chunks)]
    new_file = {
        "file_name": file_data.file_name,
        "total_chunks": file_data.total_chunks,
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
            "chunks": [1, 2]
        }
    Expected result:
        File's chunk ownership is updated in the database.
    """
    email = current_peer["email"]
    file_name = data["file_name"]
    chunks = data["chunks"]

    # Check if peer exists and is logged in
    peer = await peer_collection.find_one({"email": email, "logged_in": True})
    if not peer:
        raise HTTPException(status_code=401, detail="Peer not logged in")

    # Update chunk ownership
    for chunk_order in chunks:
        await file_collection.update_one(
            {"file_name": file_name, "chunks.order": chunk_order},
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
            "file_name": "file123",
            "chunks": Optional[List[int]]
        }
    Output:
        List of peers owning the requested chunks.
    """
    file_name = data["file_name"]
    requested_chunks = data.get("chunks", None)

    file = await file_collection.find_one({"file_name": file_name})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Fetch chunks
    chunks_to_return = file["chunks"] if requested_chunks is None else [
        chunk for chunk in file["chunks"] if chunk["order"] in requested_chunks
    ]

    result = []
    for chunk_data in chunks_to_return:
        valid_peers = []
        for peer_email  in chunk_data["peers"]:
            peer = await peer_collection.find_one({"email": peer_email , "logged_in": True})
            if peer:
                valid_peers.append({"email": peer["email"], "ip": peer["ip"], "port": peer["port"]})

        result.append({"chunk": chunk_data["order"], "peers": valid_peers})

    return {"peers": result}
from fastapi import APIRouter,UploadFile,File
from pathlib import Path
import shutil


router = APIRouter(
    prefix='/process-image',
    tags=['citizen']
)

# Define the directory where uploaded files will be saved
UPLOAD_DIRECTORY = Path("./uploads")

# Ensure the upload directory exists
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def receive_citizenship_image(file: UploadFile = File(...)):
    """
    Receives an image file and saves it to the uploads directory.
    The file field name must match 'file' as defined by the Node.js server.
    """
    try:
        # Construct the path where the file will be saved
        file_path = UPLOAD_DIRECTORY / file.filename

        # Use shutil to save the uploaded file to disk
        # file.file is a file-like object provided by FastAPI
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Log a message for successful file receipt
        print(f"Received and saved file: {file.filename}")

        # Return a success message
        return {
            "status": "success",
            "message": f"File '{file.filename}' received and saved.",
            "file_size": file.size,
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "status": "error",
            "message": "Failed to process the uploaded file."
        }
    finally:
        # Close the file stream after processing
        await file.close()





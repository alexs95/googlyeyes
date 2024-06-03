from cv2 import imdecode, imencode, IMREAD_COLOR
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import Response
from numpy import fromstring, uint8, frombuffer
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.config import settings
from app.core.lifespan import services

router = APIRouter()


@router.post("/transform", name="transform")
async def transform(file: UploadFile) -> Response:
    try:
        # Ensure the image is a JPEG
        if file.content_type != "image/jpeg":
            raise HTTPException(HTTP_400_BAD_REQUEST, detail=f"{file.content_type} file type is not supported.")

        # Read image into Numpy array
        contents = await file.read()
        image = imdecode(frombuffer(contents, dtype=uint8), IMREAD_COLOR)

        # Ensure image is not larger than max_image_dimension
        if max(image.shape) > settings.max_image_dimension:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                detail=f"Images with a dimension of greater than {settings.max_image_dimension} pixels are not supported."
            )

        # Run GooglyEye service
        image = services["googly"].run(image)

        # Convert image to JPEG format and return as bytes in Response
        _, stream = imencode(".jpg", image)
        return Response(content=stream.tobytes(), media_type="image/jpeg")

    finally:
        # Close SpooledTemporaryFile to ensure it is deleted if it spilled to disk
        file.file.close()


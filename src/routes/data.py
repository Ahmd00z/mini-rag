from fastapi import APIRouter, Depends, UploadFile

from controllers import DataController

from helpers.config import get_settings, Settings


data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()

    is_valid,result_signal = data_controller.validate_uploaded_file(file=file)

    return {
        "signal": result_signal
    }
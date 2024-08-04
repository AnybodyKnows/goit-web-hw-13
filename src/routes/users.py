import cloudinary
import cloudinary.uploader
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Path,
    Query,
    UploadFile,
    File,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.entity.models import User
from src.conf.config import config

from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.repository import users as repository_users

router = APIRouter(prefix="/users", tags=["users"])
cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user


@router.patch(
    "/avatar",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    public_idd = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_idd, owerwrite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_idd).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    print(res_url)
    user = await repository_users.update_avatar_url(user.email, res_url, db)
    return user

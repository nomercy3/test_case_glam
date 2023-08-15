# Imports
from fastapi import APIRouter, Depends

# Source code imports
from dependencies import (
    InstagramParserService,
    ImageUrlsResponseDTO,
    NotFoundHTTPException
)


instagram_router = APIRouter()


@instagram_router.get(
    path='/getPhotos',
    response_model=ImageUrlsResponseDTO,
    responses={404: {'description': 'Account not found'}},
    description='Returns photos urls for provided username and max_count number',
    summary='Get Photos'
)
async def get_photos(
        username: str,
        max_count: int,
        parse_service: InstagramParserService = Depends(InstagramParserService)
):
    try:
        response_data = await parse_service.parse(username, max_count)

        return ImageUrlsResponseDTO(urls=response_data)

    except ValueError:
        raise NotFoundHTTPException(detail='The account was not found or something went wrong')


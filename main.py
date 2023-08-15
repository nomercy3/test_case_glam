# Imports
from fastapi import FastAPI

# Source code imports
from routers.instagram import instagram_router
from dependencies import APITags


app = FastAPI(
    title='Glam API',
    version='1.0.0'
)

app.include_router(instagram_router, tags=[APITags.INSTAGRAM])

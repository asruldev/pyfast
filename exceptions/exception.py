from fastapi import Request
from fastapi.responses import JSONResponse

class StoryException(Exception):
  def __init__(self, name: str):
    self.name = name

def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )

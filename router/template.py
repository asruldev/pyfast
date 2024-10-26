from starlette.background import BackgroundTasks
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from custom_log import log

router = APIRouter(
    prefix='/template',
    tags=['Template']
)

templates = Jinja2Templates(directory='templates')

@router.get('/{id}', response_class=HTMLResponse)
def get_products(id: int, request: Request, bt: BackgroundTasks):
    bt.add_task(log_template_call, f"Template read for product with id {id}")
    return templates.TemplateResponse(
        'product.html',
        {
            "request": request,
            "id": id
        }
    )

def log_template_call(message: str):
    log("MY API", message)
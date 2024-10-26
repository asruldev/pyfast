from fastapi import APIRouter, Response, status, Form, Depends
from schemas import UserBase
from auth.oauth2 import get_current_user
from custom_log import log

router = APIRouter(
    prefix='/product',
    tags=['Product']
)

products = ['watch', 'camera', 'phone']

@router.get('')
def get_all_products():
    data = " ".join(products)
    log("GET Product", "ini data nya")
    return Response(content=data, media_type='text/plain', status_code=status.HTTP_200_OK)

@router.post('')
def create_product(name: str = Form(...), current_user: UserBase = Depends(get_current_user)):
    products.append(name)
    return {'products': products, 'user': current_user}
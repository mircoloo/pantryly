import httpx
from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2AuthorizationBearer
from core.security import verify_jwt
from config import PRODUCT_SERVICE_URL

router = APIRouter(prefix="/products")
oauth2 = OAuth2AuthorizationBearer()

@router.api_route("/{path:path}", methods=["GET", "POST"])
async def product_proxy(
    path: str,
    request: Request,
    token: str = Depends(oauth2)
):
    user = verify_jwt(token)

    headers = dict(request.headers)
    headers["x-user-id"] = user["sub"]

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            request.method,
            f"{PRODUCT_SERVICE_URL}/{path}",
            headers=headers,
            params=request.query_params,
            content=await request.body()
        )

    return resp.json()
from fastapi import Request, Response, APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.Auth_Schemas import (
    RegisterInSchema,
    LoginInSchema,
    LoginOutSchema,
    DeleteAccountSchema,
    RegesterOutSchema,
    UserOutSchema,
)
from app.core.depndencies import get_auth_service, get_current_user_by_cookie
from app.service.auth_service import AuthService
from app.core.cookies import set_cookies, clear_cookies
from jose import jwt

router = APIRouter()


# routers
@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserOutSchema,
    tags=["current user"],
)
async def get_current_user(current_user=Depends(get_current_user_by_cookie)):
    return current_user


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    tags=["register"],
    response_model=RegesterOutSchema,
)
async def register(
    payload: RegisterInSchema, service: AuthService = Depends(get_auth_service)
):

    try:
        user = await service.register(
            email=payload.email,
            plain_password=payload.password,
            username=payload.username,
        )

        return RegesterOutSchema(
            email=user.email, public_id=user.public_id, username=user.user_name
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login",
             status_code=status.HTTP_200_OK,
             response_model=LoginOutSchema,
             tags=["login"],
             )
async def login(
    request: Request,
    response: Response,
    payload: LoginInSchema,
    service: AuthService = Depends(get_auth_service),
):

    user_agent = request.headers.get("user-agent", "unknown")
    ip_address = request.headers.get("X-Forwarded-For", request.client.host)
    try:
        result = await service.login(
            email=payload.email,
            plain_password=payload.password,
            user_agent=user_agent,
            ip_address=ip_address,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")

    # set cookies
    set_cookies(
        response=response,
        access_token=result.get("access_token"),
        refresh_token=result.get("refresh_token"),
    )
    return {
        "R_token": result.get("refresh_token"),
        "user_public_id": result.get("user_public_id"),
        "email": result.get("email"),
    }


@router.post("/delete_account", tags=["delete account"])
async def delete_account(
    request: DeleteAccountSchema,
    refresh_token: str = Cookie(None),
    service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    await service.delete_account(
        plain_password=request.password, plain_refresh_token=refresh_token
    )


@router.post("/refresh_endpoint", tags=["refresh endpoint"])
async def refresh_endpoint(
    response: Response,
    request: Request,
    refresh_token: str = Cookie(None),
    service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
):
    user_agent = request.headers.get("user-agent", "unknown")
    ip_address = request.headers.get("X-Forwarded-For", request.client.host)

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    new_token_dict = await service.refresh_endpoint(refresh_token, user_agent=user_agent, ip_address=ip_address)

    access_token = new_token_dict["access_token"]
    refresh_token = new_token_dict["refresh_token"]

    set_cookies(
        response=response, access_token=access_token, refresh_token=refresh_token
    )

    return {"massege": "the Endpoint Refreshed"}


@router.post("/logout", tags=["Logout"])
async def logout(response: Response,
                 refresh_token: str = Cookie(None),
                 service: AuthService = Depends(get_auth_service),
                 ):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")

    await service.logout(refresh_token)
    clear_cookies(response)


@router.post("/global_logout", tags=["Global Logout"])
async def global_logout(response: Response,
                        access_token: str = Cookie(None),
                        service: AuthService = Depends(get_auth_service),
                        ):
    if not access_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    await service.logout_all_session(access_token)
    clear_cookies(response)

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from common import UnitOfWork, IUnitOfWork
from schemas import UserRead
from services import AuthService


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        uow: IUnitOfWork = UnitOfWork()
        auth_service = AuthService(is_verified=True, is_active=True, is_superuser=True)
        token = await auth_service.authenticate_user(
            email=email, password=password, uow=uow
        )
        request.session.update({"access_token": str(token.access_token, "utf-8")})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool | RedirectResponse:
        token = request.session.get("access_token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        auth_service = AuthService(is_verified=True, is_active=True, is_superuser=True)
        current_user: UserRead = await auth_service.validate_access_token(
            bytes(token, "utf-8")
        )
        await auth_service.check_user_state(current_user=current_user)

        if not current_user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        # Check the token in depth
        return True

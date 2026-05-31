from exceptions import AppException, NotFoundException, ConflictException, BadRequestException, UnauthorizedException
from fastapi import status, FastAPI, Request
from fastapi.responses import JSONResponse


STATUS_MAP: dict[type[AppException], int] = {
  NotFoundException: status.HTTP_404_NOT_FOUND,
  ConflictException: status.HTTP_409_CONFLICT,
  BadRequestException: status.HTTP_400_BAD_REQUEST,
  UnauthorizedException: status.HTTP_401_UNAUTHORIZED
}

def register_exception_handlers(app: FastAPI) -> None:
  @app.exception_handler(AppException)
  async def exception_handler(request: Request, exc: NotFoundException):
      code = STATUS_MAP.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
      return JSONResponse(
          status_code=code,
          content={"detail" : exc.detail}
      )

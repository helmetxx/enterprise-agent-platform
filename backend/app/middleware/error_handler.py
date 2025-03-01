from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
from app.core.exceptions import AppException

async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except AppException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"code": e.code, "message": e.message}
        )
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": "database_error", "message": "Database error occurred"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": "internal_error", "message": str(e)}
        ) 
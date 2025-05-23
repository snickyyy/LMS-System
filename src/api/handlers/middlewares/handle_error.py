from logging import getLogger

from fastapi import Request
from starlette.responses import JSONResponse

from api.errors.usecase import NotFoundError, BadRequestError, ObjectAlreadyExists, NotEnoughPermission
from api.schemas.response.base import ErrorResponse

logger = getLogger(__name__)

async def error_handling_middleware(request: Request, next: callable):
    try:
        response = await next(request)
        return response
    except NotFoundError as e:
        logger.error("NotFoundError: %s", str(e))
        return JSONResponse(ErrorResponse(msg=str(e)).model_dump(), status_code=404)

    except NotEnoughPermission as e:
        logger.error("NotEnoughPermission: %s", str(e))
        return JSONResponse(ErrorResponse(msg=str(e)).model_dump(), status_code=403)

    except ObjectAlreadyExists as e:
        logger.error("ObjectAlreadyExists: %s", str(e))
        return JSONResponse(ErrorResponse(msg=str(e)).model_dump(), status_code=409)

    except BadRequestError as e:
        logger.error("BadRequestError: %s", str(e))
        return JSONResponse(ErrorResponse(msg=str(e)).model_dump(), status_code=400)

    except Exception as e:
        logger.error("Internal Server Error: %s", str(e))
        return JSONResponse(ErrorResponse(msg="Internal Server Error, please try again later").model_dump(), status_code=503)


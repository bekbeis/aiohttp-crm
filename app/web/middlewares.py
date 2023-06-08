import typing
import json
from aiohttp_apispec.middlewares import validation_middleware
from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application

# В любую мидлвару всегда передается 2 аргумента:
# 1. request - текущий запрос
# 2. handler - следующая мидлвара или обработчик запроса (какой-то view)


@middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    # HTTPUnprocessableEntity (код 422) - это специальный код для ошибок валидации
    except HTTPUnprocessableEntity as e:
        return error_json_response(http_status=400, status='bad request', message=e.reason, data=json.loads(e.text))
    except HTTPException as e:
        return error_json_response(http_status=e.status, status='error', message=str(e))
    except Exception as e:
        return error_json_response(http_status=500, status='internal server error', message=str(e))


def setup_middlewares(app: "Application"):
    # Мидлвары, так же как и сигналы, вызываются в обратном порядке.
    # Поэтому хоть error_handling_middleware и стоит первым,
    # он будет вызван после validation_middleware.
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)

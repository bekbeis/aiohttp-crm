from aiohttp.web import Application as AiohttpApplicatoin, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequest
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from app.web.routes import setup_routes
from app.store.crm.accessor import CrmAccessor
from app.store import setup_accessors
from typing import Optional

# Переопределяем класс Application, чтобы добавить в него поле database,
# куда мы будем сохранять данные. Доступ к этому полю будет во всех
# view-функциях, где есть инстанция app.


class Application(AiohttpApplicatoin):
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None


# Переопределяем классы Request и View, чтобы добавить в них корректные
# тайпинги.

class Request(AiohttpRequest):
    @property
    def app(self) -> Application:
        return super().app


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request


# Основной класс aiohttp - Application, i.e. это и есть наш сервер
app = Application()


def run_app():
    setup_routes(app)
    setup_accessors(app)
    aiohttp_run_app(app)

# У нас может быть много подприложений, поэтому лучше сделать
# одну функцию setup_routes, которая будет объединять все
# внутренние установки путей

from aiohttp.web_app import Application
from app.crm.routes import setup_routes as crm_setup_routes


def setup_routes(app: Application):
    crm_setup_routes(app)

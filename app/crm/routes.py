import typing

from app.web.app import Application
from app.crm.views import AddUserView


# Установка роутов. Чтобы они работали,
# нужно эту функцию вызвать
def setup_routes(app: Application):
    # Если на страницу /page_name приходит GET-запрос,
    # то он попадет в нашу функцию function_name из views.py
    # выгдлядит это примерно так:
    # app.router.add_get('/page_name', function_name)
    app.router.add_view('/add_user', AddUserView)

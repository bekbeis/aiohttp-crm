import typing

# Условно: если идет проверка типов, то импортируем. В обратном случае, нет.
# Почему вообще это надо? Мы импортируем Application и напрямую, и цепочкой
# импортов через AddUserView. Программе (?) может быть непонятно,
# что и откуда тянуть первым.
if typing.TYPE_CHECKING:
    from app.web.app import Application

# Установка роутов. Чтобы они работали,
# нужно эту функцию вызвать

# Поставили в ковычки, так как нам не нужно работать
# непосредственно с этим классом. Нам нужно только знать
# его методы, чтобы были подсказки.


def setup_routes(app: "Application"):
    from app.crm.views import AddUserView, ListUsersView, GetUserView
    # Если на страницу /page_name приходит GET-запрос,
    # то он попадет в нашу функцию function_name из views.py
    # выгдлядит это примерно так:
    # app.router.add_get('/page_name', function_name)
    app.router.add_view('/add_user', AddUserView)
    app.router.add_view('/list_users', ListUsersView)
    app.router.add_view('/get_user', GetUserView)

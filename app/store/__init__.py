import typing
from app.store.crm.accessor import CrmAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_accessors(app: "Application"):
    app.crm_accessor = CrmAccessor()
    # Сигналы в Aiohttp - это некие события, которые обозначают
    # жизненные циклы приложения. Они аксессятся через app.on_signal_name
    # .on_signal_name.append(function_name) - добавляем function_name в
    # массив функций, которые будут вызваны при событии signal_name
    # Можно передавать много функций, которые будут вызваны в обратном порядке
    # (с последнего элемента в массиве функций).
    app.on_startup.append(app.crm_accessor.connect)
    app.on_cleanup.append(app.crm_accessor.disconnect)

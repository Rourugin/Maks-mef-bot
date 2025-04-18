from aiogram import Router

from app.handlers.main_h import main_r
from app.handlers.commands_h import commands_r
from app.handlers.unexpected_events_h import unexpected_event_r


def setup_routers() -> Router:
    router = Router()
    router.include_routers(main_r)
    router.include_routers(commands_r)
    router.include_routers(unexpected_event_r)
    return router

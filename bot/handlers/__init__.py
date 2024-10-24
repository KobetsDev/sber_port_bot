from .errors import dp
from .users import dp
from .event.events import dp
from .event.events_callback import dp
from .event.events_add import dp

from .message.send import dp
from .task.main import dp

__all__ = ["dp"]

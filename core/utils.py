import datetime
from typing import Any, NoReturn


def soft_delete(model_obj: Any) -> NoReturn:
    model_obj.deleted_at = datetime.datetime.now()
    model_obj.save()

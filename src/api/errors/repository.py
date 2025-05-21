from functools import wraps
from logging import Logger

from sqlalchemy.exc import DatabaseError, IntegrityError, DataError, ProgrammingError


class NotFound(Exception):
    ...

class AlreadyExists(Exception):
    ...

class InvalidData(Exception):
    ...

class InternalDatabaseError(Exception):
    ...

def handle_db_errors(logger: Logger):
    def internal(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IntegrityError as e:
                logger.error(e)
                raise AlreadyExists(e)
            except DataError as e:
                logger.error(e)
                raise InvalidData(e)
            except ProgrammingError as e:
                logger.error(e)
                raise InvalidData(e)
            except DatabaseError as e:
                logger.error(e)
                raise NotFound(e)
            except Exception as e:
                logger.error(e)
                raise InternalDatabaseError(e)
        return wrapper
    return internal
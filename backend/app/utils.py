from copy import copy

from fastapi import status, Request
from fastapi.responses import JSONResponse

from other.lessons import Lessons
import database.requests as rq
import other.log.colors as colors
import other.log.logging as logging
from other.PermissionsManager.models import Permissions
from other.PermissionsManager.PermissionsManager import PM


log = logging.logging(Name='UTILS', Color=colors.blue)
lessons = Lessons()


async def CheckUserID(user_id_request: int, user_id_check: int):
    log.debug(user_id_request, f'Checking {user_id_check}')

    if (await rq.GetUser(user_id_request, user_id_check)) == AttributeError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                    'status': 'fail',
                    'details': f'User \'{user_id_check}\' not found!'
                })


async def GetPermissions(user_id: int) -> Permissions | Exception:
    log.info(user_id, f'Getting permissions {user_id}')

    try:
        log.debug(user_id, f'Copying DefaultPermissions')
        permission = copy(PM.DefaultPermissions)

        user = await rq.GetUser(user_id, user_id)

        for role in user.roles:
            log.debug(user_id, f'Combining {role.name} [{role.role_id}]')
            permission = PM.Combine(user_id, permission,
                       PM.JSONToClass(user_id, role.permissions)
                       )

        return permission
    except Exception as Error:
        log.error(user_id, f'{Error}')


async def Error403(request: Request, user_id: int | str | None = None):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f'Not right enough to access: {request.base_url} | UserID: {user_id}')


async def GetLessons() -> Lessons:
    return lessons
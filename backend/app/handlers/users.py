from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import utils
import database.requests as rq
from handlers.bodies.core import Core
from handlers.bodies.edit_user import Body as EditUserBody


router = APIRouter(tags=['Users'])


@router.get('/GetUser', summary='Get user')
async def GetUser(body: Core):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None:
        return await utils.CheckUserID(body.UserID, body.UserID)

    user: rq.User = await rq.GetUser(body.UserID, body.UserID)
    roles: list[dict[str, str | dict[str, bool]]] = []
    for role in user.roles:
        roles.append({
            'role_id': role.role_id,
            'name': role.name,
            'permissions': role.permissions['permissions']
        })

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'user_id': user.user_id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'send_notifications': user.send_notifications,
        'roles': roles
    })


@router.get('/GetAdmins', summary='Get all users with permission admin')
async def GetAdmins(body: Core):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None:
        return await utils.CheckUserID(body.UserID, body.UserID)

    users: list[rq.User] = await rq.GetUsers(body.UserID)
    admins: dict[str, list[dict[str, int | str | None]]] = {
        'admins': []
    }

    for user in users:
        for role in user.roles:
            if role.permissions['permissions']['admin']:
                admins['admins'].append({
                    'user_id': user.user_id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'send_notifications': user.send_notifications
                })
                break

    return JSONResponse(status_code=status.HTTP_200_OK, content=admins)


@router.get('/GetUsers', summary='Get users')
async def GetUsers(body: Core):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None:
        return await utils.CheckUserID(body.UserID, body.UserID)

    users: list[rq.User] = await rq.GetUsers(body.UserID)
    users_json: list[dict[str, str]] = []

    for user in users:
        users_json.append({
            'user_id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'send_notifications': user.send_notifications
        })

    return JSONResponse(status_code=status.HTTP_200_OK, content={'users': users_json})


@router.post('/SetUser', summary='Set user')
async def SetUser(body: EditUserBody):
    if isinstance((await rq.GetUser(body.UserID, body.UserID)), rq.User):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                'status': 'fail',
                'details': 'User with such UserID already exists'
            })

    roles: list[rq.Role] = []
    for role_id in body.role_ids:
        role = await rq.GetRole(body.UserID, role_id)

        if role == rq.Role:
            roles.append(role)
        elif role == AttributeError:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                    'status': 'fail',
                    'details': 'There is no role with such ID'
                })

    await rq.SetUser(
        body.UserID,
        body.username,
        body.first_name,
        body.last_name,
        roles
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'success',
            'details': None
        })


@router.post('/UpdateUser', summary='Update user')
async def UpdateUser(body: EditUserBody):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None:
        return await utils.CheckUserID(body.UserID, body.UserID)

    for role_id in body.role_ids:
        if not isinstance(await rq.GetRole(body.UserID, role_id), rq.Role):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                    'status': 'fail',
                    'details': 'There is no role with such ID'
                })

    await rq.UpdateUser(
        body.UserID,
        body.username,
        body.first_name,
        body.last_name,
        body.send_notifications,
        body.role_ids
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'success',
            'details': None
        })

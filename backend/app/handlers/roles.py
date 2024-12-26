from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status

import utils
import database.requests as rq
from other.config import config
from handlers.bodies.core import Core
from handlers.bodies.edit_role import Body as EditRoleBody


router = APIRouter(tags=['Roles'])


@router.get('/GetRole', summary='Get role')
async def GetRole(RoleID: int, body: Core, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).admin_panel.use.role == False: return await utils.Error403(request, body.UserID)

    role: rq.Role = await rq.GetRole(body.UserID, RoleID)

    if role == AttributeError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                'status': 'fail',
                'details': 'There is no role with such a RoleID'
            })

    users = []
    for user in role.users:
        users.append({
            'user_id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'send_notifications': user.send_notifications
        })

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'role_id': role.role_id,
        'name': role.name,
        'permissions': role.permissions['permissions'],
        'users': users
    })


@router.get('/GetRoles', summary='Get roles')
async def GetRoles(body: Core, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).admin_panel.use.role == False: return await utils.Error403(request, body.UserID)

    roles: list[rq.Role] = await rq.GetRoles(body.UserID)
    roles_json: list[dict[str, str]] = []

    for role in roles:
        roles_json.append({
            'role_id': role.role_id,
            'name': role.name,
            'permissions': role.permissions,
        })
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={ 'roles': roles_json })


@router.post('/SetRole', summary='Set role')
async def SetRole(body: EditRoleBody, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).admin_panel.use.role == False: return await utils.Error403(request, body.UserID)

    if isinstance((await rq.GetRole(body.UserID, body.RoleID)), rq.Role):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                'status': 'fail',
                'details': 'The role with such an id already exists'
            })

    for user_id in body.user_ids:
        user = await rq.GetUser(body.UserID, user_id)

        if user == AttributeError:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                    'status': 'fail',
                    'details': f'A user with an id {user_id} was not found'
                })


    permissions = rq.PM.JSONToClass(body.UserID, { 'permissions': body.permissions })
    if isinstance(permissions, Exception) or permissions == Exception:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                'status': 'fail',
                'details': 'There was an error when processing permits'
            })

    await rq.SetRole(
        body.UserID,
        body.RoleID,
        body.user_ids,
        body.name,
        permissions
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'success',
            'details': None
        })


@router.post('/UpdateRole', summary='Update role')
async def UpdateRole(body: EditRoleBody, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).admin_panel.use.role == False: return await utils.Error403(request, body.UserID)

    if not isinstance((await rq.GetRole(body.UserID, body.RoleID)), rq.Role):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                'status': 'fail',
                'details': 'The role with such ID does not exist'
            })

    for user_id in body.user_ids:
        user = await rq.GetUser(body.UserID, user_id)

        if user == AttributeError:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                    'status': 'fail',
                    'details': f'A user with an id {user_id} was not found'
                })


    permissions = rq.PM.JSONToClass(body.UserID, { 'permissions': body.permissions })
    if isinstance(permissions, Exception) or permissions == Exception:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                'status': 'fail',
                'details': 'There was an error when processing permits'
            })

    await rq.UpdateRole(
        body.UserID,
        body.RoleID,
        body.user_ids,
        body.name,
        permissions
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'success',
            'details': None
        })


@router.delete('/DeleteRole', summary='Delete role')
async def DeleteRole(RoleID: int, body: Core, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).admin_panel.use.role == False: return await utils.Error403(request, body.UserID)

    role = await rq.GetRole(body.UserID, RoleID)

    if not isinstance(role, rq.Role):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                'status': 'fail',
                'details': 'The role with such ID does not exist'
            })

    elif RoleID == config.ID_ROLE_OWNER or RoleID == config.ID_ROLE_DEFAULT:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
                'status': 'fail',
                'details': f'It is impossible to delete the record from ID {RoleID} since it is determined by the variables of the environment'
            })

    await rq.DeleteRole(body.UserID, role)

    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'success',
            'details': None
        })

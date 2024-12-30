from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status

import utils
import database.requests as rq
from database.models import Lesson
from handlers.bodies.core import Core
from handlers.bodies.edit_lessons import Body as EditLessonsBody


router = APIRouter(tags=['Lessons'])


@router.get('/GetLessons', summary='Get lessons')
async def GetLessons(body: Core, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).lessons.use == False: return await utils.Error403(request, body.UserID)

    data_lessons: list[Lesson] = await rq.GetLessons(body.UserID)
    lessons: list[dict[str | None, bytes | None]] = []

    for lesson in data_lessons:
        lessons.append({
            'lesson_id': lesson.lesson_id,
            'lesson_name': await (await utils.GetLessons()).GetName(lesson.lesson_id),
            'homework': lesson.homework,
            'photo': list(lesson.photo) if lesson.photo != None else None,
            'url': lesson.url
        })

    return JSONResponse(status_code=status.HTTP_200_OK, content=lessons)


@router.get('/GetLesson', summary='Get lesson')
async def GetLesson(lesson_id: str, body: Core, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).lessons.use == False: return await utils.Error403(request, body.UserID)

    lesson_name = (await (await utils.GetLessons()).GetName(lesson_id))
    if lesson_name == NameError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            'status': 'fail',
            'details': f'Lessons \'{lesson_id}\' not found'
        })

    data_lesson: Lesson = await rq.GetLesson(body.UserID, lesson_id)
    if isinstance(data_lesson, Lesson):
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            'lesson_id': data_lesson.lesson_id,
            'lesson_name': lesson_name,
            'homework': data_lesson.homework,
            'photo': list(data_lesson.photo) if data_lesson.photo != None else None,
            'url': data_lesson.url
        })


@router.post('/UpdateLesson', summary='Update lessons')
async def SetLesson(body: EditLessonsBody, request: Request):
    if (await utils.CheckUserID(body.UserID, body.UserID)) != None: return await utils.CheckUserID(body.UserID, body.UserID)
    if (await utils.GetPermissions(body.UserID)).lessons.edit.homework == False: return await utils.Error403(request, body.UserID)
    elif (await utils.GetPermissions(body.UserID)).lessons.edit.photo == False: return await utils.Error403(request, body.UserID)
    elif (await utils.GetPermissions(body.UserID)).lessons.edit.url == False: return await utils.Error403(request, body.UserID)

    await rq.UpdateLesson(
        body.UserID,
        body.lessons_id,
        body.homework,
        bytes(body.photo) if body.photo != None else None,
        body.url
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={
            'status': 'success',
            'details': None
        })

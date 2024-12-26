from dataclasses import field, dataclass

from marshmallow import EXCLUDE, Schema
from marshmallow_dataclass import class_schema


__all__ = ['LessonsEdit', 'Lessons', 'Schedule', 'AdminPanelUse', 'AdminPanel', 'Permissions']


class PermissionsMetaSchema(Schema):
    class Meta:
        unknown = EXCLUDE


    def SetAll(self, value: bool) -> None:
        for field_name, field_value in self.__dataclass_fields__.items():
            if isinstance(getattr(self, field_name), bool):
                setattr(self, field_name, value)
            elif hasattr(getattr(self, field_name), '__dataclass_fields__'):
                nested_obj = getattr(self, field_name)
                nested_obj.SetAll(value)
        return self


@dataclass
class LessonsEdit(PermissionsMetaSchema):
    homework: bool = field(metadata=dict(data_key='homework'))
    photo: bool = field(metadata=dict(data_key='photo'))
    url: bool = field(metadata=dict(data_key='url'))


@dataclass
class Lessons(PermissionsMetaSchema):
    use: bool = field(metadata=dict(data_key='use'))
    edit: LessonsEdit  = field(metadata=dict(data_key='edit'))


@dataclass
class Schedule(PermissionsMetaSchema):
    use: bool = field(metadata=dict(data_key='use'))
    edit: bool = field(metadata=dict(data_key='edit'))


@dataclass
class ScheduleCall(PermissionsMetaSchema):
    use: bool = field(metadata=dict(data_key='use'))
    edit: bool = field(metadata=dict(data_key='edit'))


@dataclass
class AdminPanelUse(PermissionsMetaSchema):
    server_status: bool = field(metadata=dict(data_key='server_status'))
    newsletter: bool = field(metadata=dict(data_key='newsletter'))
    role: bool = field(metadata=dict(data_key='role'))


@dataclass
class AdminPanel(PermissionsMetaSchema):
    use: AdminPanelUse = field(metadata=dict(data_key='use'))


@dataclass
class Permissions(PermissionsMetaSchema):
    lessons: Lessons = field(metadata=dict(data_key='lessons'))
    schedule: Schedule = field(metadata=dict(data_key='schedule'))
    schedule_call: ScheduleCall = field(metadata=dict(data_key='schedule_call'))
    admin_panel: AdminPanel = field(metadata=dict(data_key='admin_panel'))
    admin: bool = field(metadata=dict(data_key='admin'))


PermissionsSchema = class_schema(Permissions)
LessonsSchema = class_schema(Lessons)
LessonsEditSchema = class_schema(LessonsEdit)
ScheduleSchema = class_schema(Schedule)
AdminPanelSchema = class_schema(AdminPanel)
AdminPanelUseSchema = class_schema(AdminPanelUse)

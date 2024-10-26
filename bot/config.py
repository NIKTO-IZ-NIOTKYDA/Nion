from os import getenv
from typing import Optional

__BOT_TOKEN__: Optional[str] = getenv('__BOT_TOKEN__')
__COMMAND_AP__: str = r'AdminPanel_4qB7cY9jZ2gP'
__DATABASE__: str = 'sqlite+aiosqlite:///bot/database/db.sqlite3'
__NO_FOUND_HOMEWORK_MSG__: str = 'Не добавлено домашнее задание =('
__VERSION__: str = r'Release 2.0.0 [dev]'  # X.X.X [stable\beta\dev]
__LOGING__: bool = True
__DEBUGGING__: bool = True
__WEBAPP_DEBUGGING__: bool = False
__WEBAPP_BACKEND_PORT__: int = 8000
__WEBAPP_FRONTEND_PORT__: int = 3000
__WEBAPP_HOST__: str = '0.0.0.0'
__WEBAPP_URL__: str = 'https://nion-webapp.netlify.app/form'
__WEBAPP_SECRET_KEY__: Optional[str] = getenv('__SECRET_KEY__')
__WEBAPP_ALGORITHM__: Optional[str] = getenv('__ALGORITHM__')
__LOG_FILE_NAME__: str = r'log.log'
__SCHEDULE_PATH_FILE__: str = r'bot/database/photo/schedule.png'
__TEMP_PHOTO_PATH_FILE__: str = r'bot/database/photo/tmp_photo.png'
__ADMIN_URL__: str = r'niktoizneotkyda_QQQ'
__LIST_ADMIN_ID__: list[int] = [5731571131, 5287168197, 1670389988]
__API_NETSCHOOL__: str = r'https://sgo.edu-74.ru/'
__SCHOOL_NAME__: str = r'МБОУ "СОШ № 10"'
__SALT512__: bytes = b'N\xc0\xfc\x98I>\xec\x11\x10p\xf6\xc7\xdd\xfd\xf4U_\x85\xd7\xbb\xff\x84\xc8\xb7m\xcd\xcbU\x11j\xb4\x99\xa1\x10\x02\x82vfK{\xe9\xb9l\x17_\xed\x0bx{\xf5C\x06\xfdZ\x17\xd7\xf5sP\xb9\xf2)M`\x00\xf3\xe5.f\x1cl\xefe\xdd\xc3\x1a\xe8:!E\xc7\xfe<\xf2\xa2\xff\x95{\x07\x12\x1cZ\xfa?\xb0 G;\xb2\x905{\xfb\xd1\x8e\xa7\xf9\x1f\xefY\xad\x9c\xc2\xc1-\xa6=llF\x85Qs^\x10v<\xe4}\xbc\x80l(!~SE\xf1k\xa4\x88\xe5Q\x99\xf7V{3CA\x98+Ng\x1c\xe0Gc\xaaxB\xb1\xf6t\xd0`n\xc6E\xa9\x84=\x04\xbf\xbcBa\x01\x03\x8b\xf3|\xc2\xcb=L\xfdw\x1fu\xe8\xce\x8c\x81\x8c\xa3\xf0O\x16\x0b\xa5\xe3\x8aj\xcc\xd7\xad\x93Ji<\xde\xc2\xa0\x0b\x06Z\xc7\xc1\x03\xb8\x9c\xbbM\x9f\x84\xb8t\xbf\xb5\x86\xa8\x81j\xec\xb8\x13a5\xe1\xab\xd2\x16\x01\x0e\x1cqK+\x93\xf0\x96{/\xe3\xdd`Z\xc7@O]\xb0\x86\x8f\xae\xb9S\xc0\x8d\x18\x87\x19\x9fs\x989D\xfe\x1e\xa0*@s\x89\xc7}\xc8\xdc\xc3@\xe3t;\x13\xd0"1\xb4=\xc2_\xa3=v:\x06\xceV\xdeZ\xc9!b\xd8\x94\x19\xc5\x8d7\x05\xc3\xb0\xa1I.\xb0V\x1eB\x8b0\xde\x1f\x1bw\xe9\xed`\x84\td\xbe*\x0c\xcbJ_S\xc5a\x89\xa7\x95\xc6Xy\xa4\xdc\x0f\x8f\xf1\xfb\x1e\xbcw\x19|\xa9\xdd\x1c_s\x14{\xa8t\xb3"\x1a\x84M \x00w{F\xa8\xf9\xd6\xad\xfc\x91!\x8f\x1e\x99LO\x0b\xcd\xd9\xaf\x8a\x91v\x19\xeb#1\xef\x97\xcf\xfe\x87\xbc\xe4;\xccCA\x8fh\x7f\xc3\x183H4\xc5\x90\x1eV\x96^\xdeG\xfd\xf1C[~\x19\xafZ\xb7R\xb7f45\x15\x0e\x18\x82\xfe|\xaf\x98\xd5\xc6m\xd0\xa9]A\xd7p\xd5\xc8\xadSbk\x1f\x81\xe2\xf9y\xa5N{\x9fM\xebU\x11\x92\xf58\x1a\xab\xae\x11\xc9-\x84\xb4\x0b\xe1\\.\x10\xde\xb9\x9d\xe4\x84y_\xfa\xcc'

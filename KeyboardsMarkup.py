from telebot import types

# Start
markup_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
DZ = types.KeyboardButton('Домашнее задание 📚')
schedule = types.KeyboardButton('Расписание 📑')
call_schedule = types.KeyboardButton('Расписание звонков 🕝')
markup_start.add(DZ, schedule, call_schedule)

markup_photo = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
schedule = types.KeyboardButton(text='Расписание')
dz = types.KeyboardButton(text='Д/З')
back_photo = types.KeyboardButton(text='⬅️ Назад')
markup_photo.add(schedule, dz, back_photo)

# DZ
markup_dz = types.InlineKeyboardMarkup()
russian_lang = types.InlineKeyboardButton(text='Русский язык', callback_data='russian_lang')
literature = types.InlineKeyboardButton(text='Литература', callback_data='literature')
native_literature = types.InlineKeyboardButton(text='Родноя литература', callback_data='native_literature')
english_lang_1 = types.InlineKeyboardButton(text='Англ. Яз. (1 группа)', callback_data='english_lang_1')
english_lang_2 = types.InlineKeyboardButton(text='Англ. Яз. (2 группа)', callback_data='english_lang_2')
algebra = types.InlineKeyboardButton(text='Алгебра', callback_data='algebra')
geometry = types.InlineKeyboardButton(text='Геометрия', callback_data='geometry')
TBIS = types.InlineKeyboardButton(text='Теория вероятностей и статистика', callback_data='TBIS')
computer_science = types.InlineKeyboardButton(text='Информатика', callback_data='computer_science')
story = types.InlineKeyboardButton(text='История', callback_data='story')
social_science = types.InlineKeyboardButton(text='Обществознание', callback_data='social_science')
geography = types.InlineKeyboardButton(text='География', callback_data='geography')
physics = types.InlineKeyboardButton(text='Физика', callback_data='physics')
chemistry = types.InlineKeyboardButton(text='Химия', callback_data='chemistry')
biology = types.InlineKeyboardButton(text='Биология', callback_data='biology')
music = types.InlineKeyboardButton(text='Музыка', callback_data='music')
technology = types.InlineKeyboardButton(text='Технология', callback_data='technology')
OBZH = types.InlineKeyboardButton(text='ОБЖ', callback_data='OBZH')
markup_dz.add(russian_lang, literature, native_literature, english_lang_1, english_lang_2, algebra, geometry, TBIS, computer_science, story, social_science, geography, physics, chemistry, biology, music, technology, OBZH)

markup_back = types.InlineKeyboardMarkup()
back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back')
markup_back.add(back)

# DZ update
markup_dz_update = types.InlineKeyboardMarkup()
russian_lang_update = types.InlineKeyboardButton(text='Русский язык (r)', callback_data='russian_lang_update')
literature_update = types.InlineKeyboardButton(text='Литература (r)', callback_data='literature_update')
native_literature_update = types.InlineKeyboardButton(text='Родноя литература (r)', callback_data='native_literature_update')
english_lang_1_update = types.InlineKeyboardButton(text='Англ. Яз. (1 группа) (r)', callback_data='english_lang_1_update')
english_lang_2_update = types.InlineKeyboardButton(text='Англ. Яз. (2 группа) (r)', callback_data='english_lang_2_update')
algebra_update = types.InlineKeyboardButton(text='Алгебра (r)', callback_data='algebra_update')
geometry_update = types.InlineKeyboardButton(text='Геометрия (r)', callback_data='geometry_update')
TBIS_update = types.InlineKeyboardButton(text='Теория вероятностей и статистика (r)', callback_data='TBIS_update')
computer_science_update = types.InlineKeyboardButton(text='Информатика (r)', callback_data='computer_science_update')
story_update = types.InlineKeyboardButton(text='История (r)', callback_data='story_update')
social_science_update = types.InlineKeyboardButton(text='Обществознание (r)', callback_data='social_science_update')
geography_update = types.InlineKeyboardButton(text='География (r)', callback_data='geography_update')
physics_update = types.InlineKeyboardButton(text='Физика (r)', callback_data='physics_update')
chemistry_update = types.InlineKeyboardButton(text='Химия (r)', callback_data='chemistry_update')
biology_update = types.InlineKeyboardButton(text='Биология (r)', callback_data='biology_update')
music_update = types.InlineKeyboardButton(text='Музыка (r)', callback_data='music_update')
technology_update = types.InlineKeyboardButton(text='Технология (r)', callback_data='technology_update')
OBZH_update = types.InlineKeyboardButton(text='ОБЖ (r)', callback_data='OBZH_update')
markup_dz_update.add(russian_lang_update, literature_update, native_literature_update, english_lang_1_update, english_lang_2_update, algebra_update, geometry_update, TBIS_update, computer_science_update, story_update, social_science_update, geography_update, physics_update, chemistry_update, biology_update, music_update, technology_update, OBZH_update)

# DZ and photo update
markup_dz_update_p = types.InlineKeyboardMarkup()
russian_lang_update_p = types.InlineKeyboardButton(text='Русский язык (rp)', callback_data='russian_lang_update_p')
literature_update_p = types.InlineKeyboardButton(text='Литература (rp)', callback_data='literature_update_p')
native_literature_update_p = types.InlineKeyboardButton(text='Родноя литература (rp)', callback_data='native_literature_update_p')
english_lang_1_update_p = types.InlineKeyboardButton(text='Англ. Яз. (1 группа) (rp)', callback_data='english_lang_1_update_p')
english_lang_2_update_p = types.InlineKeyboardButton(text='Англ. Яз. (2 группа) (rp)', callback_data='english_lang_2_update_p')
algebra_update_p = types.InlineKeyboardButton(text='Алгебра (rp)', callback_data='algebra_update_p')
geometry_update_p = types.InlineKeyboardButton(text='Геометрия (rp)', callback_data='geometry_update_p')
TBIS_update_p = types.InlineKeyboardButton(text='Теория вероятностей и статистика (rp)', callback_data='TBIS_update_p')
computer_science_update_p = types.InlineKeyboardButton(text='Информатика (rp)', callback_data='computer_science_update_p')
story_update_p = types.InlineKeyboardButton(text='История (rp)', callback_data='story_update_p')
social_science_update_p = types.InlineKeyboardButton(text='Обществознание (rp)', callback_data='social_science_update_p')
geography_update_p = types.InlineKeyboardButton(text='География (rp)', callback_data='geography_update_p')
physics_update_p = types.InlineKeyboardButton(text='Физика (rp)', callback_data='physics_update_p')
chemistry_update_p = types.InlineKeyboardButton(text='Химия (rp)', callback_data='chemistry_update_p')
biology_update_p = types.InlineKeyboardButton(text='Биология (rp)', callback_data='biology_update_p')
music_update_p = types.InlineKeyboardButton(text='Музыка (rp)', callback_data='music_update_p')
technology_update_p = types.InlineKeyboardButton(text='Технология (rp)', callback_data='technology_update_p')
OBZH_update_p = types.InlineKeyboardButton(text='ОБЖ (rp)', callback_data='OBZH_update_p')
markup_dz_update_p.add(russian_lang_update_p, literature_update_p, native_literature_update_p, english_lang_1_update_p, english_lang_2_update_p, algebra_update_p, geometry_update_p, TBIS_update_p, computer_science_update_p, story_update_p, social_science_update_p, geography_update_p, physics_update_p, chemistry_update_p, biology_update_p, music_update_p, technology_update_p, OBZH_update_p)

# send nummer
markup_send_nummer = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
nummer = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
markup_send_nummer.add(nummer)

# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
mailing = types.KeyboardButton('Рассылка✉️')
# reboot = types.KeyboardButton('Перезагрузка 🔄')
backup_db = types.KeyboardButton('Бэкап базы данных 📑')
info = types.KeyboardButton('Статус сервера 🛠️')
markup_admin_panel.add(mailing, backup_db, info)  # *deleted reboot

markup_chack_mailing = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes = types.KeyboardButton('✅ YES ✅')
no = types.KeyboardButton('❌ NO ❌')
markup_chack_mailing.add(yes, no)

# -=-=-=-=-=-=-=-=-=- End Admin Panel -=-=-=-=-=-=-=-=-=- #

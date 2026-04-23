"""Переводы — ru/uz/en + функции t() и detect_language()"""

from bot.emojis import E

TRANSLATIONS = {
    # === start ===
    "start.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет, {{name}}!</b>\n\n"
            f"{E['music']} Я бот для изменения голоса.\n\n"
            f"{E['pin']} <b>Как пользоваться:</b>\n"
            f"Отправь голосовое или аудио — я применю эффект! {E['plane']}\n\n"
            "Выбери действие ниже:"
        ),
        "uz": (
            f"{E['bot']} <b>Salom, {{name}}!</b>\n\n"
            f"{E['music']} Men ovozni o'zgartiruvchi botman.\n\n"
            f"{E['pin']} <b>Qanday foydalanish:</b>\n"
            f"Ovozli xabar yoki audio yuboring — men effekt qo'llashaman! {E['plane']}\n\n"
            "Quyidagi tugmalardan birini tanla:"
        ),
        "en": (
            f"{E['bot']} <b>Hello, {{name}}!</b>\n\n"
            f"{E['music']} I'm a voice changer bot.\n\n"
            f"{E['pin']} <b>How to use:</b>\n"
            f"Send a voice message or audio — I'll apply an effect! {E['plane']}\n\n"
            "Choose an action below:"
        ),
    },

    # === кнопки ===
    "btn.voice_effect": {
        "ru": "Изменить голос",
        "uz": "Ovozni o'zgartirish",
        "en": "Change voice",
    },
    "btn.profile": {
        "ru": "Профиль",
        "uz": "Profil",
        "en": "Profile",
    },
    "btn.help": {
        "ru": "Помощь",
        "uz": "Yordam",
        "en": "Help",
    },
    "btn.language": {
        "ru": "Язык",
        "uz": "Til",
        "en": "Language",
    },
    "btn.admin_panel": {
        "ru": "Админ-панель",
        "uz": "Admin panel",
        "en": "Admin panel",
    },
    "btn.back": {
        "ru": "Назад",
        "uz": "Orqaga",
        "en": "Back",
    },
    "btn.check_sub": {
        "ru": "Проверить подписку",
        "uz": "Obunani tekshirish",
        "en": "Check subscription",
    },
    "btn.cancel": {
        "ru": "Отмена",
        "uz": "Bekor qilish",
        "en": "Cancel",
    },
    "btn.another_effect": {
        "ru": "Другой эффект",
        "uz": "Boshqa effekt",
        "en": "Another effect",
    },
    # === кнопки админки ===
    "btn.admin_stats": {
        "ru": "Статистика",
        "uz": "Statistika",
        "en": "Statistics",
    },
    "btn.admin_channels": {
        "ru": "Каналы",
        "uz": "Kanallar",
        "en": "Channels",
    },
    "btn.admin_broadcast": {
        "ru": "Рассылка",
        "uz": "Xabar tarqatish",
        "en": "Broadcast",
    },
    "btn.admin_home": {
        "ru": "Главное меню",
        "uz": "Bosh menyu",
        "en": "Main menu",
    },
    "btn.admin_add": {
        "ru": "Добавить канал",
        "uz": "Kanal qo'shish",
        "en": "Add channel",
    },
    "btn.admin_back": {
        "ru": "Назад",
        "uz": "Orqaga",
        "en": "Back",
    },
    "btn.admin_cancel": {
        "ru": "Отмена",
        "uz": "Bekor qilish",
        "en": "Cancel",
    },
    "btn.admin_confirm_del": {
        "ru": "Удалить",
        "uz": "O'chirish",
        "en": "Delete",
    },
    "btn.admin_cancel_del": {
        "ru": "Оставить",
        "uz": "Qoldirish",
        "en": "Keep",
    },

    # === эффекты ===
    "effect.chipmunk": {
        "ru": "Бурундук",
        "uz": "Olmaxon",
        "en": "Chipmunk",
    },
    "effect.bass": {
        "ru": "Бас",
        "uz": "Bass",
        "en": "Bass",
    },
    "effect.robot": {
        "ru": "Робот",
        "uz": "Robot",
        "en": "Robot",
    },
    "effect.whisper": {
        "ru": "Шёпот",
        "uz": "Shivirlash",
        "en": "Whisper",
    },
    "effect.speed_up": {
        "ru": "Ускорение",
        "uz": "Tezlashtirish",
        "en": "Speed up",
    },
    "effect.slow_down": {
        "ru": "Замедление",
        "uz": "Sekinlashtirish",
        "en": "Slow down",
    },
    "effect.radio": {
        "ru": "Радио",
        "uz": "Radio",
        "en": "Radio",
    },
    "effect.helium": {
        "ru": "Гелий",
        "uz": "Geliy",
        "en": "Helium",
    },
    "effect.cathedral": {
        "ru": "Собор",
        "uz": "Sobor",
        "en": "Cathedral",
    },
    "effect.ghost": {
        "ru": "Призрак",
        "uz": "Arvoh",
        "en": "Ghost",
    },
    "effect.studio": {
        "ru": "Студия",
        "uz": "Studiya",
        "en": "Studio",
    },
    "effect.vinyl": {
        "ru": "Винил",
        "uz": "Vinil",
        "en": "Vinyl",
    },
    "effect.phaser": {
        "ru": "Фазер",
        "uz": "Fazer",
        "en": "Phaser",
    },
    "effect.megaphone": {
        "ru": "Мегафон",
        "uz": "Megafon",
        "en": "Megaphone",
    },
    "effect.podcast": {
        "ru": "Подкаст",
        "uz": "Podkast",
        "en": "Podcast",
    },
    "effect.dubstep": {
        "ru": "Дабстеп",
        "uz": "Dabstep",
        "en": "Dubstep",
    },
    # === voice (доменные сообщения) ===
    "voice.send_audio": {
        "ru": f"{E['music']} Отправь мне голосовое сообщение или аудиофайл, и я изменю его!",
        "uz": f"{E['music']} Menga ovozli xabar yoki audio fayl yuboring, men uni o'zgartiraman!",
        "en": f"{E['music']} Send me a voice message or audio file, and I'll change it!",
    },
    "voice.choose_effect": {
        "ru": f"{E['gear']} <b>Выбери эффект для голосового сообщения:</b>",
        "uz": f"{E['gear']} <b>Ovozli xabar uchun effektni tanla:</b>",
        "en": f"{E['gear']} <b>Choose an effect for the voice message:</b>",
    },
    "voice.processing": {
        "ru": f"{E['clock']} Применяю эффект <b>{{effect}}</b>...",
        "uz": f"{E['clock']} <b>{{effect}}</b> effekti qo'llanmoqda...",
        "en": f"{E['clock']} Applying <b>{{effect}}</b> effect...",
    },
    "voice.done": {
        "ru": f"{E['check']} Готово! Эффект <b>{{effect}}</b> применён.",
        "uz": f"{E['check']} Tayyor! <b>{{effect}}</b> effekti qo'llandi.",
        "en": f"{E['check']} Done! <b>{{effect}}</b> effect applied.",
    },
    "voice.busy": {
        "ru": f"{E['clock']} Подожди, ещё обрабатываю предыдущее сообщение...",
        "uz": f"{E['clock']} Kuting, oldingi xabar hali qayta ishlanmoqda...",
        "en": f"{E['clock']} Please wait, still processing the previous message...",
    },
    "voice.cancelled": {
        "ru": f"{E['cross']} Обработка отменена.",
        "uz": f"{E['cross']} Qayta ishlash bekor qilindi.",
        "en": f"{E['cross']} Processing cancelled.",
    },
    "voice.error_not_audio": {
        "ru": f"{E['warning']} Отправь голосовое сообщение или аудиофайл.",
        "uz": f"{E['warning']} Ovozli xabar yoki audio fayl yuboring.",
        "en": f"{E['warning']} Send a voice message or audio file.",
    },
    "voice.error_download": {
        "ru": f"{E['cross']} Не удалось скачать файл. Попробуй ещё раз.",
        "uz": f"{E['cross']} Faylni yuklab bo'lmadi. Qayta urinib ko'ring.",
        "en": f"{E['cross']} Failed to download the file. Try again.",
    },
    "voice.error_ffmpeg": {
        "ru": f"{E['cross']} Ошибка обработки аудио. Попробуй другой файл.",
        "uz": f"{E['cross']} Audio qayta ishlashda xatolik. Boshqa fayl yuboring.",
        "en": f"{E['cross']} Audio processing error. Try a different file.",
    },

    # === профиль ===
    "profile.title": {
        "ru": (
            f"{E['profile']} <b>Твой профиль</b>\n\n"
            f"{E['edit']} Имя: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['music']} Эффектов применено: {{downloads}}"
        ),
        "uz": (
            f"{E['profile']} <b>Sening profiling</b>\n\n"
            f"{E['edit']} Ism: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['music']} Qo'llangan effektlar: {{downloads}}"
        ),
        "en": (
            f"{E['profile']} <b>Your profile</b>\n\n"
            f"{E['edit']} Name: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['music']} Effects applied: {{downloads}}"
        ),
    },

    # === помощь ===
    "help.text": {
        "ru": (
            f"{E['book']} <b>Помощь</b>\n\n"
            f"{E['star']} Отправь голосовое или аудио — получишь файл с эффектом\n"
            f"{E['star']} 16 эффектов: Студия, Бурундук, Гелий, Бас, Робот, Призрак, Шёпот, Радио, Собор, Мегафон, Фазер, Винил, Подкаст, Дабстеп, Ускорение, Замедление\n"
            f"{E['lock']} Макс. размер файла: 20 МБ\n\n"
            f"{E['plane']} По вопросам: @{{admin_username}}"
        ),
        "uz": (
            f"{E['book']} <b>Yordam</b>\n\n"
            f"{E['star']} Ovozli xabar yoki audio yuboring — effektli fayl olasiz\n"
            f"{E['star']} 16 ta effekt: Studiya, Olmaxon, Geliy, Bass, Robot, Arvoh, Shivirlash, Radio, Sobor, Megafon, Fazer, Vinil, Podkast, Dabstep, Tezlashtirish, Sekinlashtirish\n"
            f"{E['lock']} Maks. fayl hajmi: 20 MB\n\n"
            f"{E['plane']} Savollar bo'lsa: @{{admin_username}}"
        ),
        "en": (
            f"{E['book']} <b>Help</b>\n\n"
            f"{E['star']} Send a voice or audio — get a file with effect\n"
            f"{E['star']} 16 effects: Studio, Chipmunk, Helium, Bass, Robot, Ghost, Whisper, Radio, Cathedral, Megaphone, Phaser, Vinyl, Podcast, Dubstep, Speed up, Slow down\n"
            f"{E['lock']} Max file size: 20 MB\n\n"
            f"{E['plane']} Contact: @{{admin_username}}"
        ),
    },

    # === подписка ===
    "sub.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет!</b>\n\n"
            f"{E['music']} Этот бот меняет голос в аудио — быстро и бесплатно!\n\n"
            f"{E['lock']} <b>Для начала подпишись на каналы ниже:</b>\n\n"
            f"После подписки нажми «{E['check']} Проверить подписку»"
        ),
        "uz": (
            f"{E['bot']} <b>Salom!</b>\n\n"
            f"{E['music']} Bu bot audiodagi ovozni o'zgartiradi — tez va bepul!\n\n"
            f"{E['lock']} <b>Boshlash uchun quyidagi kanallarga obuna bo'ling:</b>\n\n"
            f"Obuna bo'lgandan keyin «{E['check']} Obunani tekshirish» tugmasini bosing"
        ),
        "en": (
            f"{E['bot']} <b>Hello!</b>\n\n"
            f"{E['music']} This bot changes voice in audio — fast and free!\n\n"
            f"{E['lock']} <b>To start, subscribe to the channels below:</b>\n\n"
            f"After subscribing, tap «{E['check']} Check subscription»"
        ),
    },
    "sub.not_subscribed": {
        "ru": (
            f"{E['cross']} <b>Ты ещё не подписался на все каналы:</b>\n\n"
            f"Подпишись и нажми «{E['check']} Проверить подписку» ещё раз."
        ),
        "uz": (
            f"{E['cross']} <b>Sen hali barcha kanallarga obuna bo'lmading:</b>\n\n"
            f"Obuna bo'ling va «{E['check']} Obunani tekshirish» tugmasini qayta bosing."
        ),
        "en": (
            f"{E['cross']} <b>You haven't subscribed to all channels yet:</b>\n\n"
            f"Subscribe and tap «{E['check']} Check subscription» again."
        ),
    },
    "sub.success": {
        "ru": f"{E['check']} <b>Отлично, {{name}}!</b> Подписка подтверждена. Добро пожаловать! {E['plane']}",
        "uz": f"{E['check']} <b>Ajoyib, {{name}}!</b> Obuna tasdiqlandi. Xush kelibsiz! {E['plane']}",
        "en": f"{E['check']} <b>Great, {{name}}!</b> Subscription confirmed. Welcome! {E['plane']}",
    },
    "sub.not_required": {
        "ru": f"{E['check']} Подписка не требуется!",
        "uz": f"{E['check']} Obuna talab qilinmaydi!",
        "en": f"{E['check']} No subscription required!",
    },
    "sub.check_alert_ok": {
        "ru": f"{E['check']} Подписка подтверждена!",
        "uz": f"{E['check']} Obuna tasdiqlandi!",
        "en": f"{E['check']} Subscription confirmed!",
    },
    "sub.check_alert_fail": {
        "ru": f"{E['cross']} Подпишись на все каналы!",
        "uz": f"{E['cross']} Barcha kanallarga obuna bo'ling!",
        "en": f"{E['cross']} Subscribe to all channels!",
    },

    # === ошибки ===
    "error.rate_limit": {
        "ru": f"{E['clock']} <b>Слишком много запросов!</b>\n\nПодожди {{seconds}} сек.",
        "uz": f"{E['clock']} <b>Juda ko'p so'rovlar!</b>\n\n{{seconds}} soniya kuting.",
        "en": f"{E['clock']} <b>Too many requests!</b>\n\nWait {{seconds}} sec.",
    },
    "error.generic": {
        "ru": f"{E['cross']} <b>Ошибка</b>\n\nПопробуй позже.",
        "uz": f"{E['cross']} <b>Xatolik</b>\n\nKeyinroq qayta urinib ko'ring.",
        "en": f"{E['cross']} <b>Error</b>\n\nTry again later.",
    },
    "error.too_large": {
        "ru": f"{E['package']} <b>Файл слишком большой</b>\n\nМаксимум 20 МБ.",
        "uz": f"{E['package']} <b>Fayl juda katta</b>\n\nMaksimum 20 MB.",
        "en": f"{E['package']} <b>File too large</b>\n\nMaximum 20 MB.",
    },
    "error.timeout": {
        "ru": f"{E['clock']} <b>Превышено время ожидания</b>\n\nПопробуй позже.",
        "uz": f"{E['clock']} <b>Kutish vaqti tugadi</b>\n\nKeyinroq qayta urinib ko'ring.",
        "en": f"{E['clock']} <b>Request timed out</b>\n\nTry again later.",
    },

    # === язык ===
    "lang.choose": {
        "ru": f"{E['gear']} <b>Выбери язык:</b>",
        "uz": f"{E['gear']} <b>Tilni tanlang:</b>",
        "en": f"{E['gear']} <b>Choose language:</b>",
    },
    "lang.changed": {
        "ru": f"{E['check']} Язык изменён на русский",
        "uz": f"{E['check']} Til o'zbek tiliga o'zgartirildi",
        "en": f"{E['check']} Language changed to English",
    },

    # === админ ===
    "admin.title": {
        "ru": f"{E['gear']} <b>Админ-панель</b>\n\nВыбери действие:",
        "uz": f"{E['gear']} <b>Admin panel</b>\n\nAmalni tanlang:",
        "en": f"{E['gear']} <b>Admin panel</b>\n\nChoose an action:",
    },
    "admin.no_access": {
        "ru": f"{E['lock']} У тебя нет доступа к админке.",
        "uz": f"{E['lock']} Sizda admin panelga kirish huquqi yo'q.",
        "en": f"{E['lock']} You don't have access to admin panel.",
    },
    "admin.stats": {
        "ru": (
            f"{E['chart']} <b>Статистика бота</b>\n\n"
            f"{E['users']} Всего юзеров: <b>{{total_users}}</b>\n"
            f"{E['star']} Новых сегодня: <b>{{today_users}}</b>\n"
            f"{E['music']} Всего эффектов: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Каналов: <b>{{total_channels}}</b>"
        ),
        "uz": (
            f"{E['chart']} <b>Bot statistikasi</b>\n\n"
            f"{E['users']} Jami foydalanuvchilar: <b>{{total_users}}</b>\n"
            f"{E['star']} Bugungi yangilar: <b>{{today_users}}</b>\n"
            f"{E['music']} Jami effektlar: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Kanallar: <b>{{total_channels}}</b>"
        ),
        "en": (
            f"{E['chart']} <b>Bot statistics</b>\n\n"
            f"{E['users']} Total users: <b>{{total_users}}</b>\n"
            f"{E['star']} New today: <b>{{today_users}}</b>\n"
            f"{E['music']} Total effects: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Channels: <b>{{total_channels}}</b>"
        ),
    },
    "admin.channels_empty": {
        "ru": f"{E['megaphone']} <b>Каналы</b>\n\nСписок пуст. Добавь канал кнопкой ниже.",
        "uz": f"{E['megaphone']} <b>Kanallar</b>\n\nRo'yxat bo'sh. Quyidagi tugma orqali kanal qo'shing.",
        "en": f"{E['megaphone']} <b>Channels</b>\n\nList is empty. Add a channel using the button below.",
    },
    "admin.channels_title": {
        "ru": f"{E['megaphone']} <b>Каналы для подписки:</b>\n",
        "uz": f"{E['megaphone']} <b>Obuna kanallari:</b>\n",
        "en": f"{E['megaphone']} <b>Subscription channels:</b>\n",
    },
    "admin.add_channel_id": {
        "ru": f"{E['megaphone']} <b>Добавление канала</b>\n\nОтправь <b>ID канала</b> (например <code>-1001234567890</code>)\n\n{E['bulb']} Узнать ID: добавь бота @getmyid_bot в канал",
        "uz": f"{E['megaphone']} <b>Kanal qo'shish</b>\n\n<b>Kanal ID</b> raqamini yuboring (masalan <code>-1001234567890</code>)\n\n{E['bulb']} ID bilish: @getmyid_bot ni kanalga qo'shing",
        "en": f"{E['megaphone']} <b>Add channel</b>\n\nSend the <b>channel ID</b> (e.g. <code>-1001234567890</code>)\n\n{E['bulb']} Get ID: add @getmyid_bot to the channel",
    },
    "admin.add_channel_title": {
        "ru": f"{E['edit']} Теперь отправь <b>название канала</b>:",
        "uz": f"{E['edit']} Endi <b>kanal nomini</b> yuboring:",
        "en": f"{E['edit']} Now send the <b>channel name</b>:",
    },
    "admin.add_channel_link": {
        "ru": f"{E['link']} Теперь отправь <b>ссылку или юзернейм канала</b>\n\nПринимаю: <code>t.me/...</code> или <code>@username</code>",
        "uz": f"{E['link']} Endi <b>kanal havolasi yoki username</b> yuboring\n\nQabul qilinadi: <code>t.me/...</code> yoki <code>@username</code>",
        "en": f"{E['link']} Now send the <b>channel link or username</b>\n\nAccepted: <code>t.me/...</code> or <code>@username</code>",
    },
    "admin.id_not_number": {
        "ru": f"{E['cross']} ID должен быть числом. Попробуй ещё раз:",
        "uz": f"{E['cross']} ID raqam bo'lishi kerak. Qayta urinib ko'ring:",
        "en": f"{E['cross']} ID must be a number. Try again:",
    },
    "admin.title_too_long": {
        "ru": f"{E['cross']} Название слишком длинное (макс 200 символов)",
        "uz": f"{E['cross']} Nom juda uzun (maks 200 belgi)",
        "en": f"{E['cross']} Name is too long (max 200 characters)",
    },
    "admin.link_invalid": {
        "ru": f"{E['cross']} Не удалось распознать ссылку.\nПопробуй ещё:",
        "uz": f"{E['cross']} Havolani aniqlab bo'lmadi.\nQayta urinib ko'ring:",
        "en": f"{E['cross']} Could not parse the link.\nTry again:",
    },
    "admin.channel_added": {
        "ru": f"{E['check']} <b>Канал добавлен!</b>",
        "uz": f"{E['check']} <b>Kanal qo'shildi!</b>",
        "en": f"{E['check']} <b>Channel added!</b>",
    },
    "admin.confirm_delete": {
        "ru": f"{E['warning']} <b>Удалить канал?</b>\n\nID: <code>{{channel_id}}</code>\n\nЭто действие нельзя отменить.",
        "uz": f"{E['warning']} <b>Kanalni o'chirishni xohlaysizmi?</b>\n\nID: <code>{{channel_id}}</code>\n\nBu amalni qaytarib bo'lmaydi.",
        "en": f"{E['warning']} <b>Delete channel?</b>\n\nID: <code>{{channel_id}}</code>\n\nThis action cannot be undone.",
    },
    "admin.channel_deleted": {
        "ru": f"{E['check']} Канал удалён",
        "uz": f"{E['check']} Kanal o'chirildi",
        "en": f"{E['check']} Channel deleted",
    },
    "admin.channel_not_found": {
        "ru": f"{E['cross']} Канал не найден",
        "uz": f"{E['cross']} Kanal topilmadi",
        "en": f"{E['cross']} Channel not found",
    },
    "admin.broadcast_prompt": {
        "ru": f"{E['plane']} <b>Массовая рассылка</b>\n\nОтправь текст/фото/видео для рассылки.",
        "uz": f"{E['plane']} <b>Ommaviy xabar</b>\n\nYuborish uchun matn/rasm/video yuboring.",
        "en": f"{E['plane']} <b>Mass broadcast</b>\n\nSend text/photo/video to broadcast.",
    },
    "admin.broadcast_preview": {
        "ru": f"{E['eye']} <b>Предпросмотр</b>\n\nОтправить это сообщение всем юзерам?",
        "uz": f"{E['eye']} <b>Oldindan ko'rish</b>\n\nBu xabarni barcha foydalanuvchilarga yuborishni xohlaysizmi?",
        "en": f"{E['eye']} <b>Preview</b>\n\nSend this message to all users?",
    },
    "admin.broadcast_confirm": {
        "ru": "Отправить",
        "uz": "Yuborish",
        "en": "Send",
    },
    "admin.broadcast_cancel": {
        "ru": "Отмена",
        "uz": "Bekor qilish",
        "en": "Cancel",
    },
    "admin.broadcast.no_message": {
        "ru": "Нет сообщения",
        "uz": "Xabar yo'q",
        "en": "No message",
    },
    "admin.broadcast_started": {
        "ru": f"{E['plane']} Рассылка запущена... Ожидай отчёт.",
        "uz": f"{E['plane']} Xabar yuborilmoqda... Hisobotni kuting.",
        "en": f"{E['plane']} Broadcast started... Wait for report.",
    },
    "admin.broadcast_done": {
        "ru": f"{E['chart']} <b>Рассылка завершена!</b>\n\n{E['check']} Доставлено: <b>{{success}}</b>\n{E['cross']} Ошибок: <b>{{failed}}</b>\n{E['users']} Всего: <b>{{total}}</b>",
        "uz": f"{E['chart']} <b>Xabar yuborish tugadi!</b>\n\n{E['check']} Yetkazildi: <b>{{success}}</b>\n{E['cross']} Xatolar: <b>{{failed}}</b>\n{E['users']} Jami: <b>{{total}}</b>",
        "en": f"{E['chart']} <b>Broadcast complete!</b>\n\n{E['check']} Delivered: <b>{{success}}</b>\n{E['cross']} Failed: <b>{{failed}}</b>\n{E['users']} Total: <b>{{total}}</b>",
    },

    # === команды (меню Telegram) ===
    "cmd.start": {
        "ru": "Запустить бота",
        "uz": "Botni ishga tushirish",
        "en": "Start the bot",
    },
    "cmd.menu": {
        "ru": "Главное меню",
        "uz": "Bosh menyu",
        "en": "Main menu",
    },
    "cmd.profile": {
        "ru": "Мой профиль",
        "uz": "Mening profilim",
        "en": "My profile",
    },
    "cmd.help": {
        "ru": "Помощь",
        "uz": "Yordam",
        "en": "Help",
    },
    "cmd.language": {
        "ru": "Сменить язык",
        "uz": "Tilni o'zgartirish",
        "en": "Change language",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить перевод по ключу и языку"""
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(lang, entry.get("ru", key))
    return text.format(**kwargs) if kwargs else text


def detect_language(language_code: str | None) -> str:
    """Определяет язык по коду из Telegram"""
    if not language_code:
        return "en"
    if language_code.startswith("ru"):
        return "ru"
    if language_code.startswith("uz"):
        return "uz"
    return "en"

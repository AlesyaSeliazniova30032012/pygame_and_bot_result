from telebot import types


kb = types.InlineKeyboardMarkup()
kb_help = types.InlineKeyboardButton(text='Выдай коррдинаты неубежавшего квадрата', callback_data='coordinate')
kb_screen = types.InlineKeyboardButton(text='Хочу скрин начала игры', callback_data='scrin')
kb.add(kb_help, kb_screen)

# kb_help = types.InlineKeyboardMarkup()
# kb_help.add(kb_screen)
#
# kb_screen = types.InlineKeyboardMarkup()
# kb_screen.add(kb_help)

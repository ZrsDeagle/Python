from telebot.types import ChatPermissions
import telebot

# Banlama yetkisi kontrolü
def can_ban(chat_id, user_id):
    chat_admins = bot.get_chat_administrators(chat_id)
    for admin in chat_admins:
        if admin.user.id == user_id:
            if admin.status == 'creator' or admin.can_restrict_members:
                return True
    return False

# Kullanıcının yönetici olup olmadığını kontrol etme
def is_admin(chat_id, user_id):
    chat_admins = bot.get_chat_administrators(chat_id)
    for admin in chat_admins:
        if admin.user.id == user_id:
            return True
    return False

# Botun yönetici olup olmadığını kontrol etme
def bot_is_admin(chat_id):
    bot_info = bot.get_me()
    chat_admins = bot.get_chat_administrators(chat_id)
    for admin in chat_admins:
        if admin.user.id == bot_info.id:
            return True
    return False

@bot.message_handler(commands=['ban'])
def ban(message):
    if not bot_is_admin(message.chat.id):
        bot.reply_to(message, "Kimseyi banlamak için yetkim yok.")
        return

    if not can_ban(message.chat.id, message.from_user.id):
        bot.reply_to(message, "Banlama yetkiniz yok.")
        return
    
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id_text = message.text.split()[1]
            if user_id_text.startswith('@'):
                user_info = bot.get_chat_member(message.chat.id, user_id_text)
                user_id = user_info.user.id
            else:
                user_id = int(user_id_text)
        except (IndexError, ValueError):
            bot.reply_to(message, "Lütfen geçerli bir kullanıcı ID'si veya kullanıcı adı girin.")
            return
    
    try:
        bot.ban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, f"Kullanıcı {user_id} banlandı.")
    except Exception as e:
        bot.reply_to(message, f"Banlama sırasında bir hata oluştu: {e}")

@bot.message_handler(commands=['mute'])
def mute(message):
    if not bot_is_admin(message.chat.id):
        bot.reply_to(message, "Kimseyi susturmak için yetkim yok.")
        return

    if not can_ban(message.chat.id, message.from_user.id):
        bot.reply_to(message, "Susturma yetkiniz yok.")
        return
    
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id_text = message.text.split()[1]
            if user_id_text.startswith('@'):
                user_info = bot.get_chat_member(message.chat.id, user_id_text)
                user_id = user_info.user.id
            else:
                user_id = int(user_id_text)
        except (IndexError, ValueError):
            bot.reply_to(message, "Lütfen geçerli bir kullanıcı ID'si veya kullanıcı adı girin.")
            return
    
    try:
        bot.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
        bot.reply_to(message, f"Kullanıcı {user_id} susturuldu.")
    except Exception as e:
        bot.reply_to(message, f"Susturma sırasında bir hata oluştu: {e}")

bot.polling()
    

@bot.message_handler(commands=['unban'])
def unban(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "Bu komutu kullanabilmek için yönetici olmanız gerekiyor.")
        return

    if not bot_is_admin(message.chat.id):
        bot.reply_to(message, "Yasak kaldırma işlemi için gerekli yetkim yok.")
        return

    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, "Lütfen geçerli bir kullanıcı ID'si girin.")
        return

    try:
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, f"Kullanıcının yasağı kaldırıldı: {user_id}")
    except Exception as e:
        bot.reply_to(message, f"Yasak kaldırma işlemi sırasında bir hata oluştu: {e}")

@bot.message_handler(commands=['unmute'])
def unmute(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "Bu komutu kullanabilmek için yönetici olmanız gerekiyor.")
        return

    if not bot_is_admin(message.chat.id):
        bot.reply_to(message, "Susturma kaldırma işlemi için gerekli yetkim yok.")
        return

    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, "Lütfen geçerli bir kullanıcı ID'si girin.")
        return

    try:
        permissions = ChatPermissions(can_send_messages=True)
        bot.restrict_chat_member(message.chat.id, user_id, permissions=permissions)
        bot.reply_to(message, f"Kullanıcının susturması kaldırıldı: {user_id}")
    except Exception as e:
        bot.reply_to(message, f"Susturma kaldırma işlemi sırasında bir hata oluştu: {e}")

bot.polling()
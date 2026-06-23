from telegram import ChatPermissions
from telegram.ext import Updater, MessageHandler, Filters
import os
import time

TOKEN = os.getenv("BOT_TOKEN")

FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True
)

def fix_permissions(chat_id, user_id, context):
    for _ in range(3):
        try:
            context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=FULL_PERMISSIONS
            )
            time.sleep(1)
        except Exception as e:
            print(e)

def handle_new_members(update, context):
    for user in update.message.new_chat_members:
        time.sleep(2)
        fix_permissions(update.effective_chat.id, user.id, context)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, handle_new_members))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

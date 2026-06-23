import os
import time
from telegram import ChatPermissions, Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")


FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
)


async def fix_permissions(chat_id, user_id, context):

    for i in range(3):

        try:
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=FULL_PERMISSIONS
            )

            time.sleep(1)

        except Exception as e:
            print(e)



async def handle_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    for user in update.message.new_chat_members:

        print(f"Fixing permissions for {user.id}")

        time.sleep(2)

        await fix_permissions(
            chat_id,
            user.id,
            context
        )



def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            handle_new_members
        )
    )

    print("Bot running")

    app.run_polling()



if __name__ == "__main__":
    main()

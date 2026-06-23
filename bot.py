import os
import asyncio

from telegram import ChatPermissions, Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")


FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_audios=False,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=False,
    can_send_voice_notes=False,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=False
)


async def fix_member(chat_id, user_id, context):

    # retry because NUSVerifyBot may apply permissions later
    for i in range(10):

        try:

            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=FULL_PERMISSIONS
            )

            print(
                f"Fixed permissions for {user_id}, attempt {i+1}"
            )

        except Exception as e:
            print("Error:", e)


        # wait 5 seconds before trying again
        await asyncio.sleep(5)



async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id


    for user in update.message.new_chat_members:

        print(
            f"New member detected: {user.id}"
        )


        asyncio.create_task(
            fix_member(
                chat_id,
                user.id,
                context
            )
        )



def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            new_member
        )
    )


    print("Bot running")

    app.run_polling(
        allowed_updates=["message"]
    )



if __name__ == "__main__":

    main()

import os
import asyncio

from telegram import ChatPermissions, Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    ContextTypes
)


TOKEN = os.getenv("BOT_TOKEN")


# Permissions you want verified users to have
FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_audios=True,
    can_send_documents=True,     # THIS enables files
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
)


async def fix_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    change = update.chat_member

    if not change:
        return


    chat_id = change.chat.id
    user_id = change.new_chat_member.user.id


    print(
        f"Detected member update: {user_id}"
    )


    # wait for NUSVerifyBot to finish
    await asyncio.sleep(3)


    try:

        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=FULL_PERMISSIONS
        )

        print(
            f"Fixed permissions for {user_id}"
        )


    except Exception as e:

        print(
            "Error:",
            e
        )



def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    app.add_handler(
        ChatMemberHandler(
            fix_user,
            ChatMemberHandler.CHAT_MEMBER
        )
    )


    print("Bot running")

    app.run_polling()



if __name__ == "__main__":

    main()


from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ReactionEmoji
from asyncio import sleep

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot.')

async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.effective_user)
    print(update.message.text)
    await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                           message_id=update.message.message_id,
                                           reaction=ReactionEmoji.GHOST)
    await update.message.reply_text('No respondo pendejadas')
    await sleep(2)
    await update.message.reply_text('Y menos a maricas')
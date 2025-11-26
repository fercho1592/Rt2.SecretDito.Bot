from telegram import Update
from telegram.ext import ContextTypes
from dependency import getRepoInstance
from models.User import User


async def registroHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repo = getRepoInstance()
    user = await repo.getUserById(update.message.from_user.id)
    if user is not None:
        await update.message.reply_text('Ya estás registrado.')
        return

    user = User(update.message.from_user.id, update.message.from_user.username)
    await repo.createUser(user)

    user = await repo.getUserById(update.message.from_user.id)
    if user is not None:
        await update.message.reply_text('Occurrió un error durante el registro. Por favor, intenta de nuevo más tarde.')
        return

    # Lógica para registrar al usuario
    await update.message.reply_text('Registro completado!')
    pass

async def getWishListHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repo = getRepoInstance()
    # validar que usuario este registrado
    user = await repo.getUserById(update.message.from_user.id)
    if user is None:
        await update.message.reply_text('Por favor, regístrate primero usando /registro')
        return

    # Lógica para obtener el wish list
    wish_list_text = "Tu wish list:\n"
    for item in user.wish_list:
        wish_list_text += f"- {item['item']}\n"

    await update.message.reply_text(wish_list_text)
    pass

async def wishListReigisterHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repo = getRepoInstance()
    # validar que usuario este registrado
    user = await repo.getUserById(update.message.from_user.id)
    if user is None:
        await update.message.reply_text('Por favor, regístrate primero usando /registro')
        return
        # Lógica para registrar el wish list

    user.wish_list.append({"item": update.message.text, "message_id": update.message.message_id})
    await repo.updateUser(user)
    await update.message.reply_text('Wish list registrado!')
    pass

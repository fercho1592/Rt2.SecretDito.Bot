from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ReactionEmoji
from dependency import getRepoInstance
from models.User import User
from models.WishListItem import WishListItem

class SecretDitoControllers:
    @staticmethod
    async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        help_text = (
            'Comandos disponibles:\n'
            '/registro - Regístrate para usar el bot.\n'
            '/wish_list - Obtén tu lista de deseos.\n'
            'Envía mensajes con los ítems que deseas agregar a tu lista de deseos.\n'
            'Reacciona a un regalo con 🔥 o 👎 para eliminarlo de tu lista de deseos.\n'
        )
        await update.message.reply_text(help_text)
        pass

    @staticmethod
    async def registro_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        try:
            repo = getRepoInstance()
            user = await repo.GetUserById(update.message.from_user.id)
            if user is not None:
                await update.message.reply_text('Ya estás registrado.')
                return

            user = User(update.message.from_user.id, update.message.from_user.username)
            await repo.CreateUser(user)
        
            # Lógica para registrar al usuario
            await update.message.reply_text('Registro completado!')
            await update.message.reply_text('Puedes compartirme tu wish list enviando mensajes con los ítems que deseas agregar.')
        except Exception as e:
            print(f'Error en registroHandler: {e}')
            await update.message.reply_text('Occurrió un error durante el registro. Por favor, intenta de nuevo más tarde.')
        pass

    @staticmethod
    async def get_wish_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        try:
            repo = getRepoInstance()
            # validar que usuario este registrado
            user = await repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return

            for item in user.wish_list:
                reply_message = await update.message.reply_text(str(item))
                item.message_ids.append(reply_message.message_id)

            await repo.UpdateUser(user)

            if user.username is None and user.name is None:
                await update.message.reply_text('Usa el comando /set_name para establecer tu nombre y que otros usuarios puedan identificarte mejor.')
        except Exception as e:
            print(f'Error en getWishListHandler: {e}')
            await update.message.reply_text('Ocurrió un error al obtener tu wish list. Reporta al inutil del administrador para que haga algo.')
        pass

    @staticmethod
    async def wish_list_register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            repo = getRepoInstance()
            # validar que usuario este registrado
            user = await repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return
                # Lógica para registrar el wish list

            user.wish_list.append(WishListItem(item=update.message.text, message_ids=[update.message.message_id]))
            await repo.UpdateUser(user)
            await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                            message_id=update.message.message_id,
                                            reaction=ReactionEmoji.THUMBS_UP)
            if user.username is None and user.name is None:
                await update.message.reply_text('Usa el comando /set_name para establecer tu nombre y que otros usuarios puedan identificarte mejor.')
        except Exception as e:
            print(f'Error en wishListReigisterHandler: {e}')
            await update.message.reply_text('Ocurrió un error al registrar tu wish list. Reporta al inutil del administrador para que haga algo.')
        pass

    @staticmethod
    async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            print (f'Reaction received: {update}')
            repo = getRepoInstance()
            user = await repo.GetUserById(update.message_reaction.user.id)
            if user is None:
                return

            # Buscar el ítem en la wish list basado en el message_id
            item_to_remove = None
            # get message text by message id using api
            message = await context.bot.get_message(chat_id=update.chat.id,
                                                    message_id=update.message_id)
            for item in user.wish_list:
                if item['item'] == message.text:
                    item_to_remove = item
                    break

            if item_to_remove is None:
                return

            # Verificar la reacción y eliminar el ítem si es necesario
            if update.new_reaction.emoji in [ReactionEmoji.FIRE, ReactionEmoji.THUMBS_DOWN]:
                user.wish_list.remove(item_to_remove)
                await repo.UpdateUser(user)
                await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                                message_id=update.reaction.message.message_id,
                                                reaction=ReactionEmoji.CHECK_MARK)
        except Exception as e:
            print(f'Error en reactionHandler: {e}')
        pass

    @staticmethod
    async def set_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            repo = getRepoInstance()
            user = await repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return

            # Obtener el nombre del mensaje
            name = ' '.join(context.args)
            if not name:
                await update.message.reply_text('Por favor, proporciona un nombre después del comando. Ejemplo: /set_name Naruto Uzumaki')
                return

            user.name = name
            await repo.UpdateUser(user)
            await update.message.reply_text(f'Su nombre ha sido establecido a: {name}')
        except Exception as e:
            print(f'Error en setNameHandler: {e}')
            await update.message.reply_text('Ocurrió un error al establecer tu nombre. Reporta al inutil del administrador para que haga algo.')
        pass

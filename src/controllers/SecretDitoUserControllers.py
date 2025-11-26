from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ReactionEmoji
from dependency import getRepoInstance
from models.WishListItem import WishListItem

class SecretDitoUserControllers:
    @staticmethod
    async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        welcome_text = (
            '¡Bienvenido a SecretDito Bot!\n'
            'Usa /registro para registrarte y empezar a llenar tu wish list.\n'
            'O usa el comando /help para ver los comandos disponibles.'
        )
        await update.message.reply_text(welcome_text)
        pass

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
                                            reaction=ReactionEmoji.CHRISTMAS_TREE)
            if user.username is None and user.name is None:
                await update.message.reply_text('Usa el comando /set_name para establecer tu nombre y que otros usuarios puedan identificarte mejor.')
        except Exception as e:
            print(f'Error en wishListReigisterHandler: {e}')
            await update.message.reply_text('Ocurrió un error al registrar tu wish list. Reporta al inutil del administrador para que haga algo.')
        pass

    @staticmethod
    async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            repo = getRepoInstance()
            user = await repo.GetUserById(update.message_reaction.user.id)
            if user is None:
                return

            # Buscar el ítem en la wish list basado en el message_id
            item_to_remove = None
            for item in user.wish_list:
                if update.message_reaction.message_id in item.message_ids:
                    item_to_remove = item
                    break

            if item_to_remove is None:
                return

            # Verificar la reacción y eliminar el ítem si es necesario
            reacted_emoji = [r.emoji for r in update.message_reaction.new_reaction]
            if any(emoji in [ReactionEmoji.FIRE, ReactionEmoji.THUMBS_DOWN] for emoji in reacted_emoji):
                user.wish_list.remove(item_to_remove)
                await repo.UpdateUser(user)
                await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                                message_id=update.message_reaction.message_id,
                                                reaction=ReactionEmoji.SEE_NO_EVIL_MONKEY)
                await update.message.reply_text(f'Ítem {item_to_remove.item} eliminado de tu wish list.')
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

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ReactionEmoji
from models.WishListItem import WishListItem
from interfaces.repo_protocols import ISecretDitoRepo
from interfaces.config_protocols import FlagServiceProtocol

class SecretDitoUserControllers:
    def __init__(self, repo: ISecretDitoRepo, flag_service: FlagServiceProtocol) -> None:
        self.repo = repo
        self.flag_service = flag_service
        pass

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if(self.flag_service.is_asignation_done()):
            await update.message.reply_text(
                'El asignación de amigos secretos ya ha sido realizada. ' +
                'Por favor contacta al administrador para más información.'
            )
            return
        
        await update.message.reply_text('¡Bienvenido a SecretDito Bot!\n'
            'Usa /registro para registrarte y empezar a llenar tu wish list.\n'
            'O usa el comando /help para ver los comandos disponibles.')
        pass

    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if(self.flag_service.is_asignation_done()):
            await update.message.reply_text(
                'Comandos disponibles:\n'
                '/wish_list - Tu lista de deseos.\n'
                '/secret_friend - Nombre de tu amigo secreto.\n'
                '/secret_wish_list - Lista de deseos de tu amigo secreto.\n'
                'Envía mensajes con el ítem que deseas agregar a tu lista.\n'
                'Reacciona a un regalo con 🔥 o 👎 para eliminarlo de tu lista.\n'
            )
            return
        help_text = (
            'Comandos disponibles:\n'
            '/registro - Regístrate para usar el bot.\n'
            '/wish_list - Tu lista de deseos.\n'
            'Envía mensajes con el ítem que deseas agregar a tu lista.\n'
            'Reacciona a un regalo con 🔥 o 👎 para eliminarlo de tu lista.\n'
        )
        await update.message.reply_text(help_text)
        pass

    async def get_wish_list_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        try:
            # validar que usuario este registrado
            user = await self.repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return

            await user.show_wish_list(update.message.reply_text,\
                lambda message_response: message_response.message_id)

            await self.repo.UpdateUser(user)

            if user.username is None and user.name is None:
                await update.message.reply_text('Usa el comando /set_name para establecer tu nombre y que otros usuarios puedan identificarte mejor.')
        except Exception as e:
            print(f'Error en getWishListHandler: {e}')
            await update.message.reply_text('Ocurrió un error al obtener tu wish list. Reporta al inutil del administrador para que haga algo.')
        pass

    async def add_to_wish_list_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            # validar que usuario este registrado
            user = await self.repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return
                # Lógica para registrar el wish list

            wishlist_item = WishListItem(item=update.message.text, message_ids=[update.message.message_id])
            user.add_to_wish_list(wishlist_item)

            await self.repo.UpdateUser(user)
            await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                            message_id=update.message.message_id,
                                            reaction=ReactionEmoji.CHRISTMAS_TREE)
            if user.username is None and user.name is None:
                await update.message.reply_text('Usa el comando /set_name para establecer tu nombre y que otros usuarios puedan identificarte mejor.')
        except Exception as e:
            print(f'Error en addToWishListHandler: {e}')
            await update.message.reply_text('Ocurrió un error al registrar tu wish list. Reporta al inutil del administrador para que haga algo.')
        pass

    async def delete_from_wish_list_by_reaction_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user = await self.repo.GetUserById(update.message_reaction.user.id)
            if user is None:
                return

            reacted_emoji = [r.emoji for r in update.message_reaction.new_reaction]
            if all(emoji in [ReactionEmoji.FIRE, ReactionEmoji.THUMBS_DOWN] for emoji in reacted_emoji):
                return
            
            item_removed = user.remove_wish_list_item_by_message_id(update.message_reaction.message_id)
            if item_removed is None:
                return

            await self.repo.UpdateUser(user)
            await context.bot.set_message_reaction(chat_id=update.effective_chat.id,
                                            message_id=update.message_reaction.message_id,
                                            reaction=ReactionEmoji.SEE_NO_EVIL_MONKEY)
                
            # await update.message.reply_text(f'Ítem {item_removed.item} eliminado de tu wish list.')
        except Exception as e:
            print(f'Error en delete_from_wish_list_by_reaction_handler: {e}')
            await update.message.reply_text('Ocurrió un error al eliminar un ítem de tu wish list. Reporta al inutil del administrador para que haga algo.')
        pass

    async def set_name_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user = await self.repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return

            # Obtener el nombre del mensaje
            name = ' '.join(context.args)
            if not name:
                await update.message.reply_text('Por favor, proporciona un nombre después del comando. Ejemplo: /set_name Naruto Uzumaki')
                return

            user.set_name(name)
            await self.repo.UpdateUser(user)

            await update.message.reply_text(f'Su nombre ha sido establecido a: {name}')
        except Exception as e:
            print(f'Error en setNameHandler: {e}')
            await update.message.reply_text('Ocurrió un error al establecer tu nombre. Reporta al inutil del administrador para que haga algo.')
        pass

    async def get_secret_friend_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        try:
            user = await self.repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('No estás registrado para este Secret Dito.\n '+\
                    'Notifica al administrador para organizar otro sorteo.')
                return

            if user.secret_friend_id is None:
                await update.message.reply_text('Aún no se te ha asignado un amigo secreto. Por favor espera.')
                return

            secret_friend = await self.repo.GetUserById(user.secret_friend_id)
            if secret_friend is None:
                await update.message.reply_text('Error al obtener los datos de tu amigo secreto. '+\
                                            'Reporta al inutil del administrador para que haga algo.')
                return

            message = f'Tu amigo secreto es: {secret_friend.name}'
            await update.message.reply_text(message)
        except Exception as e:
            print(f'Error en getSecretFriendHandler: {e}')
            await update.message.reply_text('Ocurrió un error al obtener a tu amigo secreto.'+\
                                            'Reporta al inutil del administrador para que haga algo.')
        pass

    async def get_secret_friend_wish_list_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        try:
            user = await self.repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('No estás registrado para este Secret Dito.\n '+\
                    'Notifica al administrador para organizar otro sorteo.')
                return

            if user.secret_friend_id is None:
                await update.message.reply_text('Aún no se te ha asignado un amigo secreto. Por favor espera.')
                return

            secret_friend = await self.repo.GetUserById(user.secret_friend_id)
            if secret_friend is None:
                await update.message.reply_text('Error al obtener los datos de tu amigo secreto. '+\
                                            'Reporta al inutil del administrador para que haga algo.')
                return

            await secret_friend.show_wish_list(update.message.reply_text, None)
        except Exception as e:
            print(f'Error en getSecretFriendWishListHandler: {e}')
            await update.message.reply_text('Ocurrió un error al obtener a tu amigo secreto.'+\
                                            'Reporta al inutil del administrador para que haga algo.')
        pass

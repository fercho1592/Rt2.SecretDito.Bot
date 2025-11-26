from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from controllers.SecretDitoUserControllers import SecretDitoUserControllers
from dependency import getRepoInstance
from models.User import User

class SecretDitoUserConversationController:
    class ConversationState:
        SET_NAME = 0

    @staticmethod
    async def entry_point(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        del context
        try:
            repo = getRepoInstance()
            user = await repo.GetUserById(update.message.from_user.id)
            if user is not None:
                await update.message.reply_text('Ya estás registrado.')
                return

            user = User(update.message.from_user.id, update.message.from_user.username, update.message.chat_id)
            await repo.CreateUser(user)
        
            # Lógica para registrar al usuario
            await update.message.reply_text('Registro completado!')
            await update.message.reply_text('Ayudame a que sea mas facil identificarte. ¿Cuál es tu nombre?')
        except Exception as e:
            print(f'Error en registroHandler: {e}')
            await update.message.reply_text('Occurrió un error durante el registro. Por favor, intenta de nuevo más tarde.')
        pass
        return SecretDitoUserConversationController.ConversationState.SET_NAME

    @staticmethod
    async def set_name_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            repo = getRepoInstance()
            user = await repo.GetUserById(update.message.from_user.id)
            if user is None:
                await update.message.reply_text('Por favor, regístrate primero usando /registro')
                return

            # Obtener el nombre del mensaje
            name = update.message.text
            if not name:
                await update.message.reply_text('Por favor, proporciona un nombre.')
                return

            user.name = name
            await repo.UpdateUser(user)
            await update.message.reply_text(f'Su nombre ha sido establecido a: {name}')
        except Exception as e:
            print(f'Error en setNameHandler: {e}')
            await update.message.reply_text('Ocurrió un error al establecer tu nombre. Reporta al inutil del administrador para que haga algo.')
        pass
        
        return ConversationHandler.END
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Application, MessageReactionHandler
from dependency import getConfigService
from interfaces.config_reader.ConfigEnum import ConfigEnum

from controllers.SecretDitoUserControllers import SecretDitoUserControllers

def BuildApp() -> Application:
    bot_token = getConfigService().get_service_api_key(ConfigEnum.TELEGRAM_TOKEN)

    app = ApplicationBuilder().token(bot_token).build()
    return app

if __name__ == '__main__':
    print('Starting bot...')
    app = BuildApp()

    print('Registering handlers...')
    app.add_handler(CommandHandler('registro', SecretDitoUserControllers.registro_handler))
    app.add_handler(CommandHandler('wish_list', SecretDitoUserControllers.get_wish_list_handler))
    app.add_handler(CommandHandler('set_name', SecretDitoUserControllers.set_name_handler))
    app.add_handler(CommandHandler('help', SecretDitoUserControllers.help_handler))
    app.add_handler(CommandHandler('start', SecretDitoUserControllers.help_handler))
    app.add_handler(MessageReactionHandler(SecretDitoUserControllers.reaction_handler))
    app.add_handler(MessageHandler(None, SecretDitoUserControllers.wish_list_register_handler))

    print('Running bot...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)

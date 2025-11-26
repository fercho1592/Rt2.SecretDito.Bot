from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Application, MessageReactionHandler

from SecretDitoHandlers import registroHandler, getWishListHandler, wishListReigisterHandler, helpHandler, reactionHandler, setNameHandler

def BuildApp() -> Application:
    from integration.YamlConfigService import YamlConfigService
    from interfaces.config_reader.ConfigEnum import ConfigEnum
    bot_token = YamlConfigService().get_service_api_key(ConfigEnum.TELEGRAM_TOKEN)

    app = ApplicationBuilder().token(bot_token).build()
    return app

if __name__ == '__main__':
    print('Starting bot...')
    app = BuildApp()
    
    print('Registering handlers...')
    app.add_handler(CommandHandler('registro', registroHandler))
    app.add_handler(CommandHandler('wish_list', getWishListHandler))
    app.add_handler(CommandHandler('set_name', setNameHandler))
    app.add_handler(CommandHandler('help', helpHandler))
    app.add_handler(MessageReactionHandler(reactionHandler))
    app.add_handler(MessageHandler(None, wishListReigisterHandler))

    print('Running bot...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)
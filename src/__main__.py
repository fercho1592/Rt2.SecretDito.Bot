from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Application, MessageReactionHandler, ConversationHandler
from dependency import build_container
from integration.container import Container
from interfaces.repo_protocols import ISecretDitoRepo
from interfaces.enums import ConfigEnum
from interfaces.config_protocols import ConfigServiceProtocol
from controllers.SecretDitoUserControllers import SecretDitoUserControllers
from controllers.SecretDitoUserConversationController import SecretDitoUserConversationController

def BuildApp(container: Container) -> Application:
    config_service: ConfigServiceProtocol = container.resolve(ConfigServiceProtocol)
    bot_token = config_service.get_service_api_key(ConfigEnum.TELEGRAM_TOKEN)

    app = ApplicationBuilder().token(bot_token).build()
    return app

if __name__ == '__main__':
    print('Starting bot...')
    container = build_container()
    app = BuildApp(container)
    user_controllers = SecretDitoUserControllers(container.resolve(ISecretDitoRepo))

    print('Registering handlers...')
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('registro', SecretDitoUserConversationController.entry_point)],
        states={
            SecretDitoUserConversationController.ConversationState.SET_NAME: [
                MessageHandler(None, SecretDitoUserConversationController.set_name_state)
            ],
        },
        fallbacks=[],
    ))
    app.add_handler(CommandHandler('wish_list', user_controllers.get_wish_list_handler))
    app.add_handler(CommandHandler('set_name', user_controllers.set_name_handler))
    app.add_handler(CommandHandler('help', user_controllers.help_handler))
    app.add_handler(CommandHandler('start', user_controllers.start_handler))
    app.add_handler(CommandHandler('secret_friend', user_controllers.get_secret_friend_handler))
    app.add_handler(CommandHandler('secret_wish_list', user_controllers.get_secret_friend_wish_list_handler))
    app.add_handler(MessageReactionHandler(user_controllers.delete_from_wish_list_by_reaction_handler))
    app.add_handler(MessageHandler(None, user_controllers.add_to_wish_list_handler))

    print('Running bot...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)

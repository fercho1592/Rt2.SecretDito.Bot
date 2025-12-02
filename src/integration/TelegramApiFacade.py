from telegram import Bot
from models.User import User
from interfaces.config_protocols import ConfigServiceProtocol
from interfaces.enums import ConfigEnum

class TelegramApiFacade:
    def __init__(self, config_service: ConfigServiceProtocol):
        self.BotToken = config_service.get_service_api_key(ConfigEnum.TELEGRAM_TOKEN)

    async def notify_user(self, user: User, message: str) -> None:
        bot = Bot(token=self.BotToken)
        if user.chat_id:
            await bot.send_message(chat_id=user.chat_id, text=message)
        else:
            print(f"Usuario {user.name} no tiene chat_id definido.")

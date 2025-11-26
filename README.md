# Rt2.SecretDito.Bot
Bot integration to manage SecretDito app from telegram or other chats services

## Installation

    pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r Requirements.txt

Also, you need to download a test driver for your browser, in this case it will be for Chrome. In case you want to use another browser you can change selenium implementation

## Configurations
The program use a file `config.ini` for all secrets and setups at root directory level

    [TelegramBot]
    token = telegram-token


## Virtual env
Action |CMD
-------|--------
Create env| `python3 -m venv .bot-venv`
Activate|`source ./.bot-venv/bin/activate`
Deactivate|`deactivate`

### Running

    py src
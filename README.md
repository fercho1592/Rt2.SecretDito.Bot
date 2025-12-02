# Rt2.SecretDito.Bot
Bot integration to manage SecretDito app from telegram or other chats services

## Virtual env
Action |CMD
-------|--------
Create env| `python3 -m venv .venv`
Activate|`source ./.venv/bin/activate`
Deactivate|`deactivate`

## Installation

    pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

Also, you need to download a test driver for your browser, in this case it will be for Chrome. In case you want to use another browser you can change selenium implementation

## Configurations
The program use a file `.env` for all secrets and setups at root directory level

    services:
        telegram_token: {Get token from BotFather}
        assignation_file: assignations.txt
        graph_settings_file: graph_settings.json

Also there is data/graph_setting.json file, that you can use to set some rules to asignation. The structure for this file is an aray with edge and values:

    [
        # invalid edge (value = -1)
        {"user_id": {telegram_id_user}, "to_user_id": {telegram_id_user}, "value": -1},
        # priority edge (value = 2 | +)
        {"user_id": {telegram_id_user}, "to_user_id": {telegram_id_user}, "value": 2},
    ]


### Running Commands

    # Runing main theat for bot
    python3 src

    # Run user assignation
    python3 ./src/run_assignation.py

    # Run user notification to fill their wish list
    python3 ./src/run_wish_list_empty_notification.py
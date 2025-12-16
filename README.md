# Rt2.SecretDito.Bot

Bot integration to manage SecretDito app from telegram or other chats services

## Virtual env

| Action     | CMD                           |
| ---------- | ----------------------------- |
| Create env | `python3 -m venv .venv`       |
| Activate   | `source ./.venv/bin/activate` |
| Deactivate | `deactivate`                  |

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

    # Running main thread for bot
    python3 src

    # Run user assignation
    python3 ./src/run_assignation.py

    # Run user notification to fill their wish list
    python3 ./src/run_wish_list_empty_notification.py

## Docker Usage

### Build Docker Image

    docker build -t secretdito-bot .

### Tagging Docker Images

To add a tag or version to your Docker image, use the -t option with your desired tag (e.g., v1.0.0):

    docker build -t secretdito-bot:1.0.0 .

To use a tagged image in docker-compose.yml, update the image field:

    image: secretdito-bot:1.0.0

### Using Docker Compose

1.  Create a .env file in the project root with your Telegram token:

        TELEGRAM_TOKEN=your_token_here

2.  Start the service:

        docker compose up

This will build the image (if needed), set the environment variable, and mount the ./data directory for persistent storage.

### Running Additional Scripts in a Running Container

To execute additional scripts (e.g., src/run_assignation.py) in a running container, use the following command:

    docker exec <container_name_or_id> python src/run_assignation.py

Replace <container_name_or_id> with the actual name or ID of your running container. You can find it with:

    docker ps

For example:

    docker exec secretdito-bot-1 python src/run_assignation.py

You can use this method to run any script inside the container, such as:

    docker exec <container_name_or_id> python src/run_wish_list_empty_notification.py

## Next Things to DO

1. Convert this project into a Docker image to be used without all Python installation steps
2. Check how to implement this project serverless mode (Azure Functions, Lambda functions)
3. Create others repository implementations to use others DBs (Mongo, Postgress, ...)
4. Add commando to ask your secret friend directly
5. Add implementation to use Whatsapp or other message services
6. Add function to use older results

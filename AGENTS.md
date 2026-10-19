# AGENTS.md

## Project overview
This repository is a Python Telegram bot for a SecretDito / Secret Santa workflow. It manages user registration, wish lists, secret friend assignment, and notification flows. The project is currently centered on Telegram, repository-backed persistence, and assignment generation using a graph-based algorithm.

## Primary technologies and runtime
- Language: Python 3
- Telegram integration: `python-telegram-bot`
- Config: YAML-based `.env` file in the project root
- Persistence: JSON files under `data/`
- Validation and linting: `pylint`

## Solution structure
- `src/__main__.py`: application bootstrap; registers Telegram command and message handlers.
- `src/dependency.py`: central dependency factory; resolves config, repositories, and API facade.
- `src/controllers/`: bot handlers that process Telegram updates.
- `src/models/`: domain objects such as `User`, `WishListItem`, and graph relationship helpers.
- `src/integration/`: concrete adapters for storage and external services (`SecretSantaRepo`, `YamlConfigService`, `TelegramApiFacade`).
- `src/interfaces/`: contracts for repositories and config access.
- `src/run_assignation.py`: generates the Secret Santa assignment using a weighted Hamiltonian-path approach.
- `src/run_user_notification.py`: sends notifications to users after assignment.
- `data/`: persisted user data, invalid edges configuration, and generated `assignations.txt` output.

## Architectural conventions
- Follow the existing layered structure: controllers -> dependency providers -> interfaces -> implementations.
- Keep external API logic inside `integration/` and service access behind interfaces.
- Repositories are accessed through `dependency.py` rather than directly from handlers.
- Domain data should be represented in model classes and serialized with `to_dict()` / `from_dict()` when saving to JSON.
- Telegram handlers are async and should use `await` for bot interactions.
- Keep command registration centralized in `src/__main__.py`.

## Coding style and naming
- Use Pythonic naming conventions:
  - Classes: `PascalCase`
  - Functions and methods: `snake_case`
  - Constants: uppercase snake case when appropriate
- Prefer explicit, readable code over clever abstractions.
- Keep methods concise and focused on one responsibility.
- Preserve the existing Spanish-language user messaging style unless the feature is intentionally bilingual.
- Use small, clear helper functions for validation and transformation logic.

## Common project rules
- Do not bypass the repository interfaces; prefer `dependency.py` and the existing abstraction layer.
- When adding a new bot command, register it in `src/__main__.py` and add the handler in the relevant controller file.
- User data lives under `data/*.json`; generated assignment files are saved in `data/assignations.txt`.
- Graph-based restrictions are represented in `graph_settings.json` and should be respected by assignment logic.
- The app uses YAML config under a root-level `.env` file with a `services` section; the expected key is `telegram_token`.
- Keep the code aligned with the current style of the repo: simple async handlers, concrete integrations, and thin controller logic.

## Build and run commands
Setup:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

Run:
- `python src`
- or `py src`

## Relevant references
- `README.md`
- `src/__main__.py`
- `src/dependency.py`
- `src/controllers/SecretDitoUserControllers.py`
- `src/controllers/SecretDitoUserConversationController.py`
- `src/integration/SecretSantaRepo.py`
- `src/run_assignation.py`

## Guidance for AI coding agents
When making changes, favor incremental edits that match the repo’s current structure and naming patterns. Preserve the project’s existing Spanish UX, dependency-injection flow, and repository-driven data access. If a change introduces new functionality, wire it into the same controller/repository pattern instead of creating a parallel architecture.

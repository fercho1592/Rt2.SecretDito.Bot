I’m turning your decision into a concrete feature list and separating the database migration from the new SQL Server implementation so the work stays manageable.

## SQL Server feature requirements

### Goal
Add a SQL Server-backed persistence layer to the bot so the current JSON file storage is replaced by a relational database while keeping the repository abstraction and the bot behavior intact.

This should fit the current structure around SecretSantaRepo.py, dependency.py, and the domain models in User.py.

---

## 1. Functional requirements

### 1.1 Data persistence
- The system must persist users in SQL Server.
- The system must persist each user’s wishlist items.
- The system must persist invalid assignment edges / restriction rules.
- The system must persist assignment results for each Secret Santa cycle.
- The system must support retrieving a user by Telegram user id.
- The system must support retrieving all registered users.
- The system must support updating an existing user record.
- The system must support creating a new user record.

### 1.2 Repository abstraction
- The current repository contract must remain behind the existing abstraction layer.
- The app must not directly access SQL Server from controllers.
- The repository implementation must be swappable without changing the bot business logic.
- The app must continue using the repository interface and dependency injection pattern.

### 1.3 User-related behavior
- A user must have a unique identifier, Telegram user id, username, chat id, and display name.
- A user can have zero or many wishlist items.
- A user can store a current assigned secret friend id.
- A user’s wishlist must be retrievable in the same format required by the bot flow.

### 1.4 Assignment logic support
- The backend must support the existing graph-based assignment validation logic.
- Restriction rules must be read from SQL tables and used by assignment generation.
- Generated assignments must be stored with enough metadata for audit and review.

### 1.5 Configuration
- SQL Server connection settings must be stored in environment configuration.
- The project must support local development and Docker-based deployment.
- Database credentials and server name must be configurable instead of hardcoded.

### 1.6 Error handling
- The app must handle database connection failures gracefully.
- Repository operations must fail clearly and log useful diagnostics.
- Missing user or empty data should return valid empty/null responses instead of crashing the bot.
- Duplicate inserts must be rejected explicitly.

---

## 2. Non-functional requirements

### 2.1 Simplicity
- The implementation must keep the app easy to run for personal use.
- The database should not require a complex distributed setup.
- A single SQL Server instance is acceptable for this project.

### 2.2 Reliability
- Data must be durable and persist across container or service restarts.
- Transaction boundaries must be maintained when creating/updating a user with related wishlist data.
- Assignment writes must be atomic when they involve multiple records.

### 2.3 Maintainability
- Schema and migration scripts must be versioned and documented.
- Database access logic should stay within the integration layer.
- The application should be easy to change from SQL Server to another relational database later if needed.

### 2.4 Performance
- The database must support the expected small personal workload without issues.
- Query patterns should be efficient for:
  - get user by id
  - get all users
  - get invalid edges
  - get assignment records

---

## 3. Data model requirements

### Main entities
- User
- WishlistItem
- SecretSantaEvent or AssignmentCycle
- UserAssignment
- InvalidEdgeRule

### Minimum fields
- Users:
  - id
  - telegram_user_id
  - username
  - name
  - chat_id
  - created_at
  - updated_at
- Wishlist items:
  - id
  - user_id
  - item_text
  - message_ids (optional)
  - created_at
- Invalid edges:
  - id
  - from_user_id
  - to_user_id
  - value
  - created_at
- Assignment cycle:
  - id
  - created_at
  - status
- Assignment record:
  - id
  - cycle_id
  - from_user_id
  - to_user_id

### Constraints
- One Telegram user must map to one persisted user record.
- A user can have multiple wishlist items.
- Invalid edges must be unique per pair and value.
- Assignment records should not allow a user to be assigned to themselves unless explicitly permitted.

---

## 4. Docker / environment requirements

- The project must support SQL Server in Docker Compose.
- The database should persist data through a named volume.
- Local development must allow environment-based configuration.
- The app must be able to start without manual DB schema creation if initialization is automated.

---

## 5. Acceptance criteria

- The bot can create and retrieve users from SQL Server.
- The bot can save and load wishlists correctly.
- The bot can load invalid edge rules from SQL Server.
- The bot can save assignment results to SQL Server.
- The repository abstraction remains unchanged for the controllers.
- The app starts successfully with SQL Server configured in environment variables.
- Data persists across container restarts.

---

## 6. Additional task: migration from current JSON storage

This should be treated as a separate follow-up task, not part of the initial feature delivery.

### Migration requirements
- Read all existing records from the current data folder.
- Import user JSON files into the new SQL Server tables.
- Import invalid edge rules from graph_settings.json.
- Map the current file-based structure into the relational schema.
- Validate duplicates, missing fields, and malformed entries.
- Preserve historical assignment outputs if relevant.
- Provide a migration script or one-time run step.
- Provide a verification report showing:
  - total users migrated
  - total wishlist items migrated
  - total invalid edges migrated
  - total assignment records migrated

### Migration safeguards
- Backup current data before running migration.
- Run in a dry-run mode first.
- Log every skipped or failed record.
- Support rollback if needed.

---

## Recommended final direction

For your profile, SQL Server is a good fit because it matches your experience and the project data is naturally relational. I would implement the SQL Server version first, then do the migration from the existing JSON files as a separate task.

If you want, I can next turn this into:
1. a real backlog with epics and tasks,
2. a database schema for SQL Server,
3. or a migration plan from the current JSON data folder to SQL tables.
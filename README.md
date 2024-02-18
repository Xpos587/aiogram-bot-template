# Aiogram Template

## Deployment

1. Setup [poetry](https://pypi.org/project/poetry/) and install requirements (`poetry install`)
2. Rename `.env.dist` to `.env` and configure it
3. Run database migrations with `make migrate` command
4. Before running the bot (`make run`), make sure you are in a virtual environment by running the command `poetry shell`.
5. Optional: configure `telegram-bot.service` ([» Read more](https://gist.github.com/comhad/de830d6d1b7ae1f165b925492e79eac8))

## Development

### Update database tables structure

**Make migration script:**

    make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES

**Run migrations:**

    make migrate

### Update translations

1. Parse new used localization keys to update translations files
   (`make i18n locale=TRANSLATION_LOCALE`)
2. Write new translations in `.ftl` files by `lang/TRANSLATION_LOCALE`
3. Restart the bot

## Used technologies

- [Aiogram 3.x](https://docs.aiogram.dev/en/dev-3.x/) (framework for creating Telegram bots)
- [Docker](https://www.docker.com/) (developing applications in containers)
- [Docker Compose](https://docs.docker.com/compose/) (tool for defining and running multi-tier applications)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (in-memory data storage for FSM and caching)
- [Project Fluent](https://projectfluent.org/) (modern localization system)

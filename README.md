### Run commands:
```shell

uv init
uv add fastapi --extra standard
uv add pwdlib --extra argon2
uv add pyjwt --extra crypto
uv add python-dotenv
uv add sqlalchemy --extra asyncio
uv add aiosqlite
uv add asyncpg
uv add alembic
uv add --dev ruff
uvx pyrefly init

uvx pyrefly check --summarize-errors
uv remove
uv lock
uv sync

uv run fastapi dev
uv build
uv sync --upgrade

uv lock --upgrade
uv sync

uvx ruff check
uvx ruff format
```

### Run with
```shell

uv run fastapi dev app/app.py 
```

or
```shell

uv run main.py 
```

### Docker

To start the PostgreSQL in Docker
```shell

docker compose up -d
```


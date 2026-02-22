from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

@dataclass
class Avito:
    client_id: str
    client_secret: str

@dataclass
class Api:
    base_url: str
    webhook_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    api: Api
    avito: Avito


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_id=list(map(int, env.list("ADMIN_ID")))
        ),
        db=DbConfig(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_NAME"),
        ),
        api=Api(base_url=env.str("API_URL"),
                webhook_token=env.str("WEBHOOK_TOKEN")
                ),
        avito=Avito(
            client_secret=env.str("eK8NDY6FLDWY5Ylatk-s7SCr7LEqCdsMSLT5oOMi"),
            client_id=env.str("AVITO_CLIENT_ID"),
        )

    )



from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


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
class Api:
    base_url: str
    webhook_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    api: Api


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=DbConfig(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_NAME"),
        ),
        yookassa=YooKassa(
            account_id=int(env.str("ACCOUNT_ID")),
            secret_key=env.str("SECRET_KEY")
        ),
        api=Api(base_url=env.str("API_URL"),
                webhook_token=env.str("WEBHOOK_TOKEN")
                )
    )

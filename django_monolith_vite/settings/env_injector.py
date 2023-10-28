from dotenv import load_dotenv


def update_configs_from_env() -> None:
    load_dotenv("dev.env")


def update_configs_from_vault(for_env) -> None:
    pass

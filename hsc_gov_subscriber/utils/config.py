import os
from configparser import ConfigParser
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.resolve()

config_file = os.path.join(PROJECT_PATH, "config.ini")


class ConfigUnit:
    def __init__(self, section, name, value=None, default_value=None, description=None):
        self._section = section
        self._name = name
        self._value = value
        self._default_value = default_value
        self._description = description

    @property
    def section(self):
        return self._section

    @property
    def name(self):
        return self._name

    @property
    def default_value(self):
        return self._default_value

    @property
    def description(self):
        return self._description

    @property
    def value(self):
        return Config.get_raw(self.section, self.name)

    def set_value(self, val):
        self._value = val


class Config:
    _config = ConfigParser()
    _config.read(config_file)

    @classmethod
    def set(cls, section, key, value):
        cls._config.set(section, key, value)
        for var in vars(cls).values():
            if (
                    isinstance(var, ConfigUnit)
                    and var.section == section
                    and var.name == key
            ):
                var.set_value(value)

    @classmethod
    def get_raw(cls, section, key):
        return cls._config.get(section, key)

    @classmethod
    def get_units(cls):
        return [v for v in vars(cls).values() if isinstance(v, ConfigUnit)]

    @staticmethod
    def save():
        with open(config_file, "w") as f:
            Config._config.write(f)

    EMAIL = ConfigUnit(
        "application",
        "email",
        description="Пошта на яку прийде білет та нагадування.",
    )
    OFFICE_ID = ConfigUnit(
        "application",
        "office_id",
        default_value=71,
        description="ID офісу ГСЦ. (71 - ГСЦ м. Миколаїв, пров. Транспортний, 1а/1).",
    )
    QUESTION_ID = ConfigUnit(
        "application",
        "question_id",
        default_value=56,
        description="ID послуги. (56 - практичний іспит (транспортний засіб навчального закладу))",
    )

    API_ID = ConfigUnit(
        "telethon",
        "api_id",
        description="App api_id з my.telegram.org"
    )

    API_HASH = ConfigUnit(
        "telethon",
        "api_hash",
        description="App api_hash з my.telegram.org"
    )

    START_DATE = ConfigUnit(
        "date",
        "start_date",
        description="дата з якої потрібно брати талон. (наприклад 2024-05-9 - якщо буде талон на 08.5.2024 - код не візьме такий талон, якщо прийде 09.5.2024 - код намагатиметься взяти талон)"
    )

    END_DATE = ConfigUnit(
        "date",
        "end_date",
        description="дата з якої вже не потрібно брати талон. (наприклад 2024-05-14 - якщо буде талон на 15.5.2024 - код не візьме такий талон, якщо прийде 14.5.2024 або 13.5.2024 - код намагатиметься взяти талон)"
    )

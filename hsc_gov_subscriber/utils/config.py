import os
import re
from configparser import ConfigParser
from datetime import datetime
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
        description="ID офісу ГСЦ. (71 - ГСЦ м. Миколаїв, пров. Транспортний, 1а/1).",
    )
    QUESTION_ID = ConfigUnit(
        "application",
        "question_id",
        description="ID послуги. (56 - практичний іспит (транспортний засіб навчального закладу), 49 - Перереєстрація транспортного засобу)",
    )
    VIN = ConfigUnit(
        "application",
        "vin",
        description="Номерний знак(AA1488BB) або VIN(останні 6 цифр)",
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


class ConfigException(Exception):
    pass


class ConfigValidation:
    VIN_PATTERN = r'([A-Za-z]{2}\d{4}[A-Za-z]{2})|(\d{6})'

    @staticmethod
    def _raise_config_exception(unit, message=None):
        raise ConfigException(
            f"Invalid value '{unit.value}' under section '{unit.section}.{unit.name}' in the config file.\n" + message)

    @staticmethod
    def _validate_date_range(unit_start_date, unit_end_date):
        start_date = datetime.strptime(unit_start_date.value, "%Y-%m-%d")
        end_date = datetime.strptime(unit_end_date.value, "%Y-%m-%d")
        if not start_date <= end_date:
            ConfigValidation._raise_config_exception(unit_start_date,
                                                     f"Check {unit_start_date.section}.{unit_start_date.name}, {unit_end_date.section}.{unit_end_date.name}. "
                                                     f"{unit_start_date.section}.{unit_start_date.name} must be less then {unit_end_date.section}.{unit_end_date.name}")

    @staticmethod
    def _check_not_none(unit: ConfigUnit):
        value = unit.value
        if (value is None
                or not value):
            ConfigValidation._raise_config_exception(unit, "Must be filled.")

    @classmethod
    def validate(cls):
        cls._validate_email()
        cls._validate_office_id()
        cls._validate_question_id()
        cls._validate_vin()

        cls._validate_api_id()
        cls._validate_api_hash()

        cls._validate_start_date()
        cls._validate_end_date()

    @staticmethod
    def _validate_email():
        ConfigValidation._check_not_none(Config.EMAIL)

    @staticmethod
    def _validate_office_id():
        ConfigValidation._check_not_none(Config.OFFICE_ID)

    @staticmethod
    def _validate_question_id():
        unit = Config.QUESTION_ID
        ConfigValidation._check_not_none(unit)
        if int(unit.value) not in (56, 49):
            ConfigValidation._raise_config_exception(unit, unit.description)

    @staticmethod
    def _validate_vin():
        if int(Config.QUESTION_ID.value) == 49:
            unit = Config.VIN
            ConfigValidation._check_not_none(unit)
            if not re.search(ConfigValidation.VIN_PATTERN, unit.value):
                ConfigValidation._raise_config_exception(unit, unit.description)

    @staticmethod
    def _validate_api_id():
        ConfigValidation._check_not_none(Config.API_ID)

    @staticmethod
    def _validate_api_hash():
        ConfigValidation._check_not_none(Config.API_HASH)

    @staticmethod
    def _validate_start_date():
        ConfigValidation._check_not_none(Config.START_DATE)
        ConfigValidation._validate_date_range(Config.START_DATE, Config.END_DATE)

    @staticmethod
    def _validate_end_date():
        ConfigValidation._check_not_none(Config.END_DATE)
        ConfigValidation._validate_date_range(Config.START_DATE, Config.END_DATE)

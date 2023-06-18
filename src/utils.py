"""
Вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
from pathlib import Path


def read_players(players_path: Path | str) -> dict[str, dict[str, int]]:
    config = ConfigParser()
    config.read(players_path)
    config = {
        player_name: {
            key: int(value)
            for key, value in config[player_name].items()
        }
        for player_name in config.sections()
    }
    return config


"""
Вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
# проект
import data


def read_players() -> bool:
    """Читает файл данных игроков, сохраняет информацию в соответствующую глобальную структуру данных. Возвращает True, если в файле данных игроков есть хотя бы одна запись, иначе False."""
    config = ConfigParser()
    config.read(data.PLAYERS_PATH)
    data.players_db = {
        player_name: {
            key: int(value)
            for key, value in config[player_name].items()
        }
        for player_name in config.sections()
    }
    return bool(config)


def read_saves() -> None:
    """"""
    saves = data.SAVES_PATH.read_text(encoding='utf-8').split('\n')
    for save in saves:
        players, turns, dim = save.split('!')
        data.saves_db |= {
            tuple(players.split(',')): {
                'dim': int(dim),
                'turns': {
                    int(turn): data.TOKENS[i%2]
                    for i, turn in enumerate(turns.split(','))
                },
            }
        }


def write_players() -> None:
    """Записывает в файл данных игроков информацию из соответствующей глобальной структуры данных."""


def write_saves() -> None:
    """"""


def dim_input() -> int:
    while True:
        dim = input(f' {data.MESSAGES["ввод размерности"]}{data.PROMPT}')
        if data.DIM_PATTERN.fullmatch(dim):
            return int(dim)
        print(f' {data.MESSAGES["некорректная размерность"]} ')


def change_dim(new_dim: int) -> None:
    """"""
    data.dim = new_dim
    data.dim_range = range(new_dim)
    data.all_cells = new_dim**2


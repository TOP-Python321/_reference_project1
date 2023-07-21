"""
Глобальные переменные и константы.
"""

# стандартная библиотека
from collections.abc import Callable
from pathlib import Path
from re import compile
from sys import argv


DEBUG = argv[1:] == ['debug']
debug_data = {}


PLAYERS_PATH = Path(r'..\data\players.ini')
SAVES_PATH = Path(r'..\data\saves.txt')

APP_TITLE = 'КРЕСТИКИ-НОЛИКИ'

COMMANDS = {
    'начать новую партию': ('new', 'n', 'начать', 'н'),
    'загрузить существующую партию': ('load', 'l', 'загрузка', 'з'),
    'отобразить раздел помощи': ('help', 'h', 'помощь', 'п'),
    'создать или переключиться на игрока': ('player', 'p', 'игрок', 'и'),
    'отобразить таблицу результатов': ('table', 't', 'таблица', 'т'),
    'изменить размер поля': ('dim', 'd', 'размер', 'р'),
    'выйти': ('quit', 'q', 'выход', 'в'),
}


NAME_PATTERN = compile(r'[A-Za-zА-ЯЁа-яё][A-Za-zА-ЯЁа-яё\d_]+')
DIM_PATTERN = compile(r'[3-9]|1[0-9]|20')


players_db: dict[str, dict[str, int]] = {}
saves_db: dict[tuple[str, str], dict] = {}


dim: int = None
dim_range: range = None
all_cells: int = None
all_cells_range: range = None

wins: list[set[int]] = []

TOKENS = ('X', 'O')

WEIGHT_OWN = 1.5
WEIGHT_FOE = 1.0

START_MATRICES = ()

authorized: str
players: list[str] = []
bot_level: Callable = None

field: str = None
field_with_coords: str = None

board: dict[int, str] = {}
turns: dict[int, str] = {}


MESSAGES = {
    'ввод команды': '\n _ введите команду > ',

    'ввод имени': '\n _ введите имя игрока > ',
    'некорректное имя': ' ! имя игрока должно начинаться с буквы, содержать только буквы, цифры и символ подчёркивания',

    'ввод размерности': ' _ введите новый размер поля > ',
    'некорректная размерность': ' ! размер поля должен находиться в диапазоне от 3 до 20',

    'ввод режима': '\n _ выберите режим игры\n    1 - один человек\n    2 - два человека\n > ',
    'ввод уровня': '\n _ выберите уровень сложности\n    1 - низкий (бот делает случайные ходы)\n    2 - высокий (бот стремится выиграть)\n > ',
    'ввод токена': '\n _ выберите токен, которым хотите играть\n    1 - крестик\n    2 - нолик\n > ',
    'некорректный выбор': ' ! введите цифру 1 или 2',

    'ввод сохранения': '\n _ выберите сохранение\n{}',
    'некорректное сохранение': ' ! введите число от 1 до {}',
    'нет сохранений': ' ! у вас нет ни одного сохранения',

    'ввод хода': '\n _ введите номер свободной ячейки > ',
    'ход не число': ' ! номер ячейки должен быть числом',
    'ход не в диапазоне': f' ! номер ячейки должен находиться в диапазоне от 1 до {all_cells} включительно',
    'ход в занятую': ' ! ячейка занята',

    'победитель': 'побеждает игрок {}',
    'ничья': 'ничья',

    # '': '',
}

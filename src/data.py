"""
Глобальные переменные и константы.
"""

# стандартная библиотека
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


dim: int = 3
dim_range = range(dim)
all_cells: int = dim**2

authorized: str

TOKENS = ('X', 'O')
WEIGHT_OWN = 1.5
WEIGHT_FOE = 1.0
START_MATRICES = ()

players: list[str] = []

board: dict[int, str] = dict.fromkeys(range(1, all_cells+1), ' ')
turns: dict[int, str] = {}

field: str = ''


MESSAGES = {
    'ввод команды': '\n _ введите команду > ',
    'ввод имени': '\n _ введите имя игрока: ',
    'некорректное имя': ' ! имя игрока должно начинаться с буквы, содержать только буквы, цифры и символ подчёркивания',
    'ввод размерности': '\n _ введите новый размер поля: ',
    'некорректная размерность': ' ! размер поля должен находиться в диапазоне от 3 до 20',
    'ввод хода': '\n _ введите номер свободной ячейки: ',
    'ход не число': ' ! номер ячейки должен быть числом',
    'ход не в диапазоне': f' ! номер ячейки должен находиться в диапазоне от 0 до {all_cells-1} включительно',
    'ход в занятую': ' ! ячейка занята',
    # '': '',
}

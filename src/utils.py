"""
Вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
from shutil import get_terminal_size
from typing import Literal
# проект
import bot
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
    """Читает файл данных сохранений, сохраняет информацию в соответствующую глобальную структуру данных."""
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
    config = ConfigParser()
    config.read_dict(data.players_db)
    with open(data.PLAYERS_PATH, 'w', encoding='utf-8') as fileout:
        config.write(fileout)


def write_saves() -> None:
    """Записывает в файл данных сохранений информацию из соответствующей глобальной структуры данных."""
    saves = '\n'.join(
        f"{','.join(players)}!{','.join(map(str, save['turns']))}!{save['dim']}"
        for players, save in data.saves_db.items()
    )
    data.SAVES_PATH.write_text(saves, encoding='utf-8')


def dim_input() -> int:
    while True:
        dim = input(data.MESSAGES["ввод размерности"])
        if data.DIM_PATTERN.fullmatch(dim):
            return int(dim)
        print(data.MESSAGES["некорректная размерность"])


def change_dim(new_dim: int) -> None:
    """"""
    data.dim = new_dim
    data.dim_range = range(new_dim)
    data.all_cells = new_dim**2
    data.board = dict.fromkeys(range(1, data.all_cells+1), ' ')
    data.MESSAGES['ход не в диапазоне'] = f' ! номер ячейки должен находиться в диапазоне от 1 до {data.all_cells} включительно'
    data.field = field_template()


def field_template(data_width: int = None) -> str:
    """"""
    if data_width is None:
        field_width = data.dim*(3 + max(len(t) for t in data.TOKENS)) - 1
    else:
        field_width = data.dim*(3 + data_width) - 1
    v_sep, h_sep = '|', '—'
    v_sep = v_sep.join([' {} ']*data.dim)
    h_sep = f'\n{h_sep*field_width}\n'
    return h_sep.join([v_sep]*data.dim)


def concatenate_rows(
        multiline1: str,
        multiline2: str,
        *multilines: str,
        padding: int = 8
) -> str:
    """"""
    multilines = multiline1, multiline2, *multilines
    multilines = [m.split('\n') for m in multilines]
    padding = ' '*padding
    return '\n'.join(
        padding.join(row)
        for row in zip(*multilines)
    )


def header_text(
        text: str,
        *,
        level: Literal[1, 2],
        v_fill: str = '#',
        h_fill: str = '='
) -> str:
    """Возвращает переданную строку, форматированную как заголовок. Форматирование отличается для разных уровней заголовка. Также могут быть изменены символы-заполнители."""
    term_width = get_terminal_size()[0] - 1
    data_width = term_width - 12
    text_len = len(text)

    if level == 1:
        text = text.upper()
        edge = v_fill + h_fill*(term_width-2) + v_fill
        padding = v_fill + ' '*(term_width-2) + v_fill
        text = '\n'.join(
            v_fill + line.center(term_width - 2) + v_fill
            for line in columnize(text, term_width - 6)
        )
        return f'{edge}\n{padding}\n{text}\n{padding}\n{edge}'

    elif level == 2:
        text = text.upper()
        if text_len <= data_width:
            return f'  {text}  '.center(term_width, h_fill)
        else:
            return '\n'.join(
                h_fill*4 + line.center(data_width + 4) + h_fill*4
                for line in columnize(text, data_width)
            )

    # elif level == 3:
    #     ...

    else:
        raise ValueError


def columnize(text: str, column_width: int) -> list[str]:
    """Разбивает переданную строку на отдельные слова и формирует из слов строки, длины которых не превышают заданное значение. Возвращает список строк, к которым впоследствии может быть применено любое выравнивание."""
    multiline, line_len, i = [[]], 0, 0
    for word in text.split():
        word_len = len(word)
        if line_len + word_len + len(multiline[i]) <= column_width:
            multiline[i] += [word]
            line_len += word_len
        else:
            multiline += [[word]]
            line_len = word_len
            i += 1
    return [' '.join(line) for line in multiline]



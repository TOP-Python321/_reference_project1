"""
Настройка партии и игровой процесс.
"""

# стандартная библиотека
from shutil import get_terminal_size
# проект
import bot
import data
import utils


def get_human_turn() -> int | None:
    """Запрашивает пользовательский ввод для хода во время игрового процесса. При некорректном вводе повторяет запрос до получения корректного ввода."""
    while True:
        turn = input(data.MESSAGES['ввод хода'])
        if not turn:
            return None
        try:
            turn = int(turn)
        except ValueError:
            print(data.MESSAGES['ход не число'])
        else:
            if 1 <= turn <= data.all_cells:
                if turn not in data.turns:
                    return turn
                else:
                    print(data.MESSAGES['ход в занятую'])
            else:
                print(data.MESSAGES['ход не в диапазоне'])


def get_bot_turn() -> int:
    """"""


def game() -> list[str] | None:
    """Контроллер игрового процесса."""
    data.field = utils.field_template()
    data.START_MATRICES = (
        bot.calc_sm_cross(),
        bot.calc_sm_zero()
    )
    # 9. Цикл до максимального количества ходов
    for t in range(len(data.turns), data.all_cells):
        o = t % 2

        ...

        if data.players[o].startswith('#'):
            # 10. Расчёт хода бота
            turn = get_bot_turn()
        else:
            # 10. Запрос хода игрока
            turn = get_human_turn()
        # а) ЕСЛИ ввод пустой:
        if turn is None:
            # сохранение незавершённой партии
            save()
            # переход к этапу 4
            return None

        # 11. Обновление глобальных переменных (опционально: выполнение автосохранения и обновление файлов данных)
        ...

        # 12. Вывод игрового поля со сделанным ходом
        # noinspection PyTypeChecker
        print_board(o)

        # 13. ЕСЛИ есть победная комбинация:
        #          переход к этапу 14
        #     ЕСЛИ нет победной комбинации:
        #           переход к этапу 9
        ...

        # победа и поражение
        clear()
        return data.players
    else:
        # ничья
        clear()
        return []


def load(players: tuple[str, str], save: dict) -> None:
    """"""
    data.players = list(players)
    data.turns = save['turns']
    utils.change_dim(save['dim'])


def save() -> None:
    """"""
    data.saves_db |= {
        tuple(data.players): {
            'dim': data.dim,
            'turns': data.turns
        }
    }


def print_board(right: bool = False) -> None:
    """"""
    board = data.field.format(*(data.board | data.turns).values())
    if data.DEBUG:
        matr = bot.vectorization(data.debug_data.get('result'))
        cw = max(len(str(n)) for n in matr)
        matr = utils.field_template(cw).format(*matr)
        board = utils.concatenate_rows(board, matr)

    if right:
        terminal_width = get_terminal_size()[0] - 1
        margin = terminal_width - max(len(line) for line in board.split())
        margin = '\n'.join(' '*margin for _ in board.split())
        board = utils.concatenate_rows(margin, board)

    print(board)


def clear() -> None:
    """"""
    # noinspection PyTypeChecker
    data.saves_db.pop(tuple(data.players), None)
    data.players = [data.authorized]
    data.turns = {}


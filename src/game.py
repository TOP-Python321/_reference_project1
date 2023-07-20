"""
Настройка партии и игровой процесс.
"""

# стандартная библиотека
from shutil import get_terminal_size
# проект
import bot
import data
import player
import utils


def mode() -> None:
    """"""
    match player.ask_player('ввод режима'):
        case '1':
            match player.ask_player('ввод уровня'):
                case '1':
                    data.players += ['#1']
                    data.bot_level = bot.easy_mode
                case '2':
                    data.players += ['#2']
                    data.bot_level = bot.hard_mode
        case '2':
            player.get_player_name()
    match player.ask_player('ввод токена'):
        case '2':
            data.players.reverse()
    data.field = utils.field_template()


def game() -> list[str] | None:
    """Контроллер игрового процесса."""
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
            turn = data.bot_level()
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


def load() -> bool:
    """"""
    save = player.ask_for_load()
    if not save:
        print(data.MESSAGES['нет сохранений'])
        return False
    players, save = save
    data.players = list(players)
    utils.change_dim(save['dim'])

    o = len(save['turns']) % 2
    last_turn = save['turns'].popitem()
    data.turns = save['turns']
    print_board(o)
    save['turns'] |= (last_turn,)
    data.turns = save['turns']
    print_board(o-1)
    return True


def save() -> None:
    """"""
    data.saves_db |= {
        tuple(data.players): {
            'dim': data.dim,
            'turns': data.turns
        }
    }
    utils.write_saves()


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
    data.bot_level = None
    data.turns = {}


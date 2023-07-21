"""
Настройка партии и игровой процесс.
"""

# стандартная библиотека
from itertools import islice
from shutil import get_terminal_size
from time import sleep

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
            player.get_player_name(False)
    match player.ask_player('ввод токена'):
        case '2':
            data.players.reverse()


def game() -> list[str] | None:
    """Контроллер игрового процесса."""
    # 9. Цикл до максимального количества ходов
    for t in range(len(data.turns), data.all_cells):
        # индекс-указатель на игрока и токен
        pointer = t % 2
        if data.players[pointer].startswith('#'):
            # 10. Расчёт хода бота
            turn = data.bot_level(pointer)
            sleep(0.5)
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
        data.turns |= {turn: data.TOKENS[pointer]}
        # 12. Вывод игрового поля со сделанным ходом
        print_board(pointer)

        # 13. ЕСЛИ есть победная комбинация:
        #          переход к этапу 14
        if is_wins(pointer):
            winner = data.MESSAGES['победитель'].format(data.players[pointer])
            print('\n', utils.header_text(winner, level=2), sep='')
            return data.players
        # ЕСЛИ нет победной комбинации:
        #      переход к этапу 9
    else:
        # ничья
        print('\n', utils.header_text(data.MESSAGES['ничья'], level=2), sep='')
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

    parity = len(save['turns']) % 2
    last_turn = save['turns'].popitem()
    data.turns = save['turns']
    print_board(parity)
    save['turns'] |= (last_turn,)
    data.turns = save['turns']
    print_board(parity - 1)
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


def print_board(right: int = False) -> None:
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
        board = utils.concatenate_rows(margin, board, padding=0)

    print(board)


def is_wins(token_index: int) -> bool:
    """"""
    turns = set(islice(data.turns, token_index, None, 2))
    for comb in data.wins:
        if comb <= turns:
            return True
    else:
        return False


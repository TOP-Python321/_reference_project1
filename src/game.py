"""
Настройка партии и игровой процесс.
"""

# проект
import data
import utils


def get_human_turn() -> int | None:
    """Запрашивает пользовательский ввод для хода во время игрового процесса. При некорректном вводе повторяет запрос до получения корректного ввода."""
    while True:
        turn = input(data.PROMPT)
        if not turn:
            return None
        try:
            turn = int(turn)
        except ValueError:
            pass
        else:
            if 0 <= turn < data.all_cells:
                if turn not in data.turns:
                    return turn


def get_bot_turn() -> int:
    """"""


def game() -> list[str] | None:
    """Контроллер игрового процесса."""
    data.field = utils.field_template()
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


def clear() -> None:
    """"""
    # noinspection PyTypeChecker
    data.saves_db.pop(tuple(data.players), None)
    data.players = [data.authorized]
    data.turns = {}


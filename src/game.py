"""
Настройка партии и игровой процесс.
"""

# проект
import data


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


def game() -> list[str] | None:
    """Контроллер игрового процесса."""
    # 9. Цикл до максимального количества ходов
    for t in range(len(data.turns), data.all_cells):
        o = t % 2

        ...

        # 10. Запрос хода игрока
        turn = get_human_turn()
        # а) ЕСЛИ ввод пустой:
        if turn is None:
            # сохранение незавершённой партии
            ...
            # переход к этапу 4
            return None

        ...

    else:
        # ничья
        return []


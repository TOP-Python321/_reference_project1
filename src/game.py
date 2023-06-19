"""
Настройка партии и игровой процесс.
"""

import data


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

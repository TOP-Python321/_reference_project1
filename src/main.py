"""
Точка входа: управляющий код.
"""

# проект
import data
import game
import player
import utils


# 1. Чтение файлов данных
# 2. ЕСЛИ первый запуск:
if utils.read_players():
    # вывод титров
    ...

# 3. Запрос имени игрока
player.get_player_name()

# суперцикл
while True:
    # 4. Ожидание ввода команды
    command = input(data.PROMPT)

    if command in data.COMMANDS['начать новую партию']:
        # 5. Запрос режима игры:
        ...
        # партия
        result = game.game()
        # 14. Обновление статистики в базе игроков и обновление файлов данных
        if result is not None:
            player.update_stats(result)

    elif command in data.COMMANDS['загрузить существующую партию']:
        # game.load()
        result = game.game()
        # 14. Обновление статистики в базе игроков и обновление файлов данных
        if result is not None:
            player.update_stats(result)
            ...

    # elif ...

    elif command in data.COMMANDS['выйти']:
        break

    # 15. Переход к этапу 4


# 16. Обработка завершения работы приложения


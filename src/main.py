"""
Точка входа: управляющий код.
"""

# проект
import data
import game
import player
import utils


print(utils.header_text(data.APP_TITLE, level=1))

# 1. Чтение файлов данных
# 2. ЕСЛИ первый запуск:
if utils.read_players():
    # вывод титров
    ...
utils.read_saves()
utils.change_dim(3)

# 3. Запрос имени игрока
player.get_player_name()

# суперцикл
while True:
    # 4. Ожидание ввода команды
    command = input(data.MESSAGES['ввод команды'])

    if command in data.COMMANDS['начать новую партию']:
        # 5. Запрос режима игры:
        game.mode()
        # партия
        result = game.game()
        # 14. Обновление статистики в базе игроков и обновление файлов данных
        if result is not None:
            player.update_stats(result)
        utils.clear()

    elif command in data.COMMANDS['загрузить существующую партию']:
        # нумерованный вывод сохранений активного игрока и запрос конкретного сохранения
        ...
        if game.load():
            result = game.game()
            # 14. Обновление статистики в базе игроков и обновление файлов данных
            if result is not None:
                player.update_stats(result)
                utils.clear(del_save=True)
            else:
                utils.clear()

    elif command in data.COMMANDS['изменить размер поля']:
        utils.change_dim(utils.dim_input())

    elif command in data.COMMANDS['создать или переключиться на игрока']:
        player.get_player_name()

    # elif command in data.COMMANDS['']:

    elif command in data.COMMANDS['выйти']:
        break

    # 15. Переход к этапу 4


# 16. Обработка завершения работы приложения


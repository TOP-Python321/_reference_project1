"""
Точка входа: управляющий код.
"""

# проект
import data
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
        ...

    elif command in data.COMMANDS['загрузить существующую партию']:
        ...

    # elif ...

    elif command in data.COMMANDS['выйти']:
        break

# 16. Обработка завершения работы приложения


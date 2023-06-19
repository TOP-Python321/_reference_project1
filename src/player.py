"""
Работа с данными игроков.
"""

# проект
import data
import utils


def name_input() -> str:
    while True:
        name = input(f' {data.MESSAGES["ввод имени"]}{data.PROMPT}')
        if data.NAME_PATTERN.fullmatch(name):
            return name
        print(f' {data.MESSAGES["некорректное имя"]} ')


# 3. Запрос имени игрока
def get_player_name() -> None:
    """Выполняет авторизацию или регистрацию игрока."""
    name = name_input()
    # а) ЕСЛИ имени нет в базе игроков:
    if name not in data.players_db:
        # добавление записи об игроке в базу игроков
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        # обновление файлов данных
        utils.write_players()
        # вывод раздела помощи
        # help.full()
    # б) добавление имени игрока к списку активных игроков
    data.players += [name]


# 14. Обновление статистики в базе игроков и обновление файлов данных
def update_stats(result: list[str]) -> None:
    """Обновляет статистику активных игроков по результатам партии."""
    if result:
        winner, looser = result
        data.players_db[winner]['побед'] += 1
        data.players_db[looser]['поражений'] += 1
    else:
        for name in data.players:
            data.players_db[name]['ничьих'] += 1


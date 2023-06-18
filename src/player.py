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


def get_player_name() -> None:
    """"""
    name = name_input()
    if name not in data.players_db:
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        utils.write_players()
        # help.full()
    data.players += [name]


"""
Работа с данными игроков.
"""

# стандартная библиотека
from itertools import chain
# проект
import data
import utils


def name_input() -> str:
    while True:
        name = input(data.MESSAGES["ввод имени"])
        if data.NAME_PATTERN.fullmatch(name):
            return name
        print(data.MESSAGES["некорректное имя"])


# 3. Запрос имени игрока
def get_player_name(switch: bool = True) -> None:
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
    if switch:
        data.authorized = name
        data.players = [name]
    else:
        # б) добавление имени игрока к списку активных игроков
        data.players += [name]


def ask_player(question: str) -> str:
    """"""
    while True:
        choice = input(data.MESSAGES[question])
        if choice in '12':
            return choice
        print(data.MESSAGES['некорректный выбор'])


def ask_for_load() -> tuple[tuple[str, str], dict] | None:
    """"""
    slots = []
    for i, players in enumerate(data.saves_db, 1):
        if data.authorized in players:
            players = ', '.join(
                f'{t}: {p}'
                for t, p in zip(data.TOKENS, players)
            )
            slots += [f'    {i} - {players}']
    if not slots:
        return None
    print(data.MESSAGES['ввод сохранения'].format('\n'.join(slots)))
    while True:
        choice = input(' > ')
        try:
            choice = int(choice)
            return tuple(data.saves_db.items())[choice-1]
        except (ValueError, IndexError):
            print(data.MESSAGES['некорректное сохранение'].format(i))


# 14. Обновление статистики в базе игроков и обновление файлов данных
def update_stats(result: list[str]) -> None:
    """Обновляет статистику активных игроков по результатам партии."""
    if result:
        winner, looser = result
        try:
            data.players_db[winner]['побед'] += 1
        except KeyError:
            pass
        try:
            data.players_db[looser]['поражений'] += 1
        except KeyError:
            pass
    else:
        for name in data.players:
            try:
                data.players_db[name]['ничьих'] += 1
            except KeyError:
                pass
    utils.write_players()


def sort_stats() -> list[list]:
    """"""
    data.players_db = {
        player: stat
        for player, stat in sorted(
            data.players_db.items(),
            key=sorting_key,
            reverse=True
        )
    }
    return [
        ['', ''] + list(chain(*data.players_db.values()))[:3],
    ] + [
        [i, player] + list(data.players_db[player].values())
        for i, player in enumerate(data.players_db, 1)
    ]


def sorting_key(player_stat: tuple[str, dict]) -> tuple[int, int]:
    """"""
    _, stat = player_stat
    return stat['побед'], sum(stat.values())


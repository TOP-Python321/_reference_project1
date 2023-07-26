"""
Раздел помощи.
"""

# стандартная библиотека
from shutil import get_terminal_size
# проект
import data
import utils


RULES = 'Вы играете одним из двух символов: крестиком {token_0} или ноликом {token_1}. Чтобы победить, первым составьте последовательность из {dim} своих символов в одной строке, в одном столбце, либо в одной диагонали.'
INTERFACE = (
    'Игра предлагает вам интерфейс командной строки. Это означает, что для выполнения определённого действия в игре необходимо ввести команду и нажать Enter. В последнем разделе данной справки приведён список действий и соответствующих им команд, которые можно использовать в главном меню между партиями.',
    'Во время выполнения различных действий игра может запрашивать у вас дополнительные данные или задавать уточняющие вопросы. В таких случаях возможные варианты ввода перечисляются в скобках в конце строки с приглашением для ввода. Отсутствие перечисления вариантов ввода означает, что можно вводить любые данные: например, когда игра запрашивает имя игрока.',
    'Во время партии игра ожидает от игрока(-ов) ввода номера клетки для текущего хода. Нумерация клеток поля показана в примере ниже. Ввод пустой строки во время своего хода позволит вам сохранить незавершённую партию и вернуться в главное меню.'
)


def render_rules() -> str:
    """"""
    data_width = get_terminal_size()[0] - 1 - 4
    rules = RULES.format(
        token_0=repr(data.TOKENS[0]),
        token_1=repr(data.TOKENS[1]),
        dim=data.dim
    )
    rules = '\n'.join(
        f'  {line:<{data_width+2}}'
        for line in utils.columnize(rules, data_width)
    )
    return (f"\n"
            f"{utils.header_text('правила игры', level=2)}\n"
            f"\n"
            f"{rules}\n")


def render_numerated_filed(center: bool = True) -> str:
    """"""
    if data.field_with_coords is None:
        return ''
    field = data.field_with_coords
    if center:
        term_width = get_terminal_size()[0] - 1
        field = field.split('\n')
        margin = (term_width - len(field[0])) // 2
        margin = '\n'.join(' '*margin for _ in field)
        field = utils.concatenate_rows(margin, data.field_with_coords, padding=0)
    return f'\n{field}\n'


def render_interface() -> str:
    """"""
    data_width = get_terminal_size()[0] - 1 - 4
    interface = '\n\n'.join(
        '\n'.join(
            f'  {line:<{data_width + 2}}'
            for line in utils.columnize(paragraph, data_width)
        )
        for paragraph in INTERFACE
    )
    return (f"\n"
            f"{utils.header_text('интерфейс', level=2)}\n"
            f"\n"
            f"{interface}\n"
            f"{render_numerated_filed()}")


def render_commands(section: bool = True) -> str:
    """"""
    if section:
        commands = f'\n{utils.header_text("команды", level=2)}\n\n'
    else:
        commands = f"{data.MESSAGES['некорректная команда']}\n\n"
    widths = [max(len(option) for option in column) for column in zip(*data.COMMANDS.values())]
    for command, options in data.COMMANDS.items():
        options = ' : '.join(f'{o:<{widths[i]}}' for i, o in enumerate(options))
        commands += f'{command} : {options} :'.rjust(get_terminal_size()[0] - 1) + '\n'
    return commands


def render_all() -> str:
    """"""
    return f'{render_rules()}{render_interface()}{render_commands()}'


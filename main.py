""" Объектная модель сапёра.    """
from src.control_game.control import Control


def run_game(hard: str, mines: str):
	helper: list[str] = [
		'Возможные вводы:',
		'click y x — сделать ход в точку y x',
		'flag yx — поставить флаг на точку y x',
		'help — помощь',
		'end game — закончить игру'
	]
	mines = None if mines == '' else int(mines)
	control: Control | None = None
	if hard == '':
		control = Control()
	elif ', ' in hard:
		control = Control(tuple(map(int, hard.split(', '))), mines)
	else:
		control = Control(hard, mines)
	print('\n'.join(helper), control, sep='\n')
	while True:
		step: str = input('Введите действие: ')
		if step == '':
			print('Вы ничего не ввели.')
		elif step.split()[0] == 'click':
			print(
				control.click(
					tuple(map(lambda x: x - 1, map(int, step.split()[1:])))
				)
			)
		elif step.split()[0] == 'flag':
			print(
				control.touch_flag(
					tuple(map(lambda x: x - 1, map(int, step.split()[1:])))
				)
			)
		elif step == 'help':
			print(print('\n'.join(helper)))
		elif step == 'end game':
			control.end_game()
		else:
			print(
				'Действие неизвестно, чтобы просмотреть ' +\
				'возможные варианты действий, напишите "help".'
			)


if __name__ == '__main__':
	run_game(
		input(
			'Введите сложность игры (варианты: easy, medium, hard или же в формате: '
			'height, width): '
		),
		input('Введите количество мин: ')
	)

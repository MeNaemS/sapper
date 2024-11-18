from src.control_game.control import Control, create_controller


def run_game(mode: str, mines: str):
	helper: list[str] = [
		'Возможные вводы:',
		'click y x — сделать ход в точку y x',
		'flag yx — поставить флаг на точку y x',
		'help — помощь',
		'end game — закончить игру'
	]
	mines = None if mines == '' else int(mines)
	control: Control | None = None
	if mode == '':
		control = create_controller()
	elif ', ' in mode:
		control = create_controller(tuple(map(int, mode.split(', '))), mines)
	else:
		control = create_controller(mode, mines)
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

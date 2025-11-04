#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS, COMMANDS
from labyrinth_game.utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help
from labyrinth_game.player_actions import (
    show_inventory,
    get_input,
    move_player,
    take_item,
    use_item
)

"""
Обработчик команд пользователя
"""
def process_command(game_state, command, COMMANDS):
    if command in ['north', 'south', 'east', 'west']:
        move_player(game_state, command)
        return

    parts = command.split(' ', 1)
    action = parts[0]

    # Доступные команды и их выполнение
    match action:
        case 'quit':
            game_state['game_over'] = True
            print("Спасибо за игру!")
            return

        case 'look':
            describe_current_room(game_state)
            return

        case 'inventory':
            show_inventory(game_state)
            return

        case 'help':
            show_help(COMMANDS)
            return

        case 'steps':
            print(f"Вы прошли шагов: {game_state['steps_taken']}")
            return

        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
                if game_state['current_room'] == 'treasure_room':
                    attempt_open_treasure(game_state)
            return

        case 'go' | 'take' | 'use':
            if len(parts) < 2:
                print("Команда требует аргумент. Пример: go north, take torch")
                return

            arg = parts[1]

            if action == 'go':
                move_player(game_state, arg)
            elif action == 'take':
                take_item(game_state, arg)
            elif action == 'use':
                use_item(game_state, arg)
            return

        case _:
            print("Неизвестная команда. Введите 'help', чтобы посмотреть список команд.")


def main():
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command, COMMANDS)

    print("Игра окончена.")


if __name__ == "__main__":
    main()
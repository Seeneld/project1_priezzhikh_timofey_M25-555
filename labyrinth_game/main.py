#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import show_inventory, get_input


game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }
  

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input()

        if command == "quit":
            print("Спасибо за игру!")
            break
        elif command == "look":
            describe_current_room(game_state)
        elif command == "inventory":
            show_inventory(game_state)
        else:
            print("Неизвестная команда. Доступные команды: look, inventory, quit.")

    print("Игра окончена.")

if __name__ == "__main__":
    main()
              
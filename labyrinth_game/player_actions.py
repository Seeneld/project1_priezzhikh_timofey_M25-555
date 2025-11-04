"""
Показ инвентаря игрового персонажа
"""
def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


"""
Получение ввода игрока
"""
def get_input(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

"""
Перемещение игрового персонажа
"""
def move_player(game_state, direction):
    from labyrinth_game.constants import ROOMS
    from labyrinth_game.utils import describe_current_room

    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if direction in room_data['exits']:
        next_room = room_data['exits'][direction]

        # Проверка на treasure_room
        if next_room == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print("Вы используете найденный ключ, " \
                "чтобы открыть путь в комнату сокровищ.")
                game_state['current_room'] = next_room
                game_state['steps_taken'] += 1
                describe_current_room(game_state)
                
                from labyrinth_game.utils import random_event
                random_event(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            game_state['current_room'] = next_room
            game_state['steps_taken'] += 1
            print(f"Вы идете на {direction}.")
            describe_current_room(game_state)
            
            from labyrinth_game.utils import random_event
            random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


"""
Подбор предмета игровым персонажем
"""
def take_item(game_state, item_name):
    from labyrinth_game.constants import ROOMS

    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_data['items']:
        room_data['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

"""
Использование предмета игровым персонажем
"""
def use_item(game_state, item_name):

    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Свет стал ярче, и вы видите больше деталей.")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность и готовность к приключениям.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            print("Вы открыли бронзовую шкатулку и нашли ржавый ключ!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
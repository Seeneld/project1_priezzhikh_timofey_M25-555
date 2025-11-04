import math

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

"""
Вывод описания текущеей комнаты
"""
def describe_current_room(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))
    else:
        print("Заметные предметы: нет")

    exits = room['exits']
    if exits:
        directions = ", ".join(exits.keys())
        print(f"Выходы: {directions}")
    else:
        print("Выходы: нет")

    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка"
        " (используйте команду solve).")
    print()


"""
Механика загадок
"""
def solve_puzzle(game_state):
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room['puzzle']
    print("Загадка:", question)
    user_answer = get_input("Ваш ответ: ").strip().lower()

    correct_variants = [correct_answer.lower()]
    if correct_answer == '10':
        correct_variants.append('десять')
    elif correct_answer == 'десять':
        correct_variants.append('10')

    if user_answer in correct_variants:
        print("Правильно! Вы получили награду.")
        room['puzzle'] = None
        if (current_room in ['hall'] 
            and 'treasure_key' not in game_state['player_inventory']):
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили ключ от сокровищницы!")
        else:
            print("Вы чувствуете, что продвинулись вперёд.")
    else:
        if current_room == 'trap_room':
            trigger_trap(game_state)
        else:
            print("Неверно. Попробуйте снова.")

"""
Открытие сундука
"""
def attempt_open_treasure(game_state):
    current_room = game_state['current_room']

    if current_room != 'treasure_room':
        print("Здесь нет сундука.")
        return

    room = ROOMS[current_room]

    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт.")
        return

    # Проверка ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    # Если ключа нет спрашиваем, хочет ли игрок ввести код
    print("Сундук заперт. Кажется, его можно открыть с помощью кода.")
    choice = get_input("Хотите попробовать ввести код? (да/нет): ").strip().lower()

    if choice == 'да':
        if room['puzzle'] is not None:
            question, correct_answer = room['puzzle']
            user_code = get_input("Введите код: ").strip().lower()

            if user_code == correct_answer.lower():
                print("Код верный! Сундук открыт!")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук не открывается.")
        else:
            print("Нет загадки, чтобы получить код.")
    else:
        print("Вы отступаете от сундука.")

"""
Показ справки
"""
def show_help(COMMANDS):
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")

def pseudo_random(seed, modulo):
    value = math.sin(seed * 51.5721) * 75636.2376
    fract = value - math.floor(value)
    result = fract * modulo
    return int(result)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        # Выбор случайного индекса предмета
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли: {lost_item}")
    else:
        # Получение урона игроком
        damage = pseudo_random(game_state['steps_taken'], 10)
        if damage < 3:
            print("Вы не выдержали испытания. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы уцелели, но едва.")

"""
Случайные события
"""
def random_event(game_state):

    # Проверка произойдёт ли событие
    if pseudo_random(game_state['steps_taken'], 10) != 0:
        return

    event_type = pseudo_random(game_state['steps_taken'], 3)

    if event_type == 0:
        # Сценарий 1: Находка
        current_room = game_state['current_room']
        room = ROOMS[current_room]
        if 'coin' not in room['items']:
            room['items'].append('coin')
            print("Вы нашли монетку на полу!")
        else:
            print("Вы слышите звук, как будто что-то звенит," \
            " но ничего не находите.")
    elif event_type == 1:
        # Сценарий 2: Испуг
        print("Вы слышите странный шорох...")
        if 'sword' in game_state['player_inventory']:
            print("Вы достаете меч, шорох прекращается.")
    elif event_type == 2:
        # Сценарий 3: Срабатывание ловушки
        current_room = game_state['current_room']
        if current_room == 'trap_room' & 'torch' not in game_state['player_inventory']:
            print("Вы зашли в тёмную комнату и наткнулись на ловушку!")
            trigger_trap(game_state)
        else:
            print("Вы освещаете комнату факелом и находите ловушку." \
                " Двигаясь осторожно, вам удалось её избежать!")
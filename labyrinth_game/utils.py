from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


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
        print("Кажется, здесь есть загадка (используйте команду solve).")
    print()


def solve_puzzle(game_state):
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room['puzzle']
    print("Загадка:", question)
    user_answer = get_input("Ваш ответ: ").strip().lower()

    if user_answer == correct_answer.lower():
        print("Правильный ответ!")
        room['puzzle'] = None
        if current_room in ['hall'] and 'treasure_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили ключ от сокровищницы!")
        else:
            print("Вы чувствуете, что продвинулись вперёд.")
    else:
        print("Неверно. Попробуйте снова.")


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

    # Если ключа нет — спрашиваем, хочет ли ввести код
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


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  steps           - показать количество пройденных шагов")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
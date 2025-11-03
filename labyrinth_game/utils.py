from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    
    if room['items']:
        print("Предметы:", ", ".join(room['items']))
    else:
        print("Предметы: нет")

    exits = room['exits']
    if exits:
        directions = ", ".join(exits.keys())
        print(f"Выходы: {directions}")
    else:
        print("Выходы: нет")

    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")
    print()
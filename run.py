import sys
from heapq import heappush, heappop


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """
    COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

    LETTERS_TO_ROOMS = {"A": 2, "B": 4, "C": 6, "D": 8}

    VALID_HALLWAY = [0, 1, 3, 5, 7, 9, 10]

    def state_to_tuple(hallway, rooms):
        return (
            tuple(hallway),
            tuple(rooms['A']),
            tuple(rooms['B']),
            tuple(rooms['C']),
            tuple(rooms['D'])
        )

    def is_done(rooms, depth):
        for room_type in 'ABCD':
            if len(rooms[room_type]) != depth:
                return False
            if any(el != room_type for el in rooms[room_type]):
                return False
        return True

    def parse_input(lines: list[str]):
        # Глубина комнат
        depth = len(lines) - 3
        # Пустой коридор
        hallway = [None] * 11

        rooms = {'A': [], 'B': [], 'C': [], 'D': []}
        rooms_with_indexes = {"A": 3, "B": 5, "C": 7, "D": 9}

        for i in range(depth, 0, -1):
            line = lines[1 + i]
            for letter, index in rooms_with_indexes.items():
                rooms[letter].append(line[index])

        return depth, hallway, rooms

    # Все возможные ходы из текущего состояния
    def get_moves(depth, hallway, rooms):
        moves = []

        for letter in "ABCD":
            room = rooms[letter]
            if not room:
                continue

            room_index = LETTERS_TO_ROOMS[letter]

            # Если комната правильная
            if all(obj == letter for obj in room):
                continue

            el = room[-1]
            # Пробуем переместить во все разрешенные позиции корридора
            for pos in VALID_HALLWAY:

                # Проверяем свободен ли путь
                start = min(pos, room_index)
                end = max(pos, room_index)

                able = True
                for i in range(start, end + 1):
                    if hallway[i] is not None:
                        able = False
                        break

                if able:
                    steps_in_room = depth - len(room) + 1
                    steps_in_hallway = abs(room_index - pos)
                    cost = (steps_in_room + steps_in_hallway) * COSTS[el]

                    new_hallway = hallway[:]
                    new_hallway[pos] = el
                    new_rooms = {k: v[:] for k, v in rooms.items()}
                    new_rooms[letter].pop()

                    moves.append((new_hallway, new_rooms, cost))

        # Пробуем зайти в комнату
        for pos, el in enumerate(hallway):
            if el is None:
                continue

            target_room_pos = LETTERS_TO_ROOMS[el]
            target_room = rooms[el]

            if any(obj != el for obj in target_room):
                continue

            # Проверяем свободен ли путь
            start = min(pos, target_room_pos)
            end = max(pos, target_room_pos)

            able = True

            for i in range(start, end + 1):
                if i != pos and hallway[i] is not None:
                    able = False
                    break

            if able:
                steps_in_hallway = abs(pos - target_room_pos)
                steps_in_room = depth - len(target_room)
                cost = (steps_in_hallway + steps_in_room) * COSTS[el]

                new_hallway = hallway[:]
                new_hallway[pos] = None
                new_rooms = {k: v[:] for k, v in rooms.items()}
                new_rooms[el].append(el)

                moves.append((new_hallway, new_rooms, cost))
        return moves

    # Считаем алгоритмом Дейкстры
    def dijkstra(depth, hallway, rooms):
        initial_state = state_to_tuple(hallway, rooms)

        # чтобы не выпадала ошибка сравнения None
        counter = 0

        queue = [(0, counter, initial_state, hallway, rooms)]
        visited = set()

        while queue:
            cost, _, state_tuple, hallway, rooms = heappop(queue)

            # Проверка если все на своих местах
            if is_done(rooms, depth):
                return cost

            # Если состояние еще не обработано
            if state_tuple not in visited:
                visited.add(state_tuple)

                for new_hallway, new_rooms, move_cost in get_moves(depth, hallway, rooms):
                    new_state_tuple = state_to_tuple(new_hallway, new_rooms)

                    if new_state_tuple not in visited:
                        counter += 1
                        heappush(
                            queue,
                            (
                                cost + move_cost, counter, new_state_tuple, new_hallway, new_rooms
                            )
                        )
        return -1

    depth, hallway, rooms = parse_input(lines)
    return dijkstra(depth, hallway, rooms)


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()

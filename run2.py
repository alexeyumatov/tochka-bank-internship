import sys
from typing import Any
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """

    # строим граф по всем узлам и шлюзам
    def build_graph(edges: list[tuple[str, str]]) -> defaultdict[Any, set]:
        graph = defaultdict(set)
        for node1, node2 in edges:
            graph[node1].add(node2)
            graph[node2].add(node1)
        return graph

    # разбиваем на узлы и шлюзы
    def classify_nodes(graph: defaultdict[Any, set]) -> tuple[set, set]:
        nodes = set()
        gateways = set()
        for node in graph:
            if node.isupper():
                gateways.add(node)
            else:
                nodes.add(node)
        return gateways, nodes

    # используем поиск в ширину по графу для дистанций
    def bfs_search(graph: defaultdict[Any, set], start: str) -> dict[str, int]:
        distances = {start: 0}
        queue = deque([start])

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)

        return distances

    def find_virus_next_pos(
        graph: defaultdict[str, set],
        virus_pos: str,
        target_gateway: str,
        distances: dict[str, int]
    ) -> str | None:
        if target_gateway not in distances:
            return None

        target_distance = distances[target_gateway]

        next_nodes = []
        for neighbor in graph[virus_pos]:
            neighbor_distances = bfs_search(graph, neighbor)
            if target_gateway in neighbor_distances:
                if neighbor_distances[target_gateway] == target_distance - 1:
                    next_nodes.append(neighbor)

        if len(next_nodes) != 0:
            next_nodes.sort()
            return next_nodes[0]

        return None

    result = []
    graph = build_graph(edges)
    gateways, _ = classify_nodes(graph)
    virus_pos = 'a'

    while True:
        # находим ближайший шлюз
        distances = bfs_search(graph, virus_pos)

        reachable_gateways = []
        for gateway in gateways:
            if gateway in distances:
                reachable_gateways.append(gateway)

        if len(reachable_gateways) == 0:
            break

        reachable_gateways.sort()
        target_gateway = reachable_gateways[0]

        # находим следующую позицию вируса исходя из ближайшего шлюза
        next_virus_pos = find_virus_next_pos(
            graph, virus_pos, target_gateway, distances
        )

        if next_virus_pos is None:
            break

        # выбираем какой корридор отключить
        if next_virus_pos.isupper():
            # Если следующая позиция - шлюз, отключаем его от текущей позиции
            result.append(f"{next_virus_pos}-{virus_pos}")
            graph[next_virus_pos].discard(virus_pos)
            graph[virus_pos].discard(next_virus_pos)
            gateways.discard(next_virus_pos)
        else:
            # Иначе отключаем коридор от целевого шлюза (лексикографически минимальный)
            corridors = []
            for neighbour in sorted(graph[target_gateway]):
                if not neighbour.isupper():
                    corridors.append((target_gateway, neighbour))

            if len(corridors) != 0:
                disconnect_gateway, disconnect_node = corridors[0]
                result.append(f"{disconnect_gateway}-{disconnect_node}")
                graph[disconnect_gateway].discard(disconnect_node)
                graph[disconnect_node].discard(disconnect_gateway)

        # пересчитываем путь и перемещаем вирус
        distances = bfs_search(graph, virus_pos)

        reachable_gateways = []
        for gateway in gateways:
            if gateway in distances:
                reachable_gateways.append(gateway)

        if len(reachable_gateways) == 0:
            break

        reachable_gateways.sort()
        target_gateway = reachable_gateways[0]

        virus_pos = find_virus_next_pos(
            graph, virus_pos, target_gateway, distances
        )

        if virus_pos is None:
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()

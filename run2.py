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
                reachable_gateways.append((distances[gateway], gateway))

        if len(reachable_gateways) == 0:
            break

        reachable_gateways.sort()
        min_distance, target_gateway = reachable_gateways[0]

        # находим следующую позицию вируса исходя из ближайшего шлюза
        next_virus_pos = find_virus_next_pos(
            graph, virus_pos, target_gateway, distances
        )

        if next_virus_pos is None:
            break

        # выбираем какой корридор отключить
        nodes_on_path = []
        for neighbor in graph[target_gateway]:
            if not neighbor.isupper():
                if neighbor in distances:
                    if distances[neighbor] + 1 == distances[target_gateway]:
                        nodes_on_path.append(neighbor)

        if len(nodes_on_path) == 0:
            break

        nodes_on_path.sort()
        disconnect_node = nodes_on_path[0]
        result.append(f"{target_gateway}-{disconnect_node}")
        graph[target_gateway].discard(disconnect_node)
        graph[disconnect_node].discard(target_gateway)

        # пересчитываем путь и перемещаем вирус
        virus_pos = next_virus_pos

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

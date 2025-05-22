import heapq


def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    previous = {}

    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(queue, (distance, neighbor))

    return distances, previous


def reconstruct_path(previous, destination):
    path = []
    while destination in previous:
        path.insert(0, destination)
        destination = previous[destination]

    path.insert(0, destination)
    return path

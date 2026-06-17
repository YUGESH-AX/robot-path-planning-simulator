import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, obstacles, rows, cols):

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == goal:

            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path

        row, col = current

        neighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1)
        ]

        for neighbor in neighbors:

            r, c = neighbor

            if r < 0 or c < 0 or r >= rows or c >= cols:
                continue

            if neighbor in obstacles:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(open_set, (f_score, neighbor))

    return []
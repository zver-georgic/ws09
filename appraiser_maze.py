import random
from collections import deque

def main():
    with open('matrix_maze.txt', 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    print(lines)
    rows, cols = map(int, lines[0].split())
    maze = [list(map(int, list(lines[i]))) for i in range(1, rows + 1)]
    start = tuple(map(int, lines[rows + 1].split()))
    end = tuple(map(int, lines[rows + 2].split()))
    maze = maze[::-1]
    return maze, rows, cols, start, end


def fork_func(maze):
    rows = len(maze)
    cols = len(maze[0])
    fork = {}
    for i in range(rows):
        for j in range(cols):
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            vr = [(i + m[0], j + m[1]) for m in moves]
            for t in vr:
                if (0 <= t[0] < rows and
                        0 <= t[1] < cols and
                        maze[t[0]][t[1]] != 1 and maze[i][j] != 1):
                    fork.setdefault((i, j), set()).add(t)
            if len(fork.get((i, j), set())) < 3:
                fork.pop((i, j), None)
    return fork


def nearest_fork_free(vis, fork):
    pos = []
    for f in fork:
        klet = fork[f]
        fr = klet - vis
        if fr:
            pos.append(f)
    return pos


def bfs_fork_free(start, vis, fork, maze, rows, cols):
    """
    Ищет кратчайший путь до ближайшей развилки, у которой есть хотя бы один непосещённый сосед.
    Возвращает (расстояние, путь) или (None, None)
    """
    queue = deque([start])
    parent = {start: None}
    visited_bfs = {start}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        cur = queue.popleft()
        # Проверяем: является ли cur развилкой с непосещённым соседом
        if cur in fork:
            if fork[cur] - vis:   # есть свободный проход
                # Восстанавливаем путь
                path = []
                node = cur
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return len(path) - 1, path   # расстояние = число шагов

        for dr, dc in directions:
            nr, nc = cur[0] + dr, cur[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 1:
                    continue
                nb = (nr, nc)
                if nb not in visited_bfs and nb not in vis:
                    visited_bfs.add(nb)
                    parent[nb] = cur
                    queue.append(nb)
    return None, None


def dfs_monte_carlo(maze, rows, cols, start, end, l, vis, fork):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vis.add(start)
    print(start)
    if start == end:
        return l, True

    st = l
    vr = [(start[0] + i[0], start[1] + i[1]) for i in moves]
    random.shuffle(vr)

    for i in vr:
        if (0 <= i[0] < rows and
                0 <= i[1] < cols and
                i not in vis and
                maze[i[0]][i[1]] != 1):

            res, found = dfs_monte_carlo(maze, rows, cols, i, end, l + 1, vis, fork)
            if found:
                return res, True
            l += (res)

    # Все соседи посещены или привели к тупику — пробуем перепрыгнуть к ближайшей развилке
    dist, path = bfs_fork_free(start, vis, fork, maze, rows, cols)
    if path is not None:
        # Добавляем все клетки пути (кроме start, она уже в vis) в посещённые
        for cell in path[1:]:
            vis.add(cell)
        fork_point = path[-1]
        res, found = dfs_monte_carlo(maze, rows, cols, fork_point, end, l + dist, vis, fork)
        if found:
            return res, True

    return 2 * (l - st), False


def simulation(maze, rows, cols, start, end, N):
    sum_steps = 0
    for i in range(N):
        vis = set()
        fork = fork_func(maze)      # видимо, нужно вычислять fork один раз, но оставим здесь для минимальных правок
        result = dfs_monte_carlo(maze, rows, cols, start, end, 0, vis, fork)
        if result[1]:
            sum_steps += result[0]
    return sum_steps / N


maze, rows, cols, start, end = main()
print()
print(simulation(maze, rows, cols, start, end, N=1))

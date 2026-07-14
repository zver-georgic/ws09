import random
from collections import deque

# --------------------- Загрузка лабиринта ---------------------
def main():
    with open('matrix_maze.txt', 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    rows, cols = map(int, lines[0].split())
    maze = [list(map(int, list(lines[i]))) for i in range(1, rows + 1)]
    start = tuple(map(int, lines[rows + 1].split()))
    end = tuple(map(int, lines[rows + 2].split()))
    maze = maze[::-1]          # переворот, как у вас
    return maze, rows, cols, start, end


# --------------------- Развилки ---------------------
def fork_func(maze):
    rows, cols = len(maze), len(maze[0])
    fork = {}
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                continue
            moves = [(-1,0), (1,0), (0,-1), (0,1)]
            neighbors = set()
            for dr, dc in moves:
                nr, nc = i+dr, j+dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                    neighbors.add((nr, nc))
            if len(neighbors) >= 3:          # развилка: 3 или 4 свободных соседа
                fork[(i,j)] = neighbors
    return fork


# --------------------- BFS до ближайшей свободной развилки ---------------------
def bfs_fork_free(start, vis, fork, maze, rows, cols):
    queue = deque([start])
    parent = {start: None}
    visited_bfs = {start}
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while queue:
        cur = queue.popleft()
        if cur in fork:
            if fork[cur] - vis:          # есть непосещённые соседи
                path = []
                node = cur
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return len(path) - 1, path

        for dr, dc in directions:
            nr, nc = cur[0]+dr, cur[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 1:
                    continue
                nb = (nr, nc)
                if nb not in visited_bfs and nb not in vis:
                    visited_bfs.add(nb)
                    parent[nb] = cur
                    queue.append(nb)
    return None, None


# --------------------- Рекурсивный поиск с прыжками ---------------------
def dfs_monte_carlo(maze, rows, cols, start, end, l, vis, fork, visited_order=None):
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    vis.add(start)
    if visited_order is not None:
        visited_order.append(start)
    print(start)                     # <-- вывод текущей клетки при входе

    if start == end:
        return l, True

    vr = [(start[0]+dr, start[1]+dc) for dr, dc in moves]
    random.shuffle(vr)

    for nb in vr:
        if (0 <= nb[0] < rows and 0 <= nb[1] < cols and
            nb not in vis and maze[nb[0]][nb[1]] != 1):
            res, found = dfs_monte_carlo(maze, rows, cols, nb, end, l+1, vis, fork, visited_order)
            if found:
                return res, True

    # Все соседи исчерпаны – прыжок к ближайшей развилке с непосещёнными проходами
    dist, path = bfs_fork_free(start, vis, fork, maze, rows, cols)
    if path is not None:
        for cell in path[1:]:                 # все клетки пути, кроме стартовой
            vis.add(cell)
            if visited_order is not None:
                visited_order.append(cell)
            print(cell)                       # <-- вывод каждой клетки BFS-прыжка
        fork_point = path[-1]
        res, found = dfs_monte_carlo(maze, rows, cols, fork_point, end, l+dist, vis, fork, visited_order)
        if found:
            return res, True

    return -1, False


# --------------------- Симуляция (несколько запусков) ---------------------
def simulation(maze, rows, cols, start, end, N):
    sum_steps = 0
    visit_counts = {}
    for _ in range(N):
        vis = set()
        fork = fork_func(maze)
        visited_order = []        # если хотите сохранять полный порядок
        res, found = dfs_monte_carlo(maze, rows, cols, start, end, 0, vis, fork, visited_order)
        if found:
            sum_steps += res
        for cell in vis:
            visit_counts[cell] = visit_counts.get(cell, 0) + 1

    # Матрица частот
    freq_matrix = [[0]*cols for _ in range(rows)]
    for (r,c), cnt in visit_counts.items():
        if 0 <= r < rows and 0 <= c < cols:
            freq_matrix[r][c] = cnt

    avg = sum_steps / N if N > 0 else 0
    return avg, freq_matrix, visit_counts


# --------------------- Пример запуска ---------------------
if __name__ == "__main__":
    maze, rows, cols, start, end = main()
    N = 10   # число симуляций
    avg_len, freq_mat, counts = simulation(maze, rows, cols, start, end, N)

    print(f"\nСредняя длина пути за {N} симуляций: {avg_len:.2f}")
    print("\nМатрица частоты посещений:")
    for row in freq_mat:
        print(" ".join(f"{v:3d}" for v in row))

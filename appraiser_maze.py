import random
def main():
    with open('matrix_maze.txt', 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    print(lines)
    rows, cols = map(int, lines[0].split())
    maze = [list(map(int, list(lines[i]))) for i in range(1, rows + 1)]
    start = tuple(map(int, lines[rows + 1].split()))
    end = tuple(map(int, lines[rows + 2].split()))
    maze=maze[::-1]
    return maze, rows, cols, start, end


def fork_func(maze):
    rows=len(maze)
    cols=len(maze[0])
    for i in range(rows):
        for j in range(cols):
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            vr = [(i + m[0], j + m[1]) for m in moves]
            for t in vr:
                if (0 <= t[0] < rows and
                        0 <= t[1] < cols and
                        maze[t[0]][t[1]] !=1  and maze[i][j]!=1):
                    fork.setdefault((i,j), set()).add(t)
            if len(fork.get((i,j), set())) < 3:
                fork.pop((i,j), None)
    return fork
def nearest_fork_free(vis,fork):
    pos=[]
    for f in fork:
        klet=fork[f]
        fr=klet-vis

        if fr:
            pos.append(f)
    return pos
def bfs_fork_free(start,vis,fork):
    pos=nearest_fork_free(vis, fork)




def dfs_monte_carlo(maze, rows, cols, start, end, l, vis,fork):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vis.add(start)
    print(start)
    if start == end:
        return l, True
    st=l
    vr = [(start[0] + i[0], start[1] + i[1]) for i in moves]
    random.shuffle(vr)
    for i in vr:
        if (0 <= i[0] < rows and
                0 <= i[1] < cols and
                i not in vis and
                maze[i[0]][i[1]] != 1):

            res, found = dfs_monte_carlo(maze, rows, cols, i, end, l + 1, vis,fork)
            if found:
                return res, True
            l += (res)
            print(nearest_fork_free(vis, fork), start)
    return 2*(l-st), False

def simulation(maze, rows, cols, start, end,N):
    sum_steps=0
    for i in range(N):
        vis = set()
        result = dfs_monte_carlo(maze, rows, cols, start, end, 0, vis,fork_func(maze))
        if result[1]:
            sum_steps += result[0]
    return sum_steps/N


maze, rows, cols, start, end = main()
sred=0
fork={}
N=1
print()
print(simulation(maze, rows, cols, start, end,N))

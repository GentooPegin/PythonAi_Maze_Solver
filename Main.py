from random import choice

maze = [
    [0, 1, 0, 2, 0],
    [2, 0, 2, 0, 0],
    [0, 0, 0, 2, 0],
    [0, 2, 0, 0, 0],
    [0, 0, 0, 2, 3]
]

maze_size = len(maze)

def choice_selection():
    ai_i, ai_j = find_ai()
    ai_move = max(q_table[(ai_i, ai_j)], key=q_table[(ai_i, ai_j)].get)
    return ai_movment_calculation(ai_move)

def ai_movment_calculation(ai_move):

    reward = 0
    old_i, old_j = find_ai()
    ai_i, ai_j = old_i, old_j
    match ai_move:
        case "up":
            ai_i -= 1
        case "down":
            ai_i += 1
        case "left":
            ai_j -= 1
        case "right":
            ai_j += 1

    if ai_i < 0 or ai_i >= maze_size or ai_j < 0 or ai_j >= maze_size:
        reward -= 10
        ai_i, ai_j = old_i, old_j
        
    elif maze[ai_i][ai_j] == 2:
        reward -= 5
        ai_i, ai_j = old_i, old_j

    elif maze[ai_i][ai_j] == 3:
        print("The Ai Escaped!")
        reward += 300
        update_q_table(old_i, old_j, ai_move, reward, ai_i, ai_j)
        return True, reward
    
    else:
        clean_maze()
        maze[ai_i][ai_j] = 1
        reward -= 1

    update_q_table(old_i, old_j, ai_move, reward, ai_i, ai_j)
    return False, reward

def clean_maze():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                maze[i][j] = 0
    
def find_ai():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                return i, j

    print("ERROR NO AI FOUND!")
    

def update_q_table(old_i, old_j, ai_move, reward, ai_i, ai_j):
    current_q = q_table[(old_i, old_j)][ai_move]
    best_future_q = max(q_table[(ai_i, ai_j)].values())

    new_q = current_q + alpha * (reward + gamma * best_future_q - current_q)

    q_table[(old_i, old_j)][ai_move] = new_q

q_table = {} # stores temperary memory from learning
alpha = 0.1
gamma = 0.9


for i in range(maze_size):
    for j in range(maze_size):
        if maze[i][j] != 2:
            q_table[(i, j)] = {
                "up": 0,
                "down": 0,
                "left": 0,
                "right": 0
            }



number_of_runs = 100


for i in range(0, number_of_runs):

    escaped = False
    turn_timer = 0

    while not escaped:
        escaped, reward = choice_selection()
        turn_timer += 1

    print(f'It took the Ai {turn_timer} turns to escape.')
    clean_maze()
    maze[0][1] = 1

print(q_table)

#After session 2
#The ai crushes the maze really quickly. I should make a way for the user to make the maze and maybe visuals?
#The maze could be squares on screen and you could see the path the ai takes after a bunch of runs?

import tkinter as tk
import ai

window = tk.Tk()

maze_size = 3

window.title("Maze AI")
window.geometry("600x600")

canvas_size = 400
square_size = canvas_size // maze_size


canvas = tk.Canvas(
    window,
    width=canvas_size,
    height=canvas_size,
    highlightthickness=0,
    bd=0
)

canvas.pack(padx=10, pady=10)

starting_position = None
goal_position = None
wall_positions = []

active_mode = None

#Modes of clicks while making the maze using ui
def StartMode():
    print("Start!")
    global active_mode 
    active_mode = "start"

def WallMode():
    print("Wall!")
    global active_mode 
    active_mode = "wall"

def GoalMode():
    print("Goal!")
    global active_mode 
    active_mode = "goal"

def EraseMode():
    print("Erase!")
    global active_mode 
    active_mode = "erase"

def square_clicked(event): #Checks if the square is clicked, what mode is currently active and changes the color and remembers the (x, y)
    global starting_position
    global goal_position
    global wall_positions

    column = event.x // square_size
    row = event.y // square_size

    if active_mode == "start":

        if (row, column) in wall_positions:
            return

        if (row, column) == goal_position:
            return

        if starting_position is not None:
            old_row, old_column = starting_position
            canvas.itemconfig(squares[old_row][old_column], fill="white")

        starting_position = (row, column)

        canvas.itemconfig(squares[row][column], fill="red")

    elif active_mode == "goal":

        if (row, column) in wall_positions:
            return

        if (row, column) == starting_position:
            return

        if goal_position is not None:
            old_row, old_column = goal_position
            canvas.itemconfig(squares[old_row][old_column], fill="white")
        
        goal_position = (row, column)
        
        canvas.itemconfig(squares[row][column], fill="green")

    elif active_mode == "wall":
        if (row, column) == starting_position:
            return

        if (row, column) == goal_position:
            return

        if (row, column) in wall_positions:
            return

        canvas.itemconfig(squares[row][column], fill="black")
        wall_positions.append((row, column))

    elif active_mode == "erase":

        if (row, column) in wall_positions:
            wall_positions.remove((row, column))
        elif (row, column) == starting_position:
            starting_position = None
        elif (row, column) == goal_position:
            goal_position= None

        canvas.itemconfig(squares[row][column], fill="white")


path_squares = []

def update_training_progress(run):
    training_label.config(text=f"Training AI... {run} / {runs_input.get()}")
    window.update()

def FinalizeMaze(): #Makes the maze and runs the ai training
    maze = []
    HideControls()
    training_label.pack(pady=10)
    window.update()
    for i in range(maze_size):
        row = []

        for j in range(maze_size):
            row.append(0)

        maze.append(row)

    for row, column in wall_positions:
        maze[row][column] = 2

    if starting_position is not None:
        row, column = starting_position
        maze[row][column] = 1

    if goal_position is not None:
        row, column = goal_position
        maze[row][column] = 3

    number_of_runs = int(runs_input.get())
    path = ai.TrainAi(maze, starting_position, number_of_runs, update_training_progress) #Calls the function from ai.py 
    training_label.pack_forget()

    for square in path:
        row, column = square

        if (row, column) != starting_position and (row, column) != goal_position:
            canvas.itemconfig(squares[row][column], fill="orange")
            path_squares.append((row, column))

    confirm_button.pack()

def Confirm(): #Cleans up the orange squares, appears only after ai finished training
    global path_squares

    for row, column in path_squares:
        canvas.itemconfig(squares[row][column], fill="white")

    path_squares = []
    confirm_button.pack_forget()
    ShowControls()

canvas.bind("<Button-1>", square_clicked)

squares = []

for i in range(maze_size):
    row = []

    for j in range(maze_size):
        square = canvas.create_rectangle(
            j * square_size + 1,
            i * square_size + 1,
            (j + 1) * square_size - 1,
            (i + 1) * square_size - 1
        )

        row.append(square)

    squares.append(row)

button_frame = tk.Frame(window) #Creates the container for the buttons
button_frame.pack(pady=10)

#Button creation for ui modes
start_button = tk.Button(button_frame, text="Place Start", command=StartMode, width=12, height=2)
wall_button = tk.Button(button_frame, text="Place Walls", command=WallMode, width=12, height=2)
goal_button = tk.Button(button_frame, text="Place Goal", command=GoalMode, width=12, height=2)
erase_button = tk.Button(button_frame, text="Erase", command=EraseMode, width=12, height=2)

start_button.pack(side="left", padx = 5)
wall_button.pack(side="left", padx = 5)
goal_button.pack(side="left", padx = 5)
erase_button.pack(side="left", padx = 5)

finalize_maze = tk.Button(window, text="Finalize Maze", command=FinalizeMaze)
finalize_maze.pack()

confirm_button = tk.Button(
    window,
    text="Confirm",
    command=Confirm
)


def HideControls(): #Hides the buttons while training
    button_frame.pack_forget()
    size_frame.pack_forget()
    runs_frame.pack_forget()
    finalize_maze.pack_forget()

def ShowControls(): #Shows the buttons after confirmation
    button_frame.pack(pady=10)
    finalize_maze.pack()
    size_frame.pack(pady=5)
    runs_frame.pack(pady=5)

#Size of the maze code is everything under this!
def ApplySize(): 
    global maze_size
    global square_size
    global squares
    global starting_position
    global goal_position
    global wall_positions
    global path_squares

    maze_size = int(size_input.get())

    if maze_size < 3:
        maze_size = 3

    if maze_size > 20:
        maze_size = 20


    square_size = canvas_size // maze_size

    starting_position = None
    goal_position = None
    wall_positions = []
    path_squares = []

    canvas.delete("all")

    squares = []

    for i in range(maze_size):
        row = []

        for j in range(maze_size):
            square = canvas.create_rectangle(
                j * square_size + 1,
                i * square_size + 1,
                (j + 1) * square_size - 1,
                (i + 1) * square_size - 1
            )

            row.append(square)

        squares.append(row)

#The container/frame for size input
size_frame = tk.Frame(window)
size_frame.pack(pady=5)

#Lets the user input how big the maze can be (3x3, 5x5, 10x10...)
size_label = tk.Label(size_frame, text="Maze size:")
size_label.pack(side="left")

def check_size(value): #Makes sure the size of the maze isnt bigger then 20x20
    if value == "":
        return True

    if not value.isdigit():
        return False

    if int(value) > 20:
        size_input.delete(0, tk.END)
        size_input.insert(0, "20")

    return True


size_input = tk.Spinbox(
    size_frame,
    from_=3,
    to=20,
    width=5,
    validate="key",
    validatecommand=(window.register(check_size), "%P")
)
size_input.pack(side="left", padx=5)

size_button = tk.Button(
    size_frame,
    text="Apply Size",
    command=ApplySize
)
size_button.pack(side="left")

#Takes user input for how many runs there should be
runs_frame = tk.Frame(window)
runs_frame.pack(pady=5)

runs_label = tk.Label(runs_frame, text="Training runs:")
runs_label.pack(side="left")

runs_input = tk.Spinbox(
    runs_frame,
    from_=1,
    to=1000,
    width=5
)
runs_input.pack(side="left", padx=5)

#shows that the ai is currently training
training_label = tk.Label(
    window,
    text="Training AI..."
)

window.mainloop()
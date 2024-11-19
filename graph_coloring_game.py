import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize scores
score = 0
high_score = 0

# Function to update the score display
def update_score_display():
    score_label.config(text=f"Score: {score}")
    high_score_label.config(text=f"High Score: {high_score}")

# Create a display function with a fixed layout
def display_graph():
    plt.clf()
    nx.draw(graph, pos, node_color=[color_map[node] for node in graph.nodes], with_labels=True, node_size=700, font_color="white", font_size=10)
    canvas.draw()

# Function to handle node coloring and game logic
def color_node(node, selected_color):
    global score, high_score
    if int(node) in color_map:
        if selected_color in [color_map[neighbor] for neighbor in graph.neighbors(int(node))]:
            messagebox.showerror("Invalid Move", "Adjacent nodes can't have the same color!")
            score -= 5  # Penalty for invalid move
        else:
            if color_map[int(node)] == "gray":
                score += 10  # Reward for valid move
            color_map[int(node)] = selected_color
            display_graph()
            check_win()
    else:
        messagebox.showerror("Error", "Select a valid node.")
    # Update the high score
    if score > high_score:
        high_score = score
    update_score_display()

# Function to check if the game is won once all nodes are colored
# Function to check if the game is won once all nodes are colored
def check_win():
    global score
    if all(color != "gray" for color in color_map.values()):
        for node in graph.nodes:
            node_color = color_map[node]
            if any(color_map[neighbor] == node_color for neighbor in graph.neighbors(node)):
                return False
        
        # Apply difficulty multiplier to the final score
        if difficulty_var.get() == "Medium":
            score *= 2  # Multiply score by 2 for Medium difficulty
        elif difficulty_var.get() == "Hard":
            score *= 3  # Multiply score by 3 for Hard difficulty

        # Bonus based on the number of colors used
        used_colors_count = count_used_colors()
        if used_colors_count <= 3:  
            score += 20 
        elif used_colors_count <= 2:
             score += 50   
        elif used_colors_count == 4:
            score += 10 

        messagebox.showinfo("Congratulations!", f"You've successfully colored the graph!\nFinal Score: {score}")
        return True
    return False

# Function to generate a new graph based on difficulty
def generate_graph(difficulty):
    global graph, color_map, pos, score
    score = 0  # Reset score
    update_score_display()
    if difficulty == "Easy":
        graph = nx.gnp_random_graph(5, 0.4)
    elif difficulty == "Medium":
        graph = nx.gnp_random_graph(8, 0.5)
    else:  # Hard
        graph = nx.gnp_random_graph(10, 0.6)
    difficulty_label.config(text=f"Difficulty: {difficulty}")
    color_map = {node: "gray" for node in graph.nodes}
    pos = nx.spring_layout(graph, seed=42)
    display_graph()

# Function to provide a hint
def give_hint():
    global score
    for node in graph.nodes:
        if color_map[node] == "gray":
            for color in colors:
                if all(color_map[neighbor] != color for neighbor in graph.neighbors(node)):
                    color_map[node] = color
                    score -= 5  # Penalty for using a hint
                    display_graph()
                    update_score_display()
                    return
    messagebox.showinfo("Hint", "No possible moves detected.")

# Functions to navigate nodes and colors
def select_next_node(event=None):
    current_node = int(node_var.get())
    next_node = (current_node + 1) % len(graph.nodes)
    node_var.set(str(next_node))

def select_previous_node(event=None):
    current_node = int(node_var.get())
    previous_node = (current_node - 1) % len(graph.nodes)
    node_var.set(str(previous_node))

def select_next_color(event=None):
    current_color = color_var.get()
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]
    color_var.set(next_color)

def select_previous_color(event=None):
    current_color = color_var.get()
    previous_color = colors[(colors.index(current_color) - 1) % len(colors)]
    color_var.set(previous_color)


def count_used_colors():
    used_colors = set(color for color in color_map.values() if color != "gray")
    return len(used_colors)
# Initialize the Tkinter window
root = tk.Tk()
root.title("Graph Coloring Game")
root.geometry("1600x800")
root.configure(bg="#2b2b2b")  # Dark background

# Score and difficulty display
header_frame = tk.Frame(root, bg="#444444")
header_frame.pack(side=tk.TOP, fill=tk.X)

score_label = tk.Label(header_frame, text=f"Score: {score}", font=("Arial", 20), fg="white", bg="#444444")
score_label.pack(side=tk.RIGHT, padx=20)  # Change side to RIGHT

high_score_label = tk.Label(header_frame, text=f"High Score: {high_score}", font=("Arial", 20), fg="white", bg="#444444")
high_score_label.pack(side=tk.RIGHT, padx=20)  # Change side to RIGHT

# Graph area
fig, ax = plt.subplots(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Hotkeys and instructions
instructions_frame = tk.Frame(root, bg="#2b2b2b")
instructions_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
instructions_label = tk.Label(instructions_frame, text=(
    "Hotkeys:\n"
    "E: Easy\n"
    "M: Medium\n"
    "H: Hard\n"
    "Arrow Keys: Navigate nodes/colors\n"
    "Enter: Color selected node\n"
    "N: Get a hint"
), font=("Arial", 12), fg="white", bg="#2b2b2b", justify="left")
instructions_label.pack(anchor="w")

# Control panel
control_frame = tk.Frame(root, bg="#444444")
control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

# Difficulty dropdown
difficulty_label = tk.Label(control_frame, text="Difficulty:", font=("Arial", 14), fg="white", bg="#444444")
difficulty_label.pack(side=tk.LEFT, padx=10)
difficulty_var = tk.StringVar(value="Medium")
difficulty_dropdown = tk.OptionMenu(control_frame, difficulty_var, "Easy", "Medium", "Hard")
difficulty_dropdown.config(font=("Arial", 14), bg="#555555", fg="white")
difficulty_dropdown.pack(side=tk.LEFT, padx=10)

# New game button
new_game_button = tk.Button(control_frame, text="New Game", command=lambda: generate_graph(difficulty_var.get()),
                            font=("Arial", 14), bg="#008CBA", fg="white")
new_game_button.pack(side=tk.LEFT, padx=10)

# Node and color selection
node_label = tk.Label(control_frame, text="Select Node:", font=("Arial", 14), fg="white", bg="#444444")
node_label.pack(side=tk.LEFT, padx=10)
node_var = tk.StringVar(value="0")
node_dropdown = tk.OptionMenu(control_frame, node_var, *map(str, range(10)))
node_dropdown.config(font=("Arial", 14), bg="#555555", fg="white")
node_dropdown.pack(side=tk.LEFT, padx=10)

color_label = tk.Label(control_frame, text="Select Color:", font=("Arial", 14), fg="white", bg="#444444")
color_label.pack(side=tk.LEFT, padx=10)
colors = ["green", "red", "blue", "yellow", "black"]
color_var = tk.StringVar(value=colors[0])
color_dropdown = tk.OptionMenu(control_frame, color_var, *colors)
color_dropdown.config(font=("Arial", 14), bg="#555555", fg="white")
color_dropdown.pack(side=tk.LEFT, padx=10)


# Function to update the button color based on the selected color
def update_button_color(*args):
    selected_color = color_var.get() 
    color_button.config(bg=selected_color) 


color_var.trace_add("write", update_button_color)

color_button = tk.Button(control_frame, text="Color Node", command=lambda: color_node(node_var.get(), color_var.get()),
                         font=("Arial", 14), bg="#4CAF50", fg="white")
color_button.pack(side=tk.LEFT, padx=10)

# Hint button
hint_button = tk.Button(control_frame, text="Hint", command=give_hint, font=("Arial", 14), bg="#f44336", fg="white")
hint_button.pack(side=tk.LEFT, padx=10)

# Hotkey bindings
root.bind("<e>", lambda event: generate_graph("Easy"))
root.bind("<m>", lambda event: generate_graph("Medium"))
root.bind("<h>", lambda event: generate_graph("Hard"))
root.bind("<Right>", select_next_node)
root.bind("<Left>", select_previous_node)
root.bind("<Up>", select_next_color)
root.bind("<Down>", select_previous_color)
root.bind("<Return>", lambda event: color_node(node_var.get(), color_var.get()))
root.bind("<n>", lambda event: give_hint())

# Start a new game initially with medium difficulty
generate_graph("Medium")

# Start the Tkinter event loop
root.mainloop()

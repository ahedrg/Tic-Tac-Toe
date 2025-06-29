import tkinter as tk
from tkinter import messagebox
import math

# Initialize variables
board = [' ' for _ in range(9)]
player_symbol = 'X'
ai_symbol = 'O'
current_turn = 'X'
buttons = []

# Check for winner
def check_winner(brd, player):
    win_states = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(brd[i] == player for i in combo) for combo in win_states)

def is_draw(brd):
    return ' ' not in brd

# Minimax with alpha-beta
def minimax(brd, depth, alpha, beta, is_maximizing):
    if check_winner(brd, ai_symbol):
        return 1
    if check_winner(brd, player_symbol):
        return -1
    if is_draw(brd):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if brd[i] == ' ':
                brd[i] = ai_symbol
                eval = minimax(brd, depth + 1, alpha, beta, False)
                brd[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if brd[i] == ' ':
                brd[i] = player_symbol
                eval = minimax(brd, depth + 1, alpha, beta, True)
                brd[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def ai_move():
    best_score = -math.inf
    best_move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_symbol
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = ai_symbol
    buttons[best_move].config(text=ai_symbol, state="disabled")
    check_game_end()

def player_move(i):
    global current_turn
    if board[i] == ' ':
        board[i] = player_symbol
        buttons[i].config(text=player_symbol, state="disabled")
        if not check_game_end():
            ai_move()

def check_game_end():
    if check_winner(board, player_symbol):
        messagebox.showinfo("Game Over", "You win!")
        disable_all_buttons()
        return True
    elif check_winner(board, ai_symbol):
        messagebox.showinfo("Game Over", "AI wins!")
        disable_all_buttons()
        return True
    elif is_draw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        disable_all_buttons()
        return True
    return False

def disable_all_buttons():
    for btn in buttons:
        btn.config(state="disabled")

def start_game(symbol):
    global player_symbol, ai_symbol, current_turn, board
    player_symbol = symbol
    ai_symbol = 'O' if symbol == 'X' else 'X'
    current_turn = 'X'
    board = [' ' for _ in range(9)]
    for i in range(9):
        buttons[i].config(text=' ', state="normal")

    if ai_symbol == 'X':
        ai_move()

# GUI Setup
root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.configure(bg='#FF6B6B')  # Vibrant coral background
root.geometry("600x700")  # Set window size

def setup_start_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    # Main title
    title_frame = tk.Frame(root, bg='#FF6B6B')
    title_frame.pack(pady=40)
    title = tk.Label(title_frame, text="Tic-Tac-Toe AI", font=("Arial", 36, "bold"), bg='#FF6B6B', fg='#FFFFFF')
    title.pack()
    
    # Symbol selection
    label = tk.Label(root, text="Choose your symbol:", font=("Arial", 24), bg='#FF6B6B', fg='#FFFFFF')
    label.pack(pady=20)
    
    frame = tk.Frame(root, bg='#FF6B6B')
    frame.pack(pady=30)
    
    # Styled buttons
    button_style = {
        'width': 8,
        'height': 3,
        'font': ("Arial", 24, "bold"),
        'relief': 'raised',
        'bd': 5
    }
    
    x_btn = tk.Button(frame, text="X", bg='#4ECDC4', fg='white', command=lambda: [setup_board(), start_game('X')], **button_style)
    x_btn.grid(row=0, column=0, padx=20)
    
    o_btn = tk.Button(frame, text="O", bg='#FFE66D', fg='#2C3E50', command=lambda: [setup_board(), start_game('O')], **button_style)
    o_btn.grid(row=0, column=1, padx=20)

def setup_board():
    for widget in root.winfo_children():
        widget.destroy()
        
    # Game title
    title = tk.Label(root, text="Tic-Tac-Toe AI", font=("Arial", 32, "bold"), bg='#FF6B6B', fg='white')
    title.pack(pady=20)
    
    board_frame = tk.Frame(root, bg='#FF6B6B')
    board_frame.pack(pady=30)
    
    buttons.clear()
    for i in range(9):
        btn = tk.Button(board_frame, 
                       text=' ',
                       width=5,
                       height=2,
                       font=("Arial", 36, "bold"),
                       command=lambda i=i: player_move(i),
                       bg='#A8E6CF',
                       fg='#2C3E50',
                       activebackground='#DCEDC1',
                       relief='raised',
                       bd=5)
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(btn)
    
    # Add restart button
    restart_btn = tk.Button(root,
                          text="Restart Game",
                          command=setup_start_screen,
                          bg='#FF8B94',
                          fg='white',
                          font=("Arial", 18, "bold"),
                          relief='raised',
                          bd=4,
                          width=15,
                          height=2)
    restart_btn.pack(pady=30)

# Start the GUI
setup_start_screen()
root.mainloop()

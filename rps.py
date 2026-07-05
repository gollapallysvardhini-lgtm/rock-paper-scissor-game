import tkinter as tk
from tkinter import messagebox, PhotoImage
import random
import time
import pygame

# Initialize pygame mixer for sound effects and music
pygame.mixer.init()

# Global game state variables
mode = None                   # "pvp" or "pvc"
player1_name = ""
player2_name = ""
total_rounds = 0
current_round = 1
score1 = 0
score2 = 0
current_turn = "player1"      # used in PvP mode to track whose turn it is
pvp_choice = None             # temporarily holds player1's move in PvP mode
timer_id = None               # to keep track of the timer

# Global references for images and game window labels
images = {}
game_window = None

# Load custom font
custom_font = ("Helvetica", 14)  # Replace with your font file and size

# ----- Helper Functions -----

def set_background(window, image_path):
    """Sets a background image for the given window."""
    bg_image = PhotoImage(file=image_path)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection

def start_timer(window, time_left, timer_label):
    """Starts a countdown timer."""
    global timer_id
    if time_left > 0:
        timer_label.config(text=f"Time Left: {time_left}")
        timer_id = window.after(1000, start_timer, window, time_left - 1, timer_label)
    else:
        messagebox.showinfo("Time's Up!", "You ran out of time!")
        # End the round or take appropriate action

def reset_timer(window, timer_label):
    """Resets the timer to the initial value."""
    global timer_id
    if timer_id:
        window.after_cancel(timer_id)  # Stop the current timer
    start_timer(window, 10, timer_label)  # Restart the timer with 10 seconds

def animate_move(canvas, image, start_x, start_y, end_x, end_y):
    """Animates the movement of an image on the canvas."""
    step = 10  # Pixels to move per frame
    if start_x < end_x:
        canvas.move(image, step, 0)
        canvas.after(50, animate_move, canvas, image, start_x + step, start_y, end_x, end_y)
    elif start_y < end_y:
        canvas.move(image, 0, step)
        canvas.after(50, animate_move, canvas, image, start_x, start_y + step, end_x, end_y)

# ----- Window Functions -----

def show_loading():
    loading = tk.Toplevel(root)
    loading.geometry("400x200")
    loading.title("Loading...")
    set_background(loading, "background.png")  # Add background
    tk.Label(loading, text="Loading...", font=custom_font, bg="white").pack(pady=50)
    root.update()
    time.sleep(2)
    loading.destroy()
    show_main_menu()

def show_main_menu():
    main_menu = tk.Toplevel(root)
    main_menu.geometry("400x300")
    main_menu.title("Main Menu")
    set_background(main_menu, "background.png")  # Add background
    tk.Label(main_menu, text="Welcome to Rock, Paper, Scissors!", font=custom_font, bg="white").pack(pady=20)
    tk.Button(main_menu, text="Start the Game", font=custom_font, command=lambda: choose_game_mode(main_menu)).pack()

def choose_game_mode(prev_window):
    prev_window.destroy()
    mode_window = tk.Toplevel(root)
    mode_window.geometry("400x300")
    mode_window.title("Choose Game Mode")
    set_background(mode_window, "background.png")  # Add background
    tk.Label(mode_window, text="Select Mode:", font=custom_font, bg="white").pack(pady=20)
    tk.Button(mode_window, text="Player vs Player", font=custom_font, command=lambda: get_player_names(mode_window, "pvp")).pack(pady=10)
    tk.Button(mode_window, text="Player vs Computer", font=custom_font, command=lambda: get_player_names(mode_window, "pvc")).pack(pady=10)

def get_player_names(prev_window, selected_mode):
    prev_window.destroy()
    name_window = tk.Toplevel(root)
    name_window.geometry("400x300")
    name_window.title("Enter Names")
    set_background(name_window, "background.png")  # Add background
    tk.Label(name_window, text="Enter Player Name(s):", font=custom_font, bg="white").pack(pady=10)
    
    tk.Label(name_window, text="Player 1 Name:", bg="white").pack()
    player1_entry = tk.Entry(name_window)
    player1_entry.pack()
    
    if selected_mode == "pvp":
        tk.Label(name_window, text="Player 2 Name:", bg="white").pack()
        player2_entry = tk.Entry(name_window)
        player2_entry.pack()
    else:
        player2_entry = None
    
    tk.Button(name_window, text="Next", command=lambda: choose_rounds(name_window, selected_mode,
                                                                      player1_entry.get(),
                                                                      player2_entry.get() if player2_entry else "Computer")).pack(pady=10)

def choose_rounds(prev_window, selected_mode, p1, p2):
    prev_window.destroy()
    rounds_window = tk.Toplevel(root)
    rounds_window.geometry("400x300")
    rounds_window.title("Choose Rounds")
    set_background(rounds_window, "background.png")  # Add background
    tk.Label(rounds_window, text="Select Number of Rounds:", font=custom_font, bg="white").pack(pady=20)
    for rounds in [3, 5, 7]:
        tk.Button(rounds_window, text=f"{rounds} Rounds", font=custom_font,
                  command=lambda r=rounds: start_game(rounds_window, selected_mode, p1, p2, r)).pack(pady=5)

# ----- Game Window and Logic -----

def start_game(prev_window, selected_mode, p1, p2, rounds):
    global mode, player1_name, player2_name, total_rounds, current_round, score1, score2, current_turn, pvp_choice, images, game_window, timer_label
    mode = selected_mode
    player1_name = p1
    player2_name = p2
    total_rounds = rounds
    current_round = 1
    score1 = 0
    score2 = 0
    current_turn = "player1"
    pvp_choice = None
    
    prev_window.destroy()
    game_window = tk.Toplevel(root)
    game_window.geometry("600x500")
    game_window.title("Rock Paper Scissors")
    set_background(game_window, "background.png")  # Add background
    
    # Scoreboard Frame
    scoreboard_frame = tk.Frame(game_window, bg="white")
    scoreboard_frame.pack(pady=10)
    round_lbl = tk.Label(scoreboard_frame, text=f"Round: {current_round}/{total_rounds}", font=custom_font, bg="white")
    round_lbl.pack(side=tk.LEFT, padx=20)
    score_lbl = tk.Label(scoreboard_frame, text=f"{player1_name}: {score1}  -  {player2_name}: {score2}", font=custom_font, bg="white")
    score_lbl.pack(side=tk.LEFT, padx=20)
    
    # Timer Label
    timer_label = tk.Label(game_window, text="Time Left: 10", font=custom_font, bg="white")
    timer_label.pack(pady=5)
    start_timer(game_window, 10, timer_label)  # Start a 10-second timer
    
    # Turn indicator for PvP
    if mode == "pvp":
        turn_lbl = tk.Label(game_window, text=f"{player1_name}'s turn", font=custom_font, bg="white")
    else:
        turn_lbl = tk.Label(game_window, text=f"{player1_name}, choose your move", font=custom_font, bg="white")
    turn_lbl.pack(pady=5)
    
    # Load and reduce Images (adjust subsample factors as needed)
    images = {
        "rock": PhotoImage(file="rock.png").subsample(4, 4),  # Reduced size
        "paper": PhotoImage(file="paper.png").subsample(4, 4),  # Reduced size
        "scissors": PhotoImage(file="scissors.png").subsample(4, 4)  # Reduced size
    }
    
    # Frame for move buttons
    btn_frame = tk.Frame(game_window, bg="white")
    btn_frame.pack(pady=20)
    
    # Create buttons with images and labels
    for move in ["rock", "paper", "scissors"]:
        move_frame = tk.Frame(btn_frame, bg="white")
        move_frame.pack(side=tk.LEFT, padx=10)
        
        # Add image button
        tk.Button(move_frame, image=images[move],
                  command=lambda m=move: process_choice(m, score_lbl, round_lbl, turn_lbl, timer_label)).pack()
        
        # Add label below the image
        tk.Label(move_frame, text=move.capitalize(), font=custom_font, bg="white").pack()
    
    # Restart and Exit Buttons
    tk.Button(game_window, text="Restart", command=lambda: restart_game(game_window)).place(x=20, y=450)
    tk.Button(game_window, text="Exit", command=root.quit).place(x=520, y=450)

def process_choice(move, score_lbl, round_lbl, turn_lbl, timer_label):
    global mode, player1_name, player2_name, current_turn, pvp_choice, score1, score2, current_round, total_rounds
    # Reset the timer
    reset_timer(game_window, timer_label)
    
    # For Player vs Computer mode:
    if mode == "pvc":
        player_move = move
        computer_move = random.choice(["rock", "paper", "scissors"])
        winner = decide_winner(player_move, computer_move)
        msg = f"{player1_name} chose {player_move}\n{player2_name} chose {computer_move}\n"
        if winner == 0:
            msg += "It's a tie!"
        elif winner == 1:
            msg += f"{player1_name} wins this round!"
            score1 += 1
        else:
            msg += f"{player2_name} wins this round!"
            score2 += 1
        messagebox.showinfo("Round Result", msg)
        current_round += 1
        if current_round > total_rounds:
            show_final_result()
        else:
            round_lbl.config(text=f"Round: {current_round}/{total_rounds}")
            score_lbl.config(text=f"{player1_name}: {score1}  -  {player2_name}: {score2}")
    else:  # Player vs Player mode
        if current_turn == "player1":
            pvp_choice = move
            current_turn = "player2"
            turn_lbl.config(text=f"{player2_name}'s turn")
        else:
            player1_move = pvp_choice
            player2_move = move
            winner = decide_winner(player1_move, player2_move)
            msg = f"{player1_name} chose {player1_move}\n{player2_name} chose {player2_move}\n"
            if winner == 0:
                msg += "It's a tie!"
            elif winner == 1:
                msg += f"{player1_name} wins this round!"
                score1 += 1
            else:
                msg += f"{player2_name} wins this round!"
                score2 += 1
            messagebox.showinfo("Round Result", msg)
            current_turn = "player1"
            turn_lbl.config(text=f"{player1_name}'s turn")
            current_round += 1
            if current_round > total_rounds:
                show_final_result()
            else:
                round_lbl.config(text=f"Round: {current_round}/{total_rounds}")
                score_lbl.config(text=f"{player1_name}: {score1}  -  {player2_name}: {score2}")

def decide_winner(move1, move2):
    # Return 0 for tie, 1 if first move wins, 2 if second move wins.
    if move1 == move2:
        return 0
    elif (move1 == "rock" and move2 == "scissors") or \
         (move1 == "paper" and move2 == "rock") or \
         (move1 == "scissors" and move2 == "paper"):
        return 1
    else:
        return 2

def show_final_result():
    global game_window, score1, score2, player1_name, player2_name
    game_window.destroy()
    result_window = tk.Toplevel(root)
    result_window.geometry("400x300")
    result_window.title("Game Over")
    set_background(result_window, "background.png")  # Add background
    if score1 > score2:
        winner_text = f"{player1_name} wins the game!"
    elif score2 > score1:
        winner_text = f"{player2_name} wins the game!"
    else:
        winner_text = "The game is a tie!"
    tk.Label(result_window, text=winner_text, font=custom_font, bg="white").pack(pady=20)
    
    # Play winning sound if there's a clear winner
    if score1 != score2:
        try:
            pygame.mixer.music.load("win_sound.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print("Sound error:", e)
    tk.Button(result_window, text="Continue", command=lambda: end_game_screen(result_window)).pack(pady=20)

def end_game_screen(prev_window):
    prev_window.destroy()
    end_window = tk.Toplevel(root)
    end_window.geometry("400x300")
    end_window.title("End Game")
    set_background(end_window, "background.png")  # Add background
    tk.Label(end_window, text="End Game", font=custom_font, bg="white").pack(pady=30)
    tk.Button(end_window, text="Restart", command=lambda: restart_game(end_window)).pack(side=tk.LEFT, padx=50, pady=20)
    tk.Button(end_window, text="Exit", command=root.quit).pack(side=tk.RIGHT, padx=50, pady=20)

def restart_game(prev_window):
    prev_window.destroy()
    show_main_menu()

# ----- Main Application -----

root = tk.Tk()
root.withdraw()
show_loading()
root.mainloop()
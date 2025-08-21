# from game import Game
# from cache import GameCache
# import tkinter as tk

# if __name__ == "__main__":
    
#     cache = GameCache()

    
#     # Запуск игры
#     # game = Game(cache)
#     game = Game(tk.Tk(), cache)
#     game.load_state()
#     game.run()  
from game import Game
from cache import GameCache
import tkinter as tk
from tkinter import messagebox, ttk

def show_welcome(cache):
    """Показать приветственное окно с выбором действий"""
    welcome = tk.Tk()
    welcome.title("Крестики-нолики")
    welcome.geometry("300x200")
    welcome.configure(bg='white')
    welcome.resizable(False, False)
    
    welcome.eval('tk::PlaceWindow . center')
    
    saved_state = cache.load_state("game_001")
    has_saved_game = saved_state is not None
    
    font_style = ("T-FLEX Type A", 11)
    button_style = {'font': font_style, 'width': 15, 'height': 1}
    
    title = tk.Label(welcome, text="Крестики-нолики 10x10", 
                          font=("T-FLEX Type A", 14, "bold"), bg='white')
    title.pack(pady=20)
    
    # Кнопка новой игры
    new_game = tk.Button(welcome, text="Новая игра", 
                            command=lambda: start_new_game(welcome, cache),
                            **button_style)
    new_game.pack(pady=10)
    
    # Кнопка продолжить (только если есть сохраненная игра)
    if has_saved_game:
        continue_btn = tk.Button(welcome, text="Продолжить игру", 
                                command=lambda: continue_game(welcome, cache),
                                **button_style)
        continue_btn.pack(pady=10)
    else:
        # Заглушка если нет сохраненной игры
        disabled_btn = tk.Button(welcome, text="Нет игр", 
                                state="disabled", **button_style)
        disabled_btn.pack(pady=10)
    
    welcome.mainloop()

def start_new_game(welcome, cache):
    """Начать новую игру"""
    welcome.destroy()
    cache.r.delete("game:game_001")
    
    input = tk.Tk()
    input.title("Крестики-нолики")
    input.geometry("300x200")
    input.configure(bg='white')
    input.resizable(False, False)
    font_style = ("T-FLEX Type A", 11)
    
    player1_label=tk.Label(input, text="Игрок за крестики:", 
                          font=font_style, bg='white')
    player1_label.pack(pady=5)
    
    player1_entry = ttk.Entry(input,font=font_style, width=20 )
    player1_entry.pack(pady=5)
    player1_entry.insert(0, "Игрок 1")
    
    player2_label=tk.Label(input, text="Игрок за нолики:", 
                          font=font_style, bg='white')
    player2_label.pack(pady=5)
    
    player2_entry = ttk.Entry(input,font=font_style, width=20 )
    player2_entry.pack(pady=5)
    player2_entry.insert(0, "Игрок 2")
    input.eval('tk::PlaceWindow . center')
    
    
    # start_main_game(cache)
    

def continue_game(welcome, cache):
    welcome.destroy()
    start_main_game(cache)

def start_main_game(cache):
    root = tk.Tk()
    game = Game(root, cache)
    
    saved_state = cache.load_state("game_001")
    if saved_state:
        game.load_state()
    
    root.protocol("WM_DELETE_WINDOW", game.on_close)
    
    game.run()

if __name__ == "__main__":
    try:
        cache = GameCache()
        show_welcome(cache)
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
        # Если Redis недоступен, все равно показываем основное окно
        cache = GameCache()
        start_main_game(cache)
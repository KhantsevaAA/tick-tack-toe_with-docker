import time
import numpy as np
import tkinter as tk
from cache import GameCache
from tkinter import messagebox, font

class Game:
    def __init__(self, root, cache: GameCache, player1="Игрок 1", player2="Игрок 2"):
       
        self.start_time = time.time()
        self.cache = cache
        self.player1=player1
        self.player2=player2
        self.game_id = "game_001"
        self.k = 0 #счётчик ходов
        self.p = np.zeros((10, 10), dtype=int) #разметка игрового поля 10 на 10
        
        # Создание главного окна
        self.root = root
        self.root.title("Крестики-нолики 10Х10")
        self.root.geometry("550x550")
        self.root.configure(bg='white')
        self.root.resizable(False, False)  
        # self.root.eval('tk::PlaceWindow . center')
        self.root.update()
        self.create_window()
        
    def create_window(self):
        font1 = ("T-FLEX Type A", 11)
        
        self.label1 = tk.Label(self.root, text=f"{self.player1}: O", font=font1, bg='white')
        self.label1.place(x=10, y=10, anchor="nw")
        
        self.label2 = tk.Label(self.root, text=f"{self.player2}: X", font=font1, bg='white')
        self.label2.place(relx=1.0, x=-10, y=10, anchor="ne")
        
        self.label3 = tk.Label(self.root, text="Счёт\n0:0", font=font1, bg='white')
        self.label3.place(relx=0.5, y=30, anchor="center")
        
        self.button1 = tk.Button(self.root, text="Сбросить счёт", font=font1, 
                                command=self.reset_score, width=12)
        self.button1.place(rely=1.0, x=10, y=-10, anchor="sw")
        self.button2 = tk.Button(self.root, text="Новая игра", font=font1, 
                                command=self.new_game, width=12)
        self.button2.place(rely=1.0,relx=1.0, x=-10, y=-10, anchor="se")
        
        #вычисление размера поля
        self.l=self.root.winfo_height()-2*self.label1.winfo_reqheight()-self.button1.winfo_reqheight()-10*4 
        self.canvas = tk.Canvas(self.root, bg='light gray', width=self.l,
                                height=self.l)
        self.canvas.place(relx=0.5,y=10+2*self.label1.winfo_reqheight(),  anchor="n")
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.draw_board()
        
    def draw_board(self):
        self.canvas.delete("all")
        cell_size = self.l / 10
        
        for i in range(1, 10):
            self.canvas.create_line(
                i * cell_size, 0,
                i * cell_size, self.l,
                fill='black'
            )
            self.canvas.create_line(
                0, i * cell_size,
                self.l, i * cell_size,
                fill='black'
            )
            
        for i in range(10):
            for j in range(10):
                if self.p[i, j] == -1:
                    self.draw_o(i, j)
                elif self.p[i, j] == 1:
                    self.draw_x(i, j)
                    
    def mouse_click(self, event):
        cell_size = self.l / 10
        x = int(event.x // cell_size)
        y = int(event.y // cell_size)

        if 0 <= x < 10 and 0 <= y < 10 and self.p[x, y] == 0:
            if self.k % 2 == 0:
                self.p[x, y] = -1
                self.draw_o(x, y)
            else:
                self.p[x, y] = 1
                self.draw_x(x, y)
                
            self.save_state()
            self.k += 1
            if self.k >= 9:  
                self.check_win()   
    
    def check_win(self):
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1)  # Горизонталь, вертикаль, диагонали
        ]

        for i in range(10):
            for j in range(10):
                if self.p[i, j] == 0:
                    continue

                for dx, dy in directions:
                    count = 1
                    # Проверка в одном направлении
                    for step in range(1, 5):
                        ni, nj = i + dx * step, j + dy * step
                        if not (0 <= ni < 10 and 0 <= nj < 10):
                            break
                        if self.p[ni, nj] != self.p[i, j]:
                            break
                        count += 1

                    # # Проверка в обратном направлении
                    # for step in range(1, 5):
                    #     ni, nj = i - dx * step, j - dy * step
                    #     if not (0 <= ni < 10 and 0 <= nj < 10):
                    #         break
                    #     if self.p[ni, nj] != self.p[i, j]:
                    #         break
                    #     count += 1

                    if count >= 5:
                        cell_size = self.l / 10
                        self.canvas.create_line(
                            (i+0.5)*cell_size,
                            (j+0.5)*cell_size,
                            (i+dx*4.5+0.5-0.5*dx)*cell_size,
                            (j+dy*4.5+0.5-0.5*dy)*cell_size,
                            width=2,
                            fill='green'
                        )
                        print(i, j, dx, dy)
                        self.win(i, j, dx, dy)
                        return

        # Проверка на ничью
        if np.all(self.p != 0):
            messagebox.showinfo("Партия закончена", "Ничья!")
            self.new_game()
                             
    def draw_o(self, x, y):
        cell_size = self.l / 10
        padding = cell_size * 0.2
        self.canvas.create_oval(
            x * cell_size + padding,
            y * cell_size + padding,
            (x + 1) * cell_size - padding,
            (y + 1) * cell_size - padding,
            width=2,
            outline='red'
        )  
                      
    def draw_x(self, x, y):
        cell_size = self.l / 10
        padding = cell_size * 0.2
        self.canvas.create_line(
            x * cell_size + padding,
            y * cell_size + padding,
            (x + 1) * cell_size - padding,
            (y + 1) * cell_size - padding,
            width=2,
            fill='blue'
        )
        self.canvas.create_line(
            x * cell_size + padding,
            (y + 1) * cell_size - padding,
            (x + 1) * cell_size - padding,
            y * cell_size + padding,
            width=2,
            fill='blue'
        )
        
    def win(self, x, y, dx, dy):
        # Обновление счета
        score = self.label3.cget("text").split()
        player1_score = int(score[1].split(':')[0])
        player2_score = int(score[1].split(':')[1])

        if self.p[x, y] == -1:  # Игрок 1 (O)
            player1_score += 1
            winner = "Игрок 1"
        else:  # Игрок 2 (X)
            player2_score += 1
            winner = "Игрок 2"

        self.label3.config(text=f"Счёт\n{player1_score}:{player2_score}")
        messagebox.showinfo("Партия закончена", f"{winner} выиграл!")
        self.new_game()

    def reset_score(self):
        self.label3.config(text="Счёт\n0:0")
        self.new_game()

    def new_game(self):
        self.p = np.zeros((10, 10), dtype=int)
        self.k = 0
        self.start_time = time.time()
        self.draw_board()
        self.save_state()
        

    def save_state(self):
        state = {
            'board': self.p.tolist(), #матрица заполнения поля
            'k': self.k, # номер хода
            'score': self.label3.cget("text"), #счёт
            'start_time': self.start_time 
        }
        # self.cache.save_state(self.game_id, state)
        self.cache.save_game(self.game_id, self.player1, self.player2, state)
        
        # self.event_handler.publish('game_state_saved', {
        #     'game_id': self.game_id,
        #     'timestamp': time.time()
        # })

    def load_state(self):
        """Загрузка состояния игры из кеша"""
        # state = self.cache.load_state(self.game_id)
        players, state = self.cache.load_game(self.game_id)
        
        if state:
            try:
                self.p = np.array(state['board'])
                self.k = state['k']
                self.label3.config(text=state['score'])
                self.start_time = state.get('start_time', time.time())
                self.draw_board()
                self.player1=players['name1']
                self.player2=players['name2']
                self.label1.config(text=f"{self.player1}: O")
                self.label2.config(text=f"{self.player2}: X")
                
                # Показываем сообщение о успешной загрузке
                messagebox.showinfo("Загрузка", "Предыдущая игра успешно загружена!")
                
            except (KeyError, ValueError, TypeError) as e:
                print(f"Ошибка загрузки состояния: {e}")
                messagebox.showerror("Ошибка", "Не удалось загрузить сохраненную игру")
                self.new_game()
        else:
            messagebox.showinfo("Новая игра", "Начинаем новую игру!")
            # self.event_handler.publish('game_state_loaded', {
            #     'game_id': self.game_id,
            #     'timestamp': time.time()
            # })

    def on_close(self):
        # self.save_state()
        self.root.destroy()

    def run(self):
        """Запуск главного цикла приложения"""
        self.root.mainloop()
    
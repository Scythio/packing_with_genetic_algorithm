#!/usr/bin/env python
# encoding: utf-8
import tkinter as tk
import random

class Item():
    def __init__(self,width,height,number,color,x=0,y=0):
        self.width = width
        self.height = height
        self.number = number
        self.color = color
        self.x = x
        self.y = y


class Application(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.master = master
        self.controller = controller
        self.pack()

        self.MAX_STORAGE_WIDTH = 200
        self.MAX_STORAGE_HEIGHT = 200
        self.MAX_ITEM_WIDTH = 50
        self.MAX_ITEM_HEIGHT = 50
        self.MAX_SIM_LEN = 200
        self.MAX_MU = 100
        self.MAX_LAM = 400
        self.item_list = []
        self.storage_width = self.MAX_STORAGE_WIDTH/2
        self.storage_height = self.MAX_STORAGE_HEIGHT/2
        self.space = 0
        self.chromosome = tk.StringVar('')
        self.progress = tk.StringVar('')
        self.fullness = tk.StringVar('')
        self.color_list = ['azure', 'sky blue', 'steel blue', 'cyan', 'aquamarine',
                           'sea green', 'pale green', 'lime green', 'yellow', 'gold',
                           'indian red', 'sandy brown', 'salmon', 'orange', 'tomato',
                           'light pink', 'violet red', 'hot pink', 'royal blue',  'blue violet']

        self.create_widgets()
        self.setup()

    def create_widgets(self):

        self.menu_frame = tk.Frame(self.master, bg='black',highlightthickness=1)
        self.menu2_frame = tk.Frame(self.master, bg='black',highlightthickness=1,highlightbackground='black')
        self.content_frame = tk.Frame(self.master, bg='black')

        self.storage_label = tk.Label(self.menu_frame,text='\nSTORAGE',bg='black',fg='light grey',font='16')
        self.storage_width_scale = tk.Scale(self.menu_frame, from_=10, to=self.MAX_STORAGE_WIDTH,
                                            orient='horizontal', length=200, label='width',
                                            command=self.update_storage, bg='black', fg='light grey',highlightthickness=0)
        self.storage_width_scale.set(self.MAX_STORAGE_WIDTH/2)
        self.storage_height_scale = tk.Scale(self.menu_frame, from_=10, to=self.MAX_STORAGE_HEIGHT,
                                            orient='horizontal', length=200, label='height',
                                            command=self.update_storage, bg='black', fg='light grey',highlightthickness=0)
        self.storage_height_scale.set(self.MAX_STORAGE_HEIGHT/2)
        self.space_scale = tk.Scale(self.menu_frame, from_=0, to=10, orient='horizontal',
                                    length=200, label='spacing',
                                    command=self.update_space,
                                    bg='black', fg='light grey', highlightthickness=0)
        self.space_scale.set(0)

        self.item_label = tk.Label(self.menu_frame, text='\nITEM', bg='black', fg='light grey', font='16')
        self.item_width_scale = tk.Scale(self.menu_frame, from_=10, to=self.MAX_ITEM_WIDTH, orient='horizontal',
                                            length=200, label='width',
                                            bg='black', fg='light grey', highlightthickness=0)
        self.item_width_scale.set(self.MAX_ITEM_WIDTH/2)
        self.item_height_scale = tk.Scale(self.menu_frame, from_=10, to=self.MAX_ITEM_HEIGHT, orient='horizontal',
                                             length=200, label='height',
                                             bg='black', fg='light grey',
                                             highlightthickness=0)
        self.item_height_scale.set(self.MAX_ITEM_HEIGHT/2)

        self.storage_canvas = tk.Canvas(self.content_frame,height=self.MAX_STORAGE_HEIGHT+40,
                                        width=self.MAX_STORAGE_WIDTH+100,bg='black', highlightthickness=0)
        self.item_list_canvas = tk.Canvas(self.content_frame,height=(self.MAX_STORAGE_HEIGHT+100)*4,
                                          width=(self.MAX_STORAGE_WIDTH+100)*2, bg='black', highlightthickness=0)
        self.chromosome_label = tk.Label(self.content_frame, bg='black', fg='light gray',font=('TkDefaultFont', 14),
                                         wraplength=(self.MAX_STORAGE_WIDTH+100)*2, highlightthickness=1, textvariable=self.chromosome)

        self.run_button = tk.Button(self.menu2_frame, text='RUN', command=self.run_genetic_algorithm, bg='black', fg='tomato', pady=10, width=20)
        self.add_item_button = tk.Button(self.menu_frame, text='ADD ITEM', command=self.add_item,
                                         bg ='black', fg='light grey', pady=10, width =20)
        self.generate_item_list_button = tk.Button(self.menu_frame, text='GENERATE ITEMS',
                                                   command=self.generate_item_list,
                                                   bg ='black', fg='light grey', pady=10, width =20)
        self.clear_item_list_button = tk.Button(self.menu_frame, text='CLEAR ITEMS',
                                                   command=self.clear_item_list,
                                                   bg='black', fg='light grey', pady=10, width=20)

        self.sim_label = tk.Label(self.menu2_frame, text='\nALGORITHM', bg='black', fg='light grey', font='16')
        self.sim_len_scale = tk.Scale(self.menu2_frame, from_=1, to=self.MAX_SIM_LEN, orient='horizontal',
                                             length=200, label='iterations',
                                             bg='black', fg='light grey',
                                             highlightthickness=0)
        self.sim_len_scale.set(int(self.MAX_SIM_LEN / 4))
        self.sim_mu_scale = tk.Scale(self.menu2_frame, from_=1, to=self.MAX_MU,
                                                               orient='horizontal',
                                                               length=200, label='mu',
                                                               bg='black', fg='light grey',
                                                               highlightthickness=0)
        self.sim_mu_scale.set(int(self.MAX_MU / 4))
        self.sim_lam_scale = tk.Scale(self.menu2_frame, from_=1, to=self.MAX_LAM,
                                                               orient='horizontal',
                                                               length=200, label='lam',
                                                               bg='black', fg='light grey',
                                                               highlightthickness=0)
        self.sim_lam_scale.set(int(self.MAX_LAM / 4))
        self.warning_label = tk.Label(self.menu2_frame, text='\nmu must be lesser than lambda', bg='black', fg='light grey', font=('TkDefaultFont', 8))

        self.progress_label = tk.Label(self.menu2_frame, textvariable=self.progress, bg='black', fg='light grey')
        self.fullness_label = tk.Label(self.menu2_frame, textvariable=self.fullness, bg='black', fg='light grey')

    def setup(self):
        self.menu2_frame.pack(side='right', fill='both')
        self.menu_frame.pack(side='right', fill='both')
        self.content_frame.pack(side='left', expand=True, fill='both')

        self.sim_label.pack(side='top')
        self.sim_len_scale.pack(side='top')
        self.sim_mu_scale.pack(side='top')
        self.sim_lam_scale.pack(side='top')
        self.warning_label.pack(side='top')
        self.progress_label.pack(side='top')
        self.fullness_label.pack(side='top')

        self.storage_label.pack(side='top')
        self.storage_width_scale.pack(side='top')
        self.storage_height_scale.pack(side='top')
        self.space_scale.pack(side='top')
        self.storage_canvas.pack(side='top')
        self.chromosome_label.pack(side='top')
        self.item_list_canvas.pack(side='top')

        self.item_label.pack(side='top')
        self.item_width_scale.pack(side='top')
        self.item_height_scale.pack(side='top')

        self.clear_item_list_button.pack(side='bottom')
        self.generate_item_list_button.pack(side='bottom')
        self.add_item_button.pack(side='bottom')

        self.run_button.pack(side='bottom')

    def add_item(self):
        color = random.choice(self.color_list)
        width=self.item_width_scale.get()
        height=self.item_height_scale.get()
        number=len(self.item_list)
        self.item_list.append(Item(width,height,number,color))
        self.update_item_list()

    def generate_item_list(self):
        storage_area = self.storage_width_scale.get()*self.storage_height_scale.get()
        items_area = 0
        for item in self.item_list:
            items_area += item.width*item.height
        while items_area < storage_area:
            width = random.randint(10, self.MAX_ITEM_WIDTH)
            height = random.randint(10, self.MAX_ITEM_HEIGHT)
            items_area += width*height
            number = len(self.item_list)
            color = random.choice(self.color_list)
            self.item_list.append(Item(width,height,number,color))
        self.update_item_list()

    def clear_item_list(self):
        self.item_list = []
        self.update_item_list()

    def run_genetic_algorithm(self):

        if len(self.item_list) > 1:
            if self.sim_mu_scale.get() < self.sim_lam_scale.get():
                self.turn_off_menu()
                self.controller.run_sim()
            else:
                self.warning_label.config(fg='tomato')
        # pub.sendMessage("Run_Button_Pressed")

    def turn_off_menu(self):
        self.storage_label.config(fg='grey')
        self.item_label.config(fg='grey')
        self.item_width_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.item_height_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.storage_width_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.storage_height_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.space_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.sim_label.config(fg='grey')
        self.sim_mu_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.sim_lam_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.sim_len_scale.config(state='disabled', troughcolor='grey', fg='grey')
        self.warning_label.config(fg='gray')
        self.add_item_button.config(state='disabled')
        self.generate_item_list_button.config(state='disabled')
        self.clear_item_list_button.config(state='disabled')
        self.run_button.config(state='disabled')

    def turn_on_menu(self):
        self.storage_label.config(fg='light grey')
        self.item_label.config(fg='light grey')
        self.item_width_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.item_height_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.storage_width_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.storage_height_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.space_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.sim_label.config(fg='light grey')
        self.sim_mu_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.sim_lam_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.sim_len_scale.config(state='normal', troughcolor='light grey', fg='light grey')
        self.warning_label.config(fg='light gray')
        self.add_item_button.config(state='normal')
        self.generate_item_list_button.config(state='normal')
        self.clear_item_list_button.config(state='normal')
        self.run_button.config(state='normal')

    def update_storage(self, arg2=None):

        self.storage_width = self.storage_width_scale.get()
        self.storage_height = self.storage_height_scale.get()
        self.storage_canvas.delete('all')
        x1 = (self.MAX_STORAGE_WIDTH + 100) / 2 - self.storage_width_scale.get()/2
        y1 = (self.MAX_STORAGE_HEIGHT + 40) / 2 - self.storage_height_scale.get()/2
        x2 = (self.MAX_STORAGE_WIDTH + 100) / 2 + self.storage_width_scale.get()/2
        y2 = (self.MAX_STORAGE_HEIGHT + 40) / 2 + self.storage_height_scale.get()/2
        self.storage_canvas.create_rectangle(x1,y1,x2,y2,fill='light grey')

    def update_space(self, arg2=None):
        self.space = self.space_scale.get()

    def update_chromosome(self, chromosome):
        self.chromosome.set(str(chromosome))

    def update_progress(self, progress):
        txt = '\nProgress: '+str(progress)+'%'
        self.progress.set(txt)

    def update_fullness(self, fullness):
        txt = '\nFullness: '+str(fullness)+'%'
        self.fullness.set(txt)

    def update_item_list(self):
        self.item_list_canvas.delete('all')
        X = 20
        Y = 40
        for item in self.item_list:
            x1 = X + self.MAX_ITEM_WIDTH / 2 - item.width / 2
            y1 = Y + self.MAX_ITEM_HEIGHT / 2 - item.height / 2
            x2 = X + self.MAX_ITEM_WIDTH / 2 + item.width / 2
            y2 = Y + self.MAX_ITEM_HEIGHT / 2 + item.height / 2
            self.item_list_canvas.create_rectangle(x1,y1,x2,y2,fill=item.color)
            self.item_list_canvas.create_text(X+(self.MAX_ITEM_WIDTH)/2,Y-5,text=item.number, fill='light grey')
            X += self.MAX_ITEM_WIDTH
            if X >= (self.MAX_STORAGE_WIDTH+100)*2 - self.MAX_ITEM_WIDTH:
                X = 20
                Y += self.MAX_ITEM_HEIGHT + 20

    def do_nothing(self, arg2):
        pass

    def get_init_values(self):
        return self.item_list

    def draw_solution(self, item_list):
        self.update_storage()
        X = (self.storage_canvas.winfo_width() - self.storage_width) / 2
        Y = (self.storage_canvas.winfo_height() + self.storage_height) / 2
        for item in item_list:
            x1 = X + item.x
            y1 = Y - item.y
            x2 = x1 + item.width
            y2 = y1 - item.height
            self.storage_canvas.create_rectangle(x1, y1, x2, y2, fill=item.color)
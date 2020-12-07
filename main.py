#!/usr/bin/env python
# encoding: utf-8
import tkinter as tk
import gui
import Model2 as model

class Controller:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x600')
        self.root.title('Packing with Genetic Algorithm')
        self.view = gui.Application(master=self.root,controller=self)

    def run_sim(self):
        pack_list, container, sim_len, mu, lam, spacing = self.get_init_values()
        self.population = model.Population(self, pack_list, container, sim_len, mu, lam, spacing)
        self.population.run()
        self.view.turn_on_menu()

    def get_init_values(self):
        cw = self.view.storage_width
        ch = self.view.storage_height
        space = self.view.space
        container = model.Rect(cw,ch)
        pack_list = []
        sim_len = self.view.sim_len_scale.get()
        mu = self.view.sim_mu_scale.get()
        lam = self.view.sim_lam_scale.get()
        for item in self.view.item_list:
            w = item.width+2*space
            h = item.height+2*space
            n = item.number
            c = item.color
            pack_list.append(model.Rect(w,h,n,c))
        return pack_list, container, sim_len, mu, lam, space

    def draw_solution(self, best_one,t,sim_len,container):
        space = self.view.space
        solution = best_one.packed_list.copy()
        item_list = []
        for item in solution:
            w = item.width - 2 * space
            h = item.height - 2 * space
            n = item.number
            c = item.color
            x = item.left_x + space
            y = item.bottom_y + space
            item_list.append(gui.Item(w, h, n, c, x, y))
        progress = (t / sim_len) * 100
        progress = round(progress, 2)
        fullness = (best_one.value / container.area) * 100
        fullness = round(fullness, 2)
        self.view.update_progress(progress)
        self.view.update_fullness(fullness)
        self.view.update_chromosome(best_one.chromosome)
        self.view.draw_solution(item_list)
        self.view.update()

if __name__ == '__main__':
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()

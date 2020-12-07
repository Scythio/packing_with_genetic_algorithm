#!/usr/bin/env python
# encoding: utf-8
import random
import copy

class Rect:

    def __init__(self, a, b, number = -1, color='white'):
        self.width = a
        self.height = b
        self.area = a*b
        self.left_x = 0
        self.right_x = self.width
        self.top_y = self.height
        self.bottom_y = 0
        self.number = number
        self.color = color

    def set_position(self, pos_x, pos_y):
        self.left_x = pos_x
        self.right_x = pos_x + self.width
        self.top_y = pos_y + self.height
        self.bottom_y = pos_y

    def change_size(self, w, h):
        self.width = w
        self.height = h
        self.right_x = self.left_x + self.width
        self.top_y = self.bottom_y + self.height
        self.area = self.width * self.height

    def check_collision(self, rect):
        collision_x = bool(self.right_x > rect.left_x and self.left_x < rect.right_x)
        collision_y = bool(self.top_y > rect.bottom_y and self.bottom_y < rect.top_y)
        if collision_x and collision_y:
            return True
        else:
            return False

    def __str__(self):
        string = 'n: '+ str(self.number) +', w: ' +str(self.width) +', h: '+ str(self.height)\
                      + ', lx:' + str(self.left_x) + ', by:' +str(self.bottom_y) + ', rx:'\
                      + str(self.right_x) + ', ty:' +str(self.top_y)
        return string

class Subject:
    def __init__(self, chromosome, pack_list_in, container, spacing):
        # N = Number of Items to be put in Storage = Number of Gens in Chromosome
        self.N = len(pack_list_in)
        if chromosome == [] or chromosome is None:
            self.chromosome = self.create_chromosome(self.N)
        else:
            self.chromosome = chromosome.copy()
        self.pack_list = self.pack_list_in_order(pack_list_in, self.chromosome)
        self.container = container
        self.free_space_list = []
        self.free_space_list.append(container)
        self.packed_list = []
        self.spacing = spacing
        self.value = self.calc_value()


    def pack_list_in_order(self, pack_list, chromosome):

        packs = pack_list.copy()
        pack_list_in_order = []
        for gen in chromosome:
            pack_list_in_order.append(packs[gen])

        return pack_list_in_order

    def calc_value(self):
        i = 0
        self.free_space_list = [self.container]
        self.packed_list = []
        packed_area = 0
        packs = self.pack_list.copy()
        while self.put_rect(packs[i]) and i < (len(packs) - 1):
            i += 1

        for rect in self.packed_list:
            packed_area += (rect.width-2*self.spacing)*(rect.height-2*self.spacing)

        return packed_area

        # TODO  może nie?

    def create_chromosome(self,n):
        items = []
        chromosome = []
        for i in range(n):
            items.append(i)
        while len(items) > 0:
            i = random.randint(0,len(items)-1)
            chromosome.append(items.pop(i))
        return chromosome

    def mutate(self):
        n = len(self.chromosome)
        nm = self.number_of_mutations()
        new_chromosome = self.chromosome.copy()
        for i in range(nm):
            n1 = random.randint(0,n-1)
            n2 = random.randint(0,n-1)
            while n1 == n2:
                n2 = random.randint(0,n-1)
            item_number1 = new_chromosome[n1]
            item_number2 = new_chromosome[n2]
            new_chromosome[n1] = item_number2
            new_chromosome[n2] = item_number1
        return new_chromosome


    def number_of_mutations(self):
        nm = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,4,4,5]
        # P(1) = 40%
        # P(2) = 30%
        # P(3) = 15%
        # P(4) = 10%
        # P(5) = 5%
        return random.choice(nm)

    def put_rect(self, pack):

        success = False

        #PROBA UMIESZCZENIA PROSTOKATA
        for space in self.free_space_list:
            if success is False and pack.width <= space.width and pack.height <= space.height:
                pack.set_position(space.left_x, space.bottom_y)
                self.packed_list.append(pack)

                success = True

                new_free_space_1 = Rect(space.width - pack.width, space.height)
                new_free_space_1.set_position(space.left_x + pack.width, space.bottom_y)

                new_free_space_2 = Rect(space.width, space.height - pack.height)
                new_free_space_2.set_position(space.left_x, space.bottom_y + pack.height)

                self.free_space_list.remove(space)
                self.free_space_list.append(new_free_space_1)
                self.free_space_list.append(new_free_space_2)

        #SZUKANIE KOLIZJI
        for space in self.free_space_list:
            if pack.check_collision(space):
                if pack.left_x <= space.left_x and pack.bottom_y <= space.bottom_y:
                    space.change_size(0, 0)
                elif pack.left_x > space.left_x:
                    space.change_size(pack.left_x - space.left_x, space.height)
                elif pack.bottom_y > space.bottom_y:
                    space.change_size(space.width, pack.bottom_y - space.bottom_y)

        #USUWANIE PUSTYCH PÓL
        for space in self.free_space_list:
            if space.area == 0:
                self.free_space_list.remove(space)

        #SORTOWANIE WOLNYCH PRZESTRZENI
        sort = True
        while sort is True:
            sort = False
            i = 0
            while i < len(self.free_space_list) - 1:
                if self.free_space_list[i].bottom_y > self.free_space_list[i + 1].bottom_y:
                    sort_item = self.free_space_list[i]
                    self.free_space_list[i] = self.free_space_list[i + 1]
                    self.free_space_list[i + 1] = sort_item
                    sort = True
                elif self.free_space_list[i].bottom_y == self.free_space_list[i + 1].bottom_y and self.free_space_list[
                    i].left_x > self.free_space_list[i + 1].left_x:
                    sort_item = self.free_space_list[i]
                    self.free_space_list[i] = self.free_space_list[i + 1]
                    self.free_space_list[i + 1] = sort_item
                    sort = True
                i += 1

        return success

    def __str__(self):
        return str(self.chromosome)

class Population():
    def __init__(self, controller, packlist, container, sim_len=200, mu=20, lam=140, spacing=0):
        self.controller = controller
        self.packlist  = packlist
        self.container = container
        self.spacing = spacing
        self.sim_len = sim_len
        self.t = 0
        self.mu = mu
        self.lam = lam
        self.parent_list = []
        self.offspring_list = []
        for i in range(mu):
            new_subject = Subject([],self.packlist,self.container,self.spacing)
            self.parent_list.append(new_subject)


    def run(self):
        while self.t < self.sim_len:
            self.t += 1
            self.offspring_list = []
            parents = self.parent_list.copy()
            for i in range(self.lam):
                parent = copy.deepcopy(random.choice(parents))
                new_chromosome = parent.mutate()
                packs = copy.deepcopy(self.packlist)
                offspring = Subject(new_chromosome,packs,self.container,self.spacing)
                self.offspring_list.append(offspring)
            NEXT = self.offspring_list + parents
            NEXT = sorted(NEXT, key=lambda x: x.value, reverse=True)
            if self.mu < self.lam:
                self.parent_list = NEXT[0:self.mu]
            else:
                self.parent_list = NEXT.copy()
            best_one = self.parent_list[0]
            self.controller.draw_solution(best_one,self.t,self.sim_len,self.container)
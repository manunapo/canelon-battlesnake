import random
from logic.gridgraph import GridGraph

MODE_RANDOM = 0
MODE_EAT = 1
MODE_CHASE_MY_TAIL = 2

# Possible mode to implement
MODE_CHASE_ENEMY_TAIL = 3

HEALTH_TRESHOLD = 100

'''
    Update: Canelon Will go for good all time

    Canelon cat move randomly.
    Canelon will eat only when its health treshold went less than HEALTH_TRESHOLD
    Canelon will chase THE NEIGHBORS of his tail when he is not hungry if it is set.
        Why chase tail's neighbors instead of the tail itself? 
            Because of how i have implemented the relation between the nodes, if the node is not available (nor food nor empty), it will not
            be neighbor of no other node.
            Here would be nice to decide which of the neighbor nodes could be a better choise 

    Finally, if there is not any path or possible good move. Canelon will take a random move.

    The A* algorithm is used to find a path to food or this tail's neighbors
        There are two improvement still needed for the graph/nodes:
            - Add a herusitic function (now it is hardcoded to 1 for all nodes)
            - Potencially add a weight to every neighbor, now all jumps to neighbors are 1
    
'''

class LogicHandler():

    def __init__(self,board_height,board_width):
        self.gg = GridGraph(board_height,board_width)
        self.health = 100
        #self.mode = MODE_CHASE_MY_TAIL
        self.mode = MODE_EAT
        self.turn = 0

    def load_turn(self, data):
        food = data['board']['food']
        my_snake = data['you']
        enemy_snakes = []
        self.turn = data["turn"]
        for snake in data['board']['snakes']:
            if snake["id"] != my_snake["id"]:
                enemy_snakes.append(snake)
        self.gg.update_grid(my_snake,enemy_snakes,food)
        
        '''
        if my_snake['health'] <= HEALTH_TRESHOLD:
            self.mode = MODE_EAT
        elif self.turn >= 3:
            self.mode = MODE_CHASE_MY_TAIL
        else:
            self.mode = MODE_RANDOM
        '''

    def pos_to_move(self,fx,fy,tx,ty):
        if ((fx == tx) and (fy+1 == ty)): return "up"
        if ((fx == tx) and (fy-1 == ty)): return "down"
        if ((fx+1 == tx) and (fy == ty)): return "right"
        if ((fx-1 == tx) and (fy == ty)): return "left"
        return ""

    def search_test(self):
        for tentative_tail,weight in self.gg.my_snake_tail.get_neighbors():
            self.gg.a_star_algorithm(self.gg.my_snake_head, tentative_tail)

    def search_food(self):
        closest_path_to_food = []
        shortest_length = 9999
        new_path = []
        for tentative_food in self.gg.the_food:
            new_path = self.gg.a_star_algorithm(self.gg.my_snake_head, tentative_food)
            if (len(new_path) < shortest_length):
                closest_path_to_food = new_path
                shortest_length = len(new_path)
        fx = self.gg.my_snake_head.x
        fy = self.gg.my_snake_head.y
        if (len(closest_path_to_food) > 1):
            tx = closest_path_to_food[1].x
            ty = closest_path_to_food[1].y
        else:
            return ""
        return self.pos_to_move(fx,fy,tx,ty)

    def search_my_tail(self):
        longest_path_to_tail = []
        longest_length = 0
        new_path = []
        for tentative_tail,weigth in self.gg.my_snake_tail.get_neighbors():
            if tentative_tail.is_crossable():
                new_path = self.gg.a_star_algorithm(self.gg.my_snake_head, tentative_tail)
                if (len(new_path) > longest_length):
                    longest_path_to_tail = new_path
                    longest_length = len(new_path)
        fx = self.gg.my_snake_head.x
        fy = self.gg.my_snake_head.y
        if (len(longest_path_to_tail) > 1):
            tx = longest_path_to_tail[1].x
            ty = longest_path_to_tail[1].y
        else:
            return ""
        return self.pos_to_move(fx,fy,tx,ty)

    def print_grid(self):
        self.gg.aux_print_grid()

    def has_potencial_collision(self):
        # to work on
        # we have 8 potencial position to look at
        # need to check if we can win the collision or not
        pass

    def find_move_with_most_space(self):
        print(f"INFO - Finding the longest path to be safe")
        size = 0
        biggest_path = []
        for neig,w in self.gg.my_snake_head.get_neighbors():
            path = self.gg.get_free_path(neig)
            if len(path) > size:
                size = len(path)
                biggest_path = path
        fx = self.gg.my_snake_head.x
        fy = self.gg.my_snake_head.y
        if (len(biggest_path) > 1):
            tx = biggest_path[0].x
            ty = biggest_path[0].y
        else:
            return ""
        return self.pos_to_move(fx,fy,tx,ty)

    def calculate_move(self,possible_moves):
        print(f"Calculating move with these parameters:")
        print(f"MODE: {self.mode}")
        print(f"possible_moves: {possible_moves}")
        next_move = ""
        if len(possible_moves) > 1:
            has_potencial_collision = False
            if has_potencial_collision:
                # To implement
                print(f"INFO - has_potencial_collision")
            elif (self.mode == MODE_EAT):
                print(f"INFO - Searching food")
                next_move = self.search_food()
                if not next_move:
                    next_move = self.find_move_with_most_space()
                
            elif (self.mode == MODE_CHASE_MY_TAIL):
                next_move = self.search_my_tail()
                if not next_move:
                    next_move = self.find_move_with_most_space()
                print(f"INFO - Chasing my tail")
            elif (self.mode == MODE_RANDOM):
                next_move = random.choice(possible_moves)

        if not next_move and (len(possible_moves) > 0):
            next_move = random.choice(possible_moves)
            print(f"INFO - Going random")
        print(f"Move Calculated to: {next_move}")
        return next_move
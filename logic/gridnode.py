
NODE_WEIGHT = 1

class GridNode():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.types = {
            0: "empty",
            1: "my_snake",
            2: "my_head",
            3: "enemy_snake",
            4: "enemy_head",
            5: "food",
            6: "my_tail"
        }
        self.type = 0
        self.neighbors = []

        # workaround to store the snake length/size in his head node
        # usefull for collisions
        self.snake_length = 3

    def __hash__(self):
        return hash((self.x, self.y ))

    def __eq__(self, other):
        if other == None:
            return False
        return (self.x, self.y) == (other.x, other.y)

    def __str__(self):
        return f"({self.x},{self.y})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def is_empty(self):
        return self.type == 0

    def is_my_snake(self):
        return self.type == 1

    def is_my_head(self):
        return self.type == 2

    def is_enemy_snake(self):
        return self.type == 3

    def is_enemy_head(self):
        return self.type == 4

    def is_food(self):
        return self.type == 5


    def is_crossable(self):
        return self.is_empty() or self.is_food()
    

    def to_empty(self):
        self.type = 0
    
    def to_my_snake(self):
        self.type = 1
    
    def to_my_head(self):
        self.type = 2

    def to_enemy_snake(self):
        self.type = 3

    def to_enemy_head(self):
        self.type = 4

    def to_food(self):
        self.type = 5

    def to_my_tail(self):
        self.type = 6
 
    
    def add_neighbor(self,grid_node):
        self.neighbors.append((grid_node,NODE_WEIGHT))

    def get_neighbors(self):
        return self.neighbors


    def get_type(self):
        return self.type

    def set_snake_length(self,length):
        self.snake_length = length

    def get_snake_length(self):
        return self.snake_length
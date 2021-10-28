from logic.gridnode import GridNode
 
class GridGraph:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.my_snake_head = None
        self.my_snake_tail = None
        self.the_food = []
        self.grid = [ [ GridNode(x,y) for y in range(height) ] for x in range(width) ]
 
    def update_grid(self,my_snake,enemy_snakes,food):
        [ [ self.grid[x][y].to_empty() for y in range(self.height) ] for x in range(self.width) ]
        for part in my_snake["body"]:
            self.grid[part['x']][part['y']].to_my_snake()
        self.my_snake_head = self.grid[my_snake["body"][0]['x']][my_snake["body"][0]['y']]
        self.my_snake_tail = self.grid[my_snake["body"][-1]['x']][my_snake["body"][-1]['y']]
        self.my_snake_head.to_my_head()

        for snake in enemy_snakes:
            for part in snake["body"]:
                self.grid[part['x']][part['y']].to_enemy_snake()
            self.my_enemy_head = self.grid[snake["body"][0]['x']][snake["body"][0]['y']]
            self.my_enemy_head.to_enemy_head()

        for f in food:
            self.the_food.append(self.grid[f['x']][f['y']])
            self.grid[f['x']][f['y']].to_food()
        counter = 0

        # Add neighbors which are not obtacles nor edges
        for y in range(self.height):
            for x in range(self.width):
                if ((x + 1) < self.width) and (self.grid[x+1][y].is_crossable()):
                    self.grid[x][y].add_neighbor(self.grid[x+1][y])
                    counter += 1
                if ((x - 1) >= 0) and (self.grid[x-1][y].is_crossable()):
                    self.grid[x][y].add_neighbor(self.grid[x-1][y])
                    counter += 1
                if ((y + 1) < self.height) and (self.grid[x][y+1].is_crossable()):
                    self.grid[x][y].add_neighbor(self.grid[x][y+1])
                    counter += 1
                if ((y - 1) >= 0) and (self.grid[x][y-1].is_crossable()):
                    self.grid[x][y].add_neighbor(self.grid[x][y-1])
                    counter += 1
                # print(f"For {x},{y} - added {counter} neig")
                counter = 0
       
    def get_neighbors(self, grid_node):
        return grid_node.get_neighbors()

    # This is heuristic function which is having equal values for all nodes
    def heuristic(self, n):
        return 1
 
    def a_star_algorithm(self, start, stop):
        # In this open_lst is a lisy of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, It starts off with the start 
  #node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])
 
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
 
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start
 
        while len(open_lst) > 0:
            n = None
 
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.heuristic(v) < poo[n] + self.heuristic(n):
                    n = v
 
            if n == None:
                print('AFF - Path does not exist!')
                return []
 
            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []
 
                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]
 
                reconst_path.append(start)
 
                reconst_path.reverse()
 
                for step in reconst_path:
                    print(f" - {step.x},{step.y}")
                # print('Path found: {}'.format(reconst_path))
                return reconst_path
 
            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
              # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight
 
                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n
 
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)
 
            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)
 
        print('AFF - Path does not exist!')
        return []
from typing import List, Dict

from logic.logichandler import LogicHandler
"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_edges(my_head: Dict[str, int], board_height, board_width, possible_moves: List[str]) -> List[str]:
    if my_head["x"] == 0:
        possible_moves.remove("left")
    if (board_width - 1) == my_head["x"]:
        possible_moves.remove("right")
    if my_head["y"] == 0:
        possible_moves.remove("down")
    if (board_height - 1) == my_head["y"]:
        possible_moves.remove("up")
    return possible_moves

def body_has_coordinate(my_body: List[dict], x, y) -> bool:
    for coord in my_body:
        if coord["x"] == x and coord["y"] == y:
            return True
    return False

def avoid_self_body(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    for move in possible_moves:
        if (move == "up"):
            if body_has_coordinate(my_body, my_head["x"], my_head["y"] + 1):
                possible_moves.remove("up")
        elif (move == "down"):
            if body_has_coordinate(my_body, my_head["x"], my_head["y"] - 1):
                possible_moves.remove("down")
        elif (move == "left"):
            if body_has_coordinate(my_body, my_head["x"] - 1, my_head["y"]):
                possible_moves.remove("left")
        elif (move == "right"):
            if body_has_coordinate(my_body, my_head["x"] + 1, my_head["y"]):
                possible_moves.remove("right")
    return possible_moves

def avoid_other_snakes(my_head: Dict[str, int], enemy_snakes: List[dict], possible_moves: List[str]) -> List[str]:
    for snake in enemy_snakes:
        b_snake = snake["body"][1:len(snake["body"])]
        for move in possible_moves:
            if (move == "up"):
                if body_has_coordinate(b_snake, my_head["x"], my_head["y"] + 1):
                    possible_moves.remove("up")
            elif (move == "down"):
                if body_has_coordinate(b_snake, my_head["x"], my_head["y"] - 1):
                    possible_moves.remove("down")
            elif (move == "left"):
                if body_has_coordinate(b_snake, my_head["x"] - 1, my_head["y"]):
                    possible_moves.remove("left")
            elif (move == "right"):
                if body_has_coordinate(b_snake, my_head["x"] + 1, my_head["y"]):
                    possible_moves.remove("right")
    return possible_moves 

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes tail this turn is: {my_body[-1]}")

    possible_moves = ["up", "down", "left", "right"]

    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    board_height = data['board']['height']
    board_width = data['board']['width']

    possible_moves = avoid_edges(my_head, board_height, board_width, possible_moves)

    possible_moves = avoid_self_body(my_head, my_body, possible_moves)
    
    snakes = data['board']['snakes']
    possible_moves = avoid_other_snakes(my_head, snakes, possible_moves)
    
    '''
    food = data['board']['food']

    my_snake = data['you']
    enemy_snakes = []
    for snake in snakes:
        if snake['id'] != my_snake['id']:
            enemy_snakes.append(snake)

    #gg = GridGraph(board_height,board_width)
    #gg.update_grid(my_snake,enemy_snakes,food)
    #gg.a_star_algorithm(gg.my_snake_head, gg.the_food[0])
    '''

    lh = LogicHandler(board_height,board_width)
    lh.load_turn(data)
    #lh.search_test()

    move = lh.calculate_move(possible_moves)

    return move
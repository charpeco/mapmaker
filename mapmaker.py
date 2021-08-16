#TO DO: make it throw out maps that use too many nodes on the borderline.

import numpy as np
import sys
from numpy import random

class node:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.valid_moves = []

    def move_down(self):
        self.coordinates = self.coordinates[0] + 1, self.coordinates[1]

    def move_up(self):
        self.coordinates = self.coordinates[0] - 1, self.coordinates[1]

    def move_right(self):
        self.coordinates = self.coordinates[0], self.coordinates[1] + 1

    def move_left(self):
        self.coordinates = self.coordinates[0], self.coordinates[1] - 1

class region:
    def __init__(self, compass_point):
        self.compass_point = compass_point
        self.region_map = np.zeros((10, 10), dtype=int)
        self.used_coordinates = set()
        self.important_nodes = {}
        self.region_maker()

    def mover(self, startpoint, endpoint, modifier):
        starting_node = node(startpoint.coordinates)
        self.region_map[starting_node.coordinates] = modifier
        while starting_node.coordinates != endpoint:
            if starting_node.coordinates[1] < endpoint[1]:
                starting_node.valid_moves.append(starting_node.move_right)
            else:
                starting_node.valid_moves.append(starting_node.move_left)
            if starting_node.coordinates[0] < endpoint[0]:
                starting_node.valid_moves.append(starting_node.move_down)
            else:
                starting_node.valid_moves.append(starting_node.move_up)
            while starting_node.coordinates != endpoint:
                if (
                    starting_node.coordinates[1] == endpoint[1]
                    and starting_node.move_down in starting_node.valid_moves
                    ):
                    starting_node.move_down()
                    self.region_map[starting_node.coordinates] += modifier
                    self.used_coordinates.add(starting_node.coordinates)
                elif (
                    starting_node.coordinates[1] == endpoint[1] and
                    starting_node.move_up in starting_node.valid_moves
                    ):
                    starting_node.move_up()
                    self.region_map[starting_node.coordinates] += modifier
                    self.used_coordinates.add(starting_node.coordinates)
                elif (
                    starting_node.coordinates[0] == endpoint[0]
                    and starting_node.move_left in starting_node.valid_moves
                    ):
                    starting_node.move_left()
                    self.region_map[starting_node.coordinates] += modifier
                    self.used_coordinates.add(starting_node.coordinates)
                elif (
                    starting_node.coordinates[0] == endpoint[0]
                    and starting_node.move_right in starting_node.valid_moves
                    ):
                    starting_node.move_right()
                    self.region_map[starting_node.coordinates] += modifier
                    self.used_coordinates.add(starting_node.coordinates)
                else:
                    move = starting_node.valid_moves[random.randint(2)]
                    move()
                    self.region_map[starting_node.coordinates] += modifier
                    self.used_coordinates.add(starting_node.coordinates)

    def boss_finder(self):
        global boss_coordinate
        global used_coordinates
        global important_nodes
        boss_coordinate = node((random.randint(3, 7), random.randint(3, 7)))
        self.region_map[boss_coordinate.coordinates] = 1
        self.important_nodes["boss_coordinate"] = boss_coordinate.coordinates
        self.used_coordinates.add(boss_coordinate.coordinates)

    def draw_first_path(self):
        coordinate_found = False
        while coordinate_found == False:
            first_border_picker = random.randint(10)
            if (abs(first_border_picker - self.important_nodes["boss_coordinate"][0]) < 2
                or abs(first_border_picker - self.important_nodes["boss_coordinate"][1]) < 2
                ):
                pass
            else:
                global first_border
                global used_coordinates
                if self.compass_point == "north":
                    first_border = node((self.region_map.shape[0] - 1, first_border_picker))
                    self.used_coordinates.add(first_border.coordinates)
                    coordinate_found = True
                elif self.compass_point == "south":
                    first_border = node((0, first_border_picker))
                    self.used_coordinates.add(first_border.coordinates)
                    coordinate_found = True
                elif self.compass_point == "west":
                    first_border = node((first_border_picker, self.region_map.shape[0] - 1))
                    self.used_coordinates.add(first_border.coordinates)
                    coordinate_found = True
                elif self.compass_point == "east":
                    first_border = node((first_border_picker, 0))
                    self.used_coordinates.add(first_border.coordinates)
                    coordinate_found = True
        self.region_map[first_border.coordinates] += 2
        self.important_nodes["first_border"] = first_border.coordinates
        self.mover(first_border, self.important_nodes["boss_coordinate"], 2)

    def draw_second_path(self):
        coordinate_found = False
        while coordinate_found == False:
            second_border_picker = random.randint(10)
            if (
                abs(self.important_nodes["first_border"][0] - second_border_picker) < 2
                or abs(self.important_nodes["first_border"][1] - second_border_picker) < 2
                ):
                pass
            else:
                global second_border
                global used_coordinates
                if self.compass_point == "north":
                    second_border = node((self.region_map.shape[0] - 1, second_border_picker))
                    self.used_coordinates.add(second_border.coordinates)
                    coordinate_found = True
                elif self.compass_point == "south":
                    second_border = node((0, second_border_picker))
                    self.used_coordinates.add(second_border.coordinates)
                    coordinate_found = True
                elif self.compass_point == "west":
                    second_border = node((second_border_picker, self.region_map.shape[0] - 1))
                    self.used_coordinates.add(second_border.coordinates)
                    coordinate_found = True
                elif self.compass_point == "east":
                    second_border = node((second_border_picker, 0))
                    self.used_coordinates.add(second_border.coordinates)
                    coordinate_found = True
                self.region_map[second_border.coordinates] = 3
                coordinate_found = True
        destination_found = False
        while destination_found == False:
            valid_destinations = list(i for i in self.used_coordinates if i != self.important_nodes["boss_coordinate"] and i != self.important_nodes["boss_coordinate"])
            destination_index = random.randint(0, len(valid_destinations))
            destination = node(valid_destinations[destination_index])
            if (
                (destination.coordinates[0] == 9 or destination.coordinates[0] == 8)
                and (self.compass_point == "north" or self.compass_point == "south")
                ):
                pass
            elif (
                (destination.coordinates[1] == 9 or destination.coordinates[1] == 8)
                and (self.compass_point == "east" or self.compass_point == "west")
                ):
                pass
            else:
                destination_found = True
        self.used_coordinates.add(second_border.coordinates)
        self.important_nodes["second_border"] = second_border.coordinates
        self.region_map[destination.coordinates] = 3
        self.mover(second_border, destination.coordinates, 3)

    def draw_third_and_fourth_path(self):
        coordinate_found = False
        while coordinate_found == False:
            random_coordinate = random.randint(9), random.randint(9)
            if self.region_map[random_coordinate] != 0:
                pass
            else:
                global third_path_end
                global used_coordinates
                self.region_map[random_coordinate] += 4
                third_path_end = node(random_coordinate)
                self.used_coordinates.add(third_path_end.coordinates)
                coordinate_found = True
        destination_found = False
        while destination_found == False:
            random_coordinate = random.randint(9), random.randint(9)
            if (
                random_coordinate == third_path_end.coordinates
                or random_coordinate not in self.used_coordinates
                ):
                pass
            else:
                destination = random_coordinate
                destination_found = True
        self.mover(third_path_end, destination, 4)
        coordinate_found = False
        while coordinate_found == False:
            random_coordinate = random.randint(9), random.randint(9)
            if self.region_map[random_coordinate] != 0:
                pass
            else:
                global fourth_path_end
                self.region_map[random_coordinate] += 5
                fourth_path_end = node(random_coordinate)
                self.used_coordinates.add(fourth_path_end.coordinates)
                coordinate_found = True
        destination_found = False
        while destination_found == False:
            random_coordinate = random.randint(9), random.randint(9)
            if (
                random_coordinate == fourth_path_end.coordinates
                or random_coordinate not in self.used_coordinates
                ):
                pass
            else:
                destination = random_coordinate
                destination_found = True
        self.mover(fourth_path_end, destination, 5)
        self.region_map[self.important_nodes["boss_coordinate"]] = 1

    def map_checker(self):
        global used_coordinates
        global region_map
        throw_out = False
        one_border = 0
        two_border = 0
        three_border = 0
        four_border = 0
        used_coordinates_list = list(self.used_coordinates)
        bad_coordinates_list = []
        for coordinate in used_coordinates_list:
            if coordinate[0] < 0 or coordinate[1] < 0:
                self.used_coordinates_list.remove(coordinate)
        for coordinate in used_coordinates_list:
            border_count = 0
            if (coordinate[0] - 1, coordinate[1]) in used_coordinates_list:
                border_count += 1
            if (coordinate[0] + 1, coordinate[1]) in used_coordinates_list:
                border_count += 1
            if (coordinate[0], coordinate[1] - 1) in used_coordinates_list:
                border_count += 1
            if (coordinate[0], coordinate[1] + 1) in used_coordinates_list:
                border_count += 1
            if coordinate == self.important_nodes["boss_coordinate"] and border_count < 3:
                throw_out = True
            if border_count == 0:
                bad_coordinates_list.append(coordinate)
            elif border_count == 1:
                one_border += 1
            elif border_count == 2:
                two_border += 1
            elif border_count == 3:
                three_border += 1
            else:
                four_border += 1
                self.important_nodes[f"four_border_{four_border}"] = coordinate
        for coordinate in bad_coordinates_list:
            used_coordinates_list.remove(coordinate)
            self.region_map[coordinate] = 0
        self.used_coordinates = set(used_coordinates_list)
        if (
            len(used_coordinates_list) > 30
            or len(used_coordinates_list) < 20
            or four_border < 2
            or four_border > 3
            or two_border > len(used_coordinates_list) / 2
            ):
            throw_out = True
        if throw_out == True:
            self.region_map = np.zeros((10, 10), dtype=int)
            self.used_coordinates = set()
            self.important_nodes = {}
            self.boss_finder()
            self.draw_first_path()
            self.draw_second_path()
            self.draw_third_and_fourth_path()
            self.map_checker()
        else:
            print(self.region_map)
            print(f"""This is the {self.compass_point}ern region.
The boss node should be {self.important_nodes["boss_coordinate"]}
The borders are {self.important_nodes["first_border"]} and {self.important_nodes["second_border"]}
The four-border nodes are {list(value for key, value in self.important_nodes.items() if "four_border" in key)}
{one_border} nodes have one border.
{two_border} nodes have two borders.
{three_border} nodes have three borders.
{four_border} nodes have four borders.
{len(self.used_coordinates)} nodes have been used.""")

    def region_maker(self):
            self.boss_finder()
            self.draw_first_path()
            self.draw_second_path()
            self.draw_third_and_fourth_path()
            self.map_checker()

def spam_region_maker(compass_point):
    count = 0
    global region_map
    while count < 1000:
        region_maker(compass_point)
        region_map = np.zeros((10, 10), dtype=int)
        used_coordinates.clear()
        count += 1

def world_maker():
    global north
    global south
    global east
    global west
    north = region("north")
    south = region("south")
    east = region("east")
    west = region("west")
    return north

def spam_world_maker():
    count = 0
    global region_map
    while count < 1000:
        world_maker()
        print(count)
        count += 1

spam_world_maker()

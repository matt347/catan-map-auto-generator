import math

# start(q1, r1) --> end(q1, r1)
def distance(start, end):
    x1, y1 = axial_to_xy(start)
    x2, y2 = axial_to_xy(end)
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 3)

def axial_to_xy(coord):
    q, r = coord
    return (math.sqrt(3))/2 * r, q + r/2

def get_tier(val):
    return 6 - abs(7 - val) if val > 0 else 0

def get_neighbors(board_map, coord):
    directions = [(-1, 1), (0, 1), (1, 0), (1, -1), (0, -1), (-1, 0)]
    neighbors = []
    x, y = coord
    for dir_x, dir_y in directions:
        if (dir_x + x, dir_y + y) in board_map:
            neighbors.append((dir_x + x, dir_y + y))
    return neighbors

def find_index(board_map, list_to_search, item_to_find):
    item_found_inds = []
    for key, val in board_map.items():
        if list_to_search[board_map[key].index] == item_to_find:
            item_found_inds.append(board_map[key].index)
    return item_found_inds

def find_coords(board_map, list_to_search, item_to_find):
    item_found_coords = []
    for key, val in board_map.items():
        if list_to_search[board_map[key].index] == item_to_find:
            item_found_coords.append(key)
    return item_found_coords

def print_board(coord_list, resources, numbers, board_score, width, max_width):
    print("\n==================================================================")
    print("Map Score: {}".format(board_score))
    a, b = 0, 0
    for i in range(len(coord_list)):
        if b == 0:
            print("        " * (abs(a - (max_width - width))), end="")
        #print("{} [{},{}]".format(coord_list[i], resources[i], numbers[i]), end="   ")
        print("{}, {}".format(resources[i], numbers[i]), end="         ")
        b += 1
        if b == max_width - abs(a - (max_width - width)):
            a += 1
            b = 0
            if i != len(coord_list)-1:
                print("\n\n")
            else:
                print("\n")
    print(resources)
    print(numbers)
    print("==================================================================")


    # need to sort by scores in descending order
    # candidate_maps = []
    # for i in range(50):
    #     resources, numbers = initialize(board_map, coord_list, inner_list, high_tier_centralize, desert_center)
    #     if resources is not None and numbers is not None:
    #         current_score = 0
    #         current_score += score_resource_dist_arrangement(board_map, resources)
    #         current_score += resource_to_number_ratio(board_map, resources, numbers)
    #         cand = Candidate(resources, numbers, current_score)
    #         candidate_maps.append(cand)
    # ordered_candidate_maps = sorted(candidate_maps, key=lambda c: c.score, reverse=True)
    # for ordered_cand in ordered_candidate_maps:
    #     print("Score:", ordered_cand.score)
    # return ordered_candidate_maps[0].resources, ordered_candidate_maps[0].numbers
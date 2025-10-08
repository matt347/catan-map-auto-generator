# ooooooh boyeeee we doin this again!!!

import CatanMapHelper
import random

# ill do a bunch of random resource lists and use the one with the best dist average,
# best port to resource and most balanced tier to resource avg
class Candidate:
    def __init__(self, resources, numbers, score):
        self.resources = resources
        self.numbers = numbers
        self.score = score

class BoardTile:
    def __init__(self, index):
        self.index = index
        self.ports = []

class resourceTile:
    def __init__(self, type, count):
        self.type = type
        self.count = count
        self.tier_avg = 0

class PortTile:
    def __init__(self, left_port, right_port, type):
        self.left_port = [left_port, left_port]
        self.right_port = right_port
        self.type = type

def add_low_tier(board_map, coord_list, numbers, empty_neighbor):
    low_tier_neighbors = CatanMapHelper.get_neighbors(board_map, coord_list[empty_neighbor])
    for neighbor_cand in low_tier_neighbors:
        if numbers[board_map[neighbor_cand].index] in [2, 3, 11, 12]:
            return False
    return True

def add_high_tier(coord_list, selected_inds, pick, desert_ind):
    if pick == desert_ind:
        return False
    for i in range(len(selected_inds)):
        if CatanMapHelper.distance(coord_list[selected_inds[i]], coord_list[pick]) < 1.73:
            return False
    return True

def choose_low_tier_ind(board_map, coord_list, numbers, low_tier_num_list, pick, desert_target_coord):
    neighbors = CatanMapHelper.get_neighbors(board_map, coord_list[pick])
    neighbors_inds, empty_neighbor_inds = [], []
    for neighbor in neighbors:
        neighbors_inds.append(board_map[neighbor].index)
        if numbers[board_map[neighbor].index] == 0 and coord_list[board_map[neighbor].index] != desert_target_coord:
            empty_neighbor_inds.append(board_map[neighbor].index)
    random.shuffle(empty_neighbor_inds)
    for empty_neighbor in empty_neighbor_inds:
        if add_low_tier(board_map, coord_list, numbers, empty_neighbor):
            numbers[empty_neighbor] = low_tier_num_list.pop()
            break

def choose_high_tier_ind(coord_list, numbers, high_tier_num_list, selected_inds, range_inds, desert_ind):
    for i in range(len(range_inds)-1, -1, -1):
        pick = range_inds[i]
        if add_high_tier(coord_list, selected_inds, pick, desert_ind):
            pick = range_inds.pop(i)
            selected_inds.append(pick)
            numbers[pick] = high_tier_num_list.pop()
            return pick
    return None

def balance_clusters(board_map, coord_list, numbers, high_tier_num_list, low_tier_num_list, high_clusters, desert_target_coord):
    for i in range(10):
        for cluster in high_clusters:
            choose_low_tier_ind(board_map, coord_list, numbers, low_tier_num_list, cluster, desert_target_coord)
        if len(low_tier_num_list) == 0 and len(high_tier_num_list) == 0:
            return True
        else:
            for i in range(len(numbers)):
                if numbers[i] not in [6, 8]:
                    numbers[i] = 0
            low_tier_num_list = [2, 3, 11, 12]
    return False

def balance_board(board_map, coord_list, numbers, med_tier_num_list, desert_target_coord):
    while len(med_tier_num_list) > 0:
        adjacency_scores, adjacency_score_inds = [], []
        for i in range(len(coord_list)):
            if numbers[i] == 0 and coord_list[i] != desert_target_coord:
                neighbors = CatanMapHelper.get_neighbors(board_map, coord_list[i])
                neighbors.append(coord_list[i])
                adj_score = 0
                for neighbor in neighbors:
                        adj = CatanMapHelper.get_tier(numbers[board_map[neighbor].index])
                        if adj < 3:
                            adj -= 3
                        adj_score += adj
                adjacency_scores.append(round(adj_score / len(neighbors),1))
                adjacency_score_inds.append(i)
        lowest_adj = 0
        min = 100
        for i in range(len(adjacency_scores)):
            if adjacency_scores[i] < min:
                min = adjacency_scores[i]
                lowest_adj = adjacency_score_inds[i]
        numbers[lowest_adj] = med_tier_num_list.pop()

def spread_same_tiers(coord_list, numbers):
    num_tier_list = [[3,11], [4,10], [5,9]]
    for i in range(len(num_tier_list)):
        tier = num_tier_list[i]
        t_range = []
        for i in range(len(coord_list)):
            if numbers[i] in tier:
                t_range.append(i)
                numbers[i] = -1
        min_dist = 100
        min_pair = (0,0)
        t1_count = (len(t_range)//2)
        t2_count = (len(t_range)//2)
        t1_list, t2_list = [], []
        for i in range(len(t_range)):
            for j in range(i+1, len(t_range)):
                dist = CatanMapHelper.distance(coord_list[t_range[i]], coord_list[t_range[j]])
                if dist < min_dist:
                    min_dist = dist
                    min_pair = (i, j)
        numbers[t_range[min_pair[0]]] = tier[0]
        numbers[t_range[min_pair[1]]] = tier[1]
        t1_list.append(t_range[min_pair[0]])
        t2_list.append(t_range[min_pair[1]])
        t_range[min_pair[0]] = -5
        t_range[min_pair[1]] = -5

        for i in range(len(t_range)):
            if t_range[i] != -5:
                dist1, dist2 = 0,0
                if len(t1_list) < t1_count:
                    for j in range(len(t1_list)):
                        dist1 += CatanMapHelper.distance(coord_list[t_range[i]], coord_list[t1_list[j]])
                if len(t2_list) < t2_count:
                    for j in range(len(t2_list)):
                        dist2 += CatanMapHelper.distance(coord_list[t_range[i]], coord_list[t2_list[j]])
                if dist1 >= dist2 and dist1 != 0:
                    t1_list.append(t_range[i])
                elif dist2 >= dist1 and dist2 != 0:
                    t2_list.append(t_range[i])
                else:
                    return None, None
        for i in range(len(t1_list)):
            numbers[t1_list[i]] = tier[0]
            numbers[t2_list[i]] = tier[1]

def spread_resources(coord_list, desert_ind):
    # store amount of times we have seen resource and avg tier?
    resources = []
    resources += ["Wood"] * 2
    resources += ["Wheat"] * 2
    resources += ["Sheep"] * 2
    resources += ["Brick"]
    resources += ["Rock"]
    resources += ["abc"] * 10
    random.shuffle(resources)
    resources.insert(desert_ind, "Desert")

    resource_inds = dict()
    for i in range(len(resources)):
        if resources[i] not in resource_inds:
            resource_inds[resources[i]] = [i]
        else:
            resource_inds[resources[i]].append(i)

    for i in range(len(resource_inds["abc"])):
        rs_dist_max = -1
        rs_pick = "x"
        for rs in ["Wood", "Wheat", "Sheep", "Brick", "Rock"]:
            rs_max = 3 if rs in ["Brick", "Rock"] else 4
            if len(resource_inds[rs]) < rs_max:
                d = 0
                for j in range(len(resource_inds[rs])):
                    d += CatanMapHelper.distance(coord_list[resource_inds["abc"][i]], coord_list[resource_inds[rs][j]])
                d /= (len(resource_inds[rs])+1)
                if d > rs_dist_max:
                    rs_dist_max = d
                    rs_pick = rs
        resource_inds[rs_pick].append(resource_inds["abc"][i])
        resources[resource_inds["abc"][i]] = rs_pick
    return resources

def initialize(board_map, coord_list, inner_list, high_tier_centralize, desert_center):
    numbers = [0] * len(coord_list)
    high_tier_num_list = [6,6,8,8]
    low_tier_num_list = [2,3,11,12]
    med_tier_num_list = [3,11,4,4,10,10,5,5,9,9]
    random.shuffle(high_tier_num_list)
    random.shuffle(low_tier_num_list)
    selected_inds, inner_inds, all_inds = [], [], []
    inner_high_tier_count = random.randint(1, len(high_tier_num_list)//2) if high_tier_centralize else 0

    desert_ind = 0
    desert_target_coord = (0,0)
    if not desert_center:
        while desert_target_coord == (0,0):
            desert_target_coord = random.choice(coord_list)
    if high_tier_centralize:
        for i in range(len(coord_list)):
            if coord_list[i] in inner_list:
                inner_inds.append(i)
        random.shuffle(inner_inds)
    for i in range(len(coord_list)):
        if coord_list[i] == desert_target_coord:
            desert_ind = i
        all_inds.append(i)
    random.shuffle(all_inds)

    resources = spread_resources(coord_list, desert_ind)

    high_clusters = []
    for i in range(inner_high_tier_count):
        pick = choose_high_tier_ind(coord_list, numbers, high_tier_num_list, selected_inds, inner_inds, desert_ind)
        if pick is not None:
            high_clusters.append(pick)
    while len(high_tier_num_list) > 0:
        pick = choose_high_tier_ind(coord_list, numbers, high_tier_num_list, selected_inds, all_inds, desert_ind)
        if pick is not None:
            high_clusters.append(pick)

    if not balance_clusters(board_map, coord_list, numbers, high_tier_num_list, low_tier_num_list, high_clusters, desert_target_coord):
        return None, None
    balance_board(board_map, coord_list, numbers, med_tier_num_list, desert_target_coord)
    spread_same_tiers(coord_list, numbers)

    # now check if any neighbors share the same number, if so return None, None
    for i in range(len(coord_list)):
        neighbors = CatanMapHelper.get_neighbors(board_map, coord_list[i])
        nbs = []
        for neighbor in neighbors:
            nbs.append(numbers[board_map[neighbor].index])
        if numbers[i] in nbs:
            return None, None

    return resources, numbers


def score_resource_dist_arrangement(board_map, resources):
    total_distance_sum = 0
    avg_distance_sum = 0
    for rs in ["Wood", "Wheat", "Sheep", "Brick", "Rock"]:
        resource_inds = CatanMapHelper.find_coords(board_map, resources, rs)
        resource_total_distance = 0
        for ind1 in range(len(resource_inds)):
            for ind2 in range(ind1 + 1, len(resource_inds)):
                dist = CatanMapHelper.distance(resource_inds[ind1], resource_inds[ind2])
                resource_total_distance += dist
        resource_avg_distance = resource_total_distance / len(resource_inds)
        total_distance_sum += resource_total_distance
        avg_distance_sum += resource_avg_distance
    return avg_distance_sum

def resource_to_number_ratio(board_map, resources, numbers):
    ratio_score = 0
    for rs in ["Wood", "Wheat", "Sheep", "Brick", "Rock"]:
        resource_inds = CatanMapHelper.find_index(board_map, resources, rs)
        non_duplicate_numbers_of_resource = []
        for ind in resource_inds:
            if numbers[ind] not in non_duplicate_numbers_of_resource:
                non_duplicate_numbers_of_resource.append(numbers[ind])
            else:
                ratio_score -=5
    return ratio_score

def create_map(board_map, coord_list, inner_list, high_tier_centralize, desert_center):
    resources, numbers = [], []
    current_score, attempts = 0, 0
    target_score = 16.8
    if not desert_center:
        target_score = 16.55
    while current_score < target_score:
        current_score = 0
        attempts += 1
        resources, numbers = initialize(board_map, coord_list, inner_list, high_tier_centralize, desert_center)
        if resources is not None and numbers is not None:
            current_score += score_resource_dist_arrangement(board_map, resources)
            current_score += resource_to_number_ratio(board_map, resources, numbers)
        if attempts % 1000 == 0:
            print("attempt: {}".format(attempts))
        if attempts > 30000:
            return None, None, None
    return resources, numbers, current_score

def available_ports(ports):
    port = []
    while len(ports) > 0:
        current_port = ports[0]
        if current_port.right_port is not None:
            if len(port) == 0:
                port.append(current_port.right_port)
                current_port.right_port = None
            return port
        elif len(current_port.left_port) == 2:
            port.append(current_port.left_port.pop(0))
            return port
        elif len(current_port.left_port) == 1:
            port.append(current_port.left_port.pop(0))
        ports.pop(0)
    return port

def spawn_grid(ports, width, max_width):
    # creates the board with axial coords set
    board_map = dict()
    coord_list, perimeter_list, buffer = [], [], []
    index = 0
    for i in range(0, 2 * (max_width - width) + 1):
        x = -(max_width // 2)
        y = max_width - width - i
        if i > (2 * (max_width - width) + 1) // 2:
            x += (i - (2 * (max_width - width) + 1) // 2)
        x_start = x
        for j in range(0, max_width - abs(i - (max_width - width))):
            board_map[(x, y)] = BoardTile(index)
            coord_list.append((x, y))
            if i == 0:
                perimeter_list.append((x,y))
            elif i == 2 * (max_width - width):
                buffer.append((x,y))
            x += 1
            index += 1
        if i != 0 and i != 2 * (max_width - width):
            perimeter_list.append((x-1, y))
            buffer.append((x_start, y))
    perimeter_list += reversed(buffer)
    for (x,y) in perimeter_list:
        board_map[(x,y)].ports = available_ports(ports)
    inner_list = []
    for i in coord_list:
        if i not in perimeter_list:
            inner_list.append(i)
    return board_map, coord_list, inner_list, perimeter_list

# test cases: (width, max_width) --> (1,4), (3,5), (5,6)
def startup(width, max_width, board_type):
    ports = []
    if board_type == "Standard":
        ports = [PortTile("Wheat","3:1","Normal"), PortTile("Rock",None,"Normal"),
                 PortTile("Sheep","3:1","Normal"), PortTile("3:1",None,"Normal"),
                 PortTile("Brick","3:1","Normal"), PortTile("Wood",None,"Normal")]
        width = 3
        max_width = 5
    elif board_type == "Expansion":
        # ports go as such: normal, normal, single, normal, single, normal, normal, single, normal, single
        width = 3
        max_width = 6
    else:
        while width < 1:
            width = int(input("Enter perimeter hex length (radius): "))
        while max_width <= width:
            max_width = int(input("Enter max hex length (diameter): "))
    return ports, width, max_width


# board map is a map of (x,y) --> index, port
if __name__ == "__main__":
    board_type = "Standard"
    width = 0
    max_width = 0
    high_tier_centralize = True
    desert_center = True
    ports, width, max_width = startup(width, max_width, board_type)
    board_map, coord_list, inner_list, perimeter_list = spawn_grid(ports, width, max_width)
    # high_tier_centralize = True means a more even spread of 6s/8s
    resources, numbers, board_score = create_map(board_map, coord_list, inner_list, high_tier_centralize, desert_center)
    if resources is not None and numbers is not None:
        CatanMapHelper.print_board(coord_list, resources, numbers, board_score, width, max_width)
    else:
        print("Wow. That is unlucky. The randomness used to create the board was inconsistent. Try again")

# also can check if number distribution per resource is balanced, but i might just leave it how it is
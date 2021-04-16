class Graph:
    def __init__(self):
        self.vertices = dict()
        self.vertex_amount = 0

    def add_vertex(self, key):
        self.vertex_amount += 1
        self.vertices[key] = Vertex(key)

    def add_edge(self, f, t, cost=0):
        if f not in self.vertices:
            self.add_vertex(f)
        if t not in self.vertices:
            self.add_vertex(t)
        self.vertices[f].add_neighbor(self.vertices[t], cost)

    def get_vertex(self, key):
        if key in self.vertices:
            return self.vertices[key]
        else:
            raise IndexError(f"W grafie nie ma wierzchołka o kluczu {key}")

    def get_starting_vertices(self):
        result = list(self.vertices.keys())
        loop_list = result.copy()
        for key in loop_list:
            temp = self.get_vertex(key)
            for i in temp.connected.keys():
                if i.key in result:
                    result.remove(i.key)
        return result

    def breadth_first_search(self, start_key, search_key):
        if start_key == search_key:
            return self.get_vertex(start_key)

        queue = []
        searched = {self.get_vertex(start_key)}
        for i in self.get_vertex(start_key).connected.keys():
            queue.append(i)
            searched.add(i)

        while True:
            if queue:
                temp = queue.pop(0)
                if temp.key == search_key:
                    return temp
                else:
                    searched.add(temp)
                    for i in temp.connected.keys():
                        if i not in searched:
                            queue.append(i)
            else:
                return None

    def depth_first_search(self, start_key, search_key):
        if start_key == search_key:
            return self.get_vertex(start_key)
        stack = []
        searched = {self.get_vertex(start_key)}
        for i in self.get_vertex(start_key).connected.keys():
            stack.append(i)
            searched.add(i)

        while True:
            if stack:
                temp = stack.pop()
                if temp.key == search_key:
                    return temp
                else:
                    searched.add(temp)
                    for i in temp.connected.keys():
                        if i not in searched:
                            stack.append(i)
            else:
                return None

    def topology_sort(self):
        result = ""
        for start_key in self.get_starting_vertices():
            stack = []
            queue = [self.get_vertex(start_key)]
            searched = set()
            backup_queue = dict()
            for i in self.get_vertex(start_key).connected.keys():
                stack.append(i)
                backup_queue[i] = queue.copy()
                result += f"{start_key} -> {i.key}\n"

            topology_bool = True
            while topology_bool:
                if stack:
                    temp = stack.pop()
                    queue.append(temp)
                    for i in temp.connected.keys():
                        if i in queue:
                            topology_bool = False
                            break
                        else:
                            stack.append(i)
                            backup_queue[i] = queue.copy()
                            if temp not in searched:
                                result += f"{temp.key} -> {i.key}\n"

                    if temp.connected.keys():
                        searched.add(temp)
                    elif stack:
                        queue = backup_queue[stack[-1]]
                else:
                    break

            if not topology_bool:
                return False
        return result

    def shortest_path_missionaries_and_cannibals(self, start_key, destiny_key):
        result = ""
        start_vert = self.get_vertex(start_key)

        queue = []
        backup_path = dict()
        for i in start_vert.connected.keys():
            backup_path[i] = [start_vert, i]
            queue.append(i)

        while True:
            if queue:
                temp = queue.pop(0)
                if temp.key == destiny_key:
                    path = backup_path[temp]
                    for i in range(len(path)-1):
                        miss_left_current, cann_left_current, miss_right_current, cann_right_current, side_current = path[i].key[1], path[i].key[3], path[i].key[5], path[i].key[7], path[i].key[9]
                        miss_left_next, cann_left_next, miss_right_next, cann_right_next, side_next = path[i+1].key[1], path[i+1].key[3], path[i+1].key[5], path[i+1].key[7], path[i+1].key[9]
                        if side_current == "left":
                            result += f"{miss_left_next}_{cann_left_next} -({miss_left_current-miss_left_next}, {cann_left_current - cann_left_next})-> {miss_right_next}_{cann_right_next}\n"
                        elif side_current == "right":
                            result += f"{miss_left_next}_{cann_left_next} <-({miss_left_next-miss_left_current}, {cann_left_next-cann_left_current})- {miss_right_next}_{cann_right_next}\n"
                    result += "\n"
                    break
                else:
                    for i in temp.connected.keys():
                        backup_path[i] = backup_path[temp].copy()
                        backup_path[i].append(i)
                        queue.append(i)
            else:
                result += "-\n\n"
                break
        return result

    def missionaries_cannibals_solve(self, miss, cann):
        self.add_vertex(("missionaries_left", miss, "cannibals_left", cann, "missionaries_right", 0, "cannibals_right", 0, "boat_side", "left"))
        start_state = self.get_vertex(("missionaries_left", miss, "cannibals_left", cann, "missionaries_right", 0, "cannibals_right", 0, "boat_side", "left"))
        queue = [start_state]
        visited = [start_state.key]

        if_solved = False
        solution = None
        while queue:
            temp = queue.pop(0)
            miss_left, cann_left, miss_right, cann_right, side = temp.key[1], temp.key[3], temp.key[5], temp.key[7], temp.key[9]
            if miss_left == 0 and cann_left == 0 and miss_right == miss and cann_right == cann and side == "right":
                if not if_solved:
                    if_solved = True
                    solution = temp.key

            if side == "left":
                if miss_left >= 1 and (miss_left - 1 >= cann_left or miss_left - 1 == 0) and miss_right + 1 >= cann_right:
                    next_vert_key = ("missionaries_left", miss_left - 1, "cannibals_left", cann_left, "missionaries_right", miss_right + 1, "cannibals_right", cann_right, "boat_side", "right")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if cann_left >= 1 and (miss_right >= cann_right + 1 or miss_right == 0):
                    next_vert_key = ("missionaries_left", miss_left, "cannibals_left", cann_left - 1, "missionaries_right", miss_right, "cannibals_right", cann_right + 1, "boat_side", "right")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if miss_left >= 2 and (miss_left - 2 >= cann_left or miss_left - 2 == 0) and miss_right + 2 >= cann_right:
                    next_vert_key = ("missionaries_left", miss_left - 2, "cannibals_left", cann_left, "missionaries_right", miss_right + 2, "cannibals_right", cann_right, "boat_side", "right")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if cann_left >= 2 and (miss_right >= cann_right + 2 or miss_right == 0):
                    next_vert_key = ("missionaries_left", miss_left, "cannibals_left", cann_left - 2, "missionaries_right", miss_right, "cannibals_right", cann_right + 2, "boat_side", "right")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if miss_left >= 1 and cann_left >= 1 and miss_right >= cann_right:
                    next_vert_key = ("missionaries_left", miss_left - 1, "cannibals_left", cann_left - 1, "missionaries_right", miss_right + 1, "cannibals_right", cann_right + 1, "boat_side", "right")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

            elif side == "right":
                if miss_right >= 1 and (miss_right - 1 >= cann_right or miss_right - 1 == 0) and miss_left + 1 >= cann_left:
                    next_vert_key = ("missionaries_left", miss_left + 1, "cannibals_left", cann_left, "missionaries_right", miss_right - 1, "cannibals_right", cann_right, "boat_side", "left")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if cann_right >= 1 and (miss_left >= cann_left + 1 or miss_left == 0):
                    next_vert_key = ("missionaries_left", miss_left, "cannibals_left", cann_left + 1, "missionaries_right", miss_right, "cannibals_right", cann_right - 1, "boat_side", "left")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if miss_right >= 2 and (miss_right - 2 >= cann_right or miss_right - 2 == 0) and miss_left + 2 >= cann_left:
                    next_vert_key = ("missionaries_left", miss_left + 2, "cannibals_left", cann_left, "missionaries_right", miss_right - 2, "cannibals_right", cann_right, "boat_side", "left")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if cann_right >= 2 and (miss_left >= cann_left + 2 or miss_left == 0):
                    next_vert_key = ("missionaries_left", miss_left, "cannibals_left", cann_left + 2, "missionaries_right", miss_right, "cannibals_right", cann_right - 2, "boat_side", "left")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)

                if miss_right >= 1 and cann_right >= 1 and miss_left >= cann_left:
                    next_vert_key = ("missionaries_left", miss_left + 1, "cannibals_left", cann_left + 1, "missionaries_right", miss_right - 1, "cannibals_right", cann_right - 1, "boat_side", "left")
                    if next_vert_key not in visited:
                        self.add_vertex(next_vert_key)
                        next_vert = self.get_vertex(next_vert_key)
                        temp.add_neighbor(next_vert)
                        visited.append(next_vert.key)
                        queue.append(next_vert)
            else:
                raise Exception("Boat crashed (its side is not in ['left', 'right'])")


        if if_solved:
            result = f"State: [Missionaries]_[Cannibals]   Boat: ([Missionaries], [Cannibals])\nStart: {miss}_{cann} -- 0_0\n"
            result += self.shortest_path_missionaries_and_cannibals(start_state.key, solution)
            return result
        else:
            return False

    def __contains__(self, key):  # wierzchołek
        return key in self.vertices

    def __str__(self):
        result = ""
        for i in self.vertices.keys():
            for j in self.vertices[i].connected.keys():
                result += f"{i} -{self.vertices[i].connected[j]}-> {j.key}\n"
        return result


class Vertex:
    def __init__(self, key):
        self.key = key
        self.connected = dict()

    def add_neighbor(self, other, weight=0):
        self.connected[other] = weight

    def __str__(self):
        if self.connected:
            result = f"{self.key} -> ["
            for i in self.connected.keys():
                result += f"{i.key} ({self.connected[i]}), "
            result = result[:-2] + "]"
            return result
        else:
            return f"{self.key}"

    def get_edges(self):
        return self.connected.keys()

    def get_weight(self, nbr):
        if nbr in self.connected:
            return self.connected[nbr]
        else:
            return None


def program_run():
    pass



if __name__ == "__main__":
    g = Graph()

    print(g.missionaries_cannibals_solve(3,3))













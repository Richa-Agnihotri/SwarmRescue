import networkx as nx
import heapq


# ==================================
# MEMBER 2 : GRAPH & PATH PLANNING
# ==================================

class RescueSystem:

    def __init__(self):
        self.global_map = set()

    # ------------------------------
    # INPUT FROM MEMBER 3 (DRONES)
    # ------------------------------
    def receive_drone_map(self, drone_map):

        self.global_map.update(drone_map)

        print("\n[INPUT RECEIVED]")
        print("Drone Map:", drone_map)

    # ------------------------------
    # INPUT FROM MEMBER 1 (YOLO)
    # ------------------------------
    def receive_victim_location(self, victim_location):

        self.victim_location = victim_location

        print("\n[INPUT RECEIVED]")
        print("Victim Found At:", victim_location)

    # ------------------------------
    # BUILD GRAPH
    # ------------------------------
    def build_graph(self, grid):

        self.grid = grid

        self.graph = nx.Graph()

        rows = len(grid)
        cols = len(grid[0])

        directions = [
            (1,0),(-1,0),
            (0,1),(0,-1)
        ]

        for i in range(rows):
            for j in range(cols):

                if grid[i][j] == 1:
                    continue

                for dx, dy in directions:

                    ni = i + dx
                    nj = j + dy

                    if (
                        0 <= ni < rows and
                        0 <= nj < cols and
                        grid[ni][nj] != 1
                    ):

                        self.graph.add_edge(
                            (i,j),
                            (ni,nj),
                            weight=1
                        )

    # ------------------------------
    # HEURISTIC
    # ------------------------------
    def heuristic(self, a, b):

        return (
            abs(a[0]-b[0]) +
            abs(a[1]-b[1])
        )

    # ------------------------------
    # A* SEARCH
    # ------------------------------
    def find_rescue_path(
        self,
        rescue_team,
        victim_location
    ):

        open_set = []

        heapq.heappush(
            open_set,
            (0, rescue_team)
        )

        came_from = {}

        g_score = {
            rescue_team: 0
        }

        while open_set:

            _, current = heapq.heappop(open_set)

            if current == victim_location:

                path = []

                while current in came_from:

                    path.append(current)

                    current = came_from[current]

                path.append(rescue_team)

                path.reverse()

                return path

            for neighbor in self.graph.neighbors(current):

                tentative = (
                    g_score[current] + 1
                )

                if (
                    neighbor not in g_score
                    or
                    tentative < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = tentative

                    f = (
                        tentative
                        +
                        self.heuristic(
                            neighbor,
                            victim_location
                        )
                    )

                    heapq.heappush(
                        open_set,
                        (f, neighbor)
                    )

        return None

    # ------------------------------
    # OUTPUT TO MEMBER 4
    # ------------------------------
    def generate_report(
        self,
        rescue_team
    ):

        path = self.find_rescue_path(
            rescue_team,
            self.victim_location
        )

        report = {

            "Merged_Map":
                self.global_map,

            "Victim":
                self.victim_location,

            "Rescue_Path":
                path
        }

        return report


# ==================================
# EXAMPLE INPUTS FROM TEAM MEMBERS
# ==================================

system = RescueSystem()


# INPUT FROM MEMBER 3
system.receive_drone_map({
    (0,0),
    (0,1),
    (1,1)
})

system.receive_drone_map({
    (1,1),
    (2,1),
    (2,2)
})


# INPUT FROM MEMBER 1 (YOLO)
system.receive_victim_location(
    (4,3)
)


# OCCUPANCY GRID
grid = [

    [0,0,0,0,0],

    [0,1,1,0,0],

    [0,0,0,0,0],

    [0,1,0,1,0],

    [0,0,0,0,0]
]

system.build_graph(grid)


# INPUT FROM RESCUE TEAM
rescue_team = (0,0)


# OUTPUT
output = system.generate_report(
    rescue_team
)

print("\n========== OUTPUT ==========")

for key, value in output.items():

    print(key, ":", value)
class Node:
    def __init__(self, parent=None, position=None):
    self.parent = parent
    self.position = position
    self.g = 0
    self.h = 0
    self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def astar(maze, start, end):
        # Create start and end node\n",
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        # Initialize both open and closed list\n",
        open_list = []
        closed_list = []
        # Add the start node\n",
        open_list.append(start_node)

        # Loop until you find the end\n",
        while len(open_list) > 0:
            # Get the current node\n"
            current_node = open_list[0]\
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list\n",
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal with updated end_goal y position\n",
            end_node = Node(end_node.parent, tuple([end_node.position[0], current_node.position[1]]))
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path\n",

            # Generate children\n",
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares\n",

                # Get node position\n",
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                # Make sure within range\n",
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > 
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain\n",
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node\n",
                new_node = Node(current_node, node_position)

                # Append\n",
                children.append(new_node)

            # Loop through children\n",
            for child in children:
                # Child is on the closed list\n",
                for closed_child in closed_list:
                    if child == closed_child:
                        continue\n",

                # Create the f, g, and h values\n",
                child.g = current_node.g + 1
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h

                # Child is already in the open list\n",
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list\n",
                open_list.append(child)

    def play_angle(x,y):
        angle = 0
        if x == 1 and y == 0:
            angle = 0
            
        elif x == 1 and y == 1:
            angle = 45

        elif x == 0 and y == 1:
            angle = 90

        elif x == -1 and y == 1:
            angle = 135

        elif x == -1 and y == 0:
           angle = 180
           
        elif x == -1 and y == -1:
            angle = 225

        elif x == 0 and y == -1:
            angle = 270

        elif x == 1 and y == -1:
            angle = 315

        else:
            angle = 0         
        return angle

    def astar_algorithm():
        # Get and create player map\n",
        output = makemap(2020020200,2146)
    #     print(\"makemap done\")\n",
    #     print(output['RBPOS'])\n",
    #     print(output['RBPOS'][0], output['DIRECTION'], output['YARDS'])\n",

        actual_x = []
        actual_y = []
        for i in output['RBPOS']:
            actual_x.append(i[0])
            actual_y.append(i[1])

        all_grids = []
        for j in range(len(output['GRIDS'])):
            maze = output['GRIDS'][j]
            serial = maze.flatten().astype(int).tolist()
            row = []
            grid = []
            for index in range(len(serial)):
                row.append(int(serial[index]))
                if index > 0 and (index + 1) % 55 == 0:
                    grid.append(row)
                    row = []
            all_grids.append(grid)


        start = (actual_x[0], actual_y[0])
        end = (actual_x[0] - output['YARDS'], actual_y[0])
    #     print(end)\n",

        list_of_optimal_paths = []
        optimal_angles = []
        optimal_step = [start]

    #     print(len(all_grids))\n",

        for i in range(len(all_grids)):
            start = (actual_x[i], actual_y[i])
            path = (astar(all_grids[i], start, end))
            
            list_of_optimal_paths.append(path)
            
            if len(path) > 1:
                optimal_step.append(path[1])
                
    #     print(\"paths:\", len(optimal_step))\n",

        for i in range(len(optimal_step) - 1):
            x = optimal_step[i+1][0] - optimal_step[i][0]
            y = optimal_step[i+1][1] - optimal_step[i][1]
            optimal_angles.append(play_angle(x,y))
            \n",
    #     print(\"angles:\", len(optimal_angles))\n",

    #     for coords in path[2:]:\n",
    #         optimal_path.append(coords)\n",


    #     for c in range(len(optimal_path[:-1])):\n",
    #         x = optimal_path[c+1][0] - optimal_path[c][0]\n",
    #         y = optimal_path[c+1][1] - optimal_path[c][1]\n",
    #         optimal_angles.append(play_angle(x,y))\n",



        actual_angles = []
        for o in range(len(output['RBPOS']) - 1):
            x = output['RBPOS'][o+1][0] - output['RBPOS'][o][0]
            y = output['RBPOS'][o+1][1] - output['RBPOS'][o][1]
            actual_angles.append(play_angle(x,y))

        aangles = []
    #     print(\"optimal\", len(optimal_angles))\n",

        if len(optimal_angles) < len(actual_angles):
            for i in range(len(optimal_angles)):
                aangles.append(actual_angles[i])

        else: 
            tmp = []\n",
            for i in range(len(actual_angles)):
                aangles.append(actual_angles[i])
                tmp.append(optimal_angles[i])
            optimal_angles = tmp
    #     print(\"aangles\", len(aangles))\n",
    #     print(len(actual_angles))\n",

        x_path = []
        y_path = []
        x_maze = []
        y_maze = []
        ts = 190

        for coord in list_of_optimal_paths[ts]:
            x_path.append(coord[0])
            y_path.append(coord[1])

        for x_coord in range(len(all_grids[ts])):
            for y_coord in range(len(all_grids[ts][0])):
                if all_grids[ts][x_coord][y_coord] == 1:
                    x_maze.append(x_coord)
                    y_maze.append(y_coord)

    #     print((x_path), y_path)\n",
        print(len(actual_x), len(actual_y))
        \n",
        plt.plot(x_maze, y_maze, 'ro ', ms=5, label='Blockers')
        plt.plot(x_path, y_path, 'g.', ms=10, label ='Optimal Path')
        plt.plot(actual_x[190:], actual_y[190:], 'k.',ms=5, label ='Actual Path')
        plt.axis(xmin=0, xmax=100, ymin=0, ymax=56)
        plt.grid()
        plt.xticks(np.arange(0, 100, step=10))
        plt.yticks(np.arange(0, 56, step=5))
        plt.legend(loc=\"upper left\")
        plt.tight_layout()
    #     plt.show()\n",
        plt.savefig('2020020200_2146_190ts.png')

        return optimal_angles, aangles
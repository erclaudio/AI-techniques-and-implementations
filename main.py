from os import linesep
import queue
import csv


def getInfo(line):
    line = line.split(", ")
    startingNode = line[0][1:-1]
    endNode = line[1][1:-1]
    tubeLine = line[2][1:-1]
    timeCost = line[3]
    mainZone = line[4][1:-1]
    secondaryZone = line[5][1:-2]
    return startingNode, endNode, tubeLine, timeCost, mainZone, secondaryZone


with open('tubedata.txt', "r") as f:
    lines = f.readlines()
    startingNodes = {}
    for line in lines:
        startingNode, endNode, tubeLine, timeCost, mainZone, secondaryZone = getInfo(
            line)
        timeCost = int(timeCost)
        if startingNode in startingNodes:
            startingNodes[startingNode].append((endNode, timeCost, tubeLine))
        else:
            startingNodes[startingNode] = [(endNode, timeCost, tubeLine)]
        if endNode in startingNodes:
            startingNodes[endNode].append((startingNode, timeCost, tubeLine))
        else:
            startingNodes[endNode] = [(startingNode, timeCost, tubeLine)]


def dfs(start, end, graph):
    stack = [(start, [start], 0)]  # Initialize a stack, node,  path, cost
    visited = set()  # Initialze a set shoiwing us which nods we have visited

    while stack:
        # We romove the last item we added(its a stack)
        station, path, cost = stack.pop()
        if station not in visited:  # If we havent visited then we can check if it is the end.

            if station == end:
                # If it is then we just return the path so far
                return path, cost, len(visited)
            # If not we add it to the visited set
            visited.add(station)
            # and then for every station we can get to starting from this station, we put it in the stack and we update the path
            for nextStation in graph[station]:
                stack.append(
                    (nextStation[0], path + [nextStation[0]], cost + nextStation[1]))
    return None, 0, 0


def bfs(start, end, graph):
    queue = [(start, [start], 0)]  # Initialize the queue
    visited = set()
    while queue:
        # Remove the first node we added to the queue(its a queue)
        station, path, cost = queue.pop(0)
        if station not in visited:
            visited.add(station)
            if station == end:  # if it is the destination, then we return the path
                return path, cost, len(visited)
            # else for evry station, we can reach, we put them in the queue
            for nextStation in graph[station]:
                queue.append(
                    (nextStation[0], path + [nextStation[0]], cost + nextStation[1]))

        # The difference with dfs is the order we get the nextStation. In queue we get the first item , in stack the last
    return None, 0, 0


def uniform_cost_search(start, end, graph):
    visited = set()  # set of the visited stations
    lines = []
    q = queue.PriorityQueue()
    q.put((0, start, [start]))  # cost,current node, path, lineUsed
    # cost = 0 and the current node is the start, and the path contains only this node
    while not q.empty():
        cost, curr, path = q.get()  # get the left most item from the queue
        if curr not in visited:
            # put it in the visited set and we know we are on the shortest path
            visited.add(curr)
            if curr == end:
                # if out curr node is the end, then we return the path and the cost to get there
                return path, cost, len(visited)

            else:
                # again for every path we put it in the priorityqueue
                for nextStation in graph[curr]:
                    if nextStation not in visited:
                        q.put((cost + nextStation[1],
                               nextStation[0], path + [nextStation[0]]))

    return None, 0, 0


def printPath(path):
    for i in range(len(path)):
        if i != len(path) - 1:
            print(path[i], "->", end="")
        else:
            print(path[i])


def getLines(graph, path):
    lines = 0
    prevLine = ""
    for i in range(1, len(path)):
        for station in graph[path[i]]:
            if station[0] == path[i - 1] and station[2] != prevLine:
                prevLine = station[2]
                lines += 1
    return lines


def h(graph, node, end):
    for neighbor in graph[node]:
        if neighbor[0] == end:
            return neighbor[1]
    return 10


def a_star_algorithm(graph, start, stop):
    not_visited = set([start])
    visited = set([])

    # poo has present distances from start to all other nodes
    dist = {}
    dist[start] = 0

    # par contains an adjac mapping of all nodes
    par = {}
    par[start] = start


    while len(not_visited) > 0:
        n = None

        # it will find a node with the lowest value of f() -
        for v in not_visited:
            for neighbor in graph[v]:
                if n == None or dist[v] + h(graph, v, neighbor[2]) < dist[n] + h(graph, v, neighbor[2]):
                    n = v


        if n == None:
            print('Path does not exist!')
            return None

        # if the current node is the stop
        # then we start again from start
        if n == stop:
            reconst_path = []

            while par[n] != n:
                reconst_path.append(n)
                n = par[n]

            reconst_path.append(start)

            reconst_path.reverse()

            return reconst_path

        # for all the neighbors of the current node do
        for neighbor in graph[n]:
            # if the current node is not present in both not visited and visited
            # add it to open_lst and note n as it's par
            if neighbor[0] not in not_visited and neighbor[0] not in visited:
                not_visited.add(neighbor[0])
                par[neighbor[0]] = n
                dist[neighbor[0]] = dist[n] + neighbor[1]


            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update par data and poo data
            # and if the node was in the visited, move it to not visited
            else:
                if dist[neighbor[0]] > dist[n] + neighbor[1]:
                    dist[neighbor[0]] = dist[n] + neighbor[1]
                    par[neighbor[0]] = n

                    if neighbor[0] in visited:
                        visited.remove(neighbor[0])
                        not_visited.add(neighbor[0])

        # remove n from the not visited, and add it to visited
        # because all of his neighbors were inspected
        not_visited.remove(n)
        visited.add(n)


    print('Path does not exist!')
    return None


def main(graph):
    while True:
        start = input("Enter the starting station: ")
        end = input("Enter the ending station: ")
        if start not in graph:
            print("Error with starting station. It's not included in the graph")
            continue
        if end not in graph:
            print("Error with ending station. It's not included in the graph")
            continue

        dfsPath, dfsScore, dfsNodes = dfs(start, end, graph)
        bfsPath, bfsScore, bfsNodes = bfs(start, end, graph)
        uscPath, uscScore, uscNodes = uniform_cost_search(start, end, graph)

        print("DFS: ")
        printPath(dfsPath)
        linesUsed = getLines(graph, dfsPath)
        print(f"Time needed: {dfsScore}")
        print(f"Lines used: {linesUsed}")
        print(f"Nodes expanded: {dfsNodes}")

        print("BFS: ")
        printPath(bfsPath)
        linesUsed = getLines(graph, bfsPath)
        print(f"Time needed: {bfsScore}")
        print(f"Lines used: {linesUsed}")
        print(f"Nodes expanded: {bfsNodes}")

        print("USC: ")
        printPath(uscPath)
        linesUsed = getLines(graph, dfsPath)
        print(f"Time needed: {uscScore}")
        print(f"Lines used: {linesUsed}")
        print(f"Nodes expanded: {uscNodes}")

        print("A*: ")
        path = a_star_algorithm(graph, start, end)
        printPath(path)
        press = input("Press q to quit, or a to try again: ")
        if press == "q":
            break


main(startingNodes)

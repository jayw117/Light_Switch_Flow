#Jason Wong
# Problem: Have n lights and switches that are inside a floor plan. Ergonomic if each switch can be
# seen by a light. One switch per light 
from graph import *

from copy import deepcopy
from collections import defaultdict
Walls = [(1,2),(1,5),(8,5),(8,3),(11,3),(11,1),(5,1),(5,3),(4,3),(4,1),(1,1),(1,2)]
lights = [(2,4),(2,2),(5,4)]  #in red
switches = [(4,4),(6,3),(6,2)]  #in green

graph = {}
nodes = ['source','sink']

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
# Return true if line segments AB and CD intersect
# Source: http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
def visible(pt1,pt2,Walls):
    x1,y1 = pt1
    x2,y2 = pt2
    for i,wall in enumerate(Walls[:-1]):
        x3,y3 = wall
        x4,y4 = Walls[i+1]
        if intersect((x1,y1),(x2,y2),(x3,y3),(x4,y4)):
            return False
    return True  
   
# Code was from JuanGunner https://stackoverflow.com/questions/55486168/
# was able to understand how switches and lights are connected
def edges(S,L): # S is switches, L is lights
    graph['sink'] = []
    if len(switches) != len(lights): #check to see even amount of switches and lights
        print("Not even")
        return 
    for i in range(0, len(S)): # will store switches as key in empty dictionary
        graph[S[i]] = []
    for switch in range(0, len(S)): #checks to see what lights are visible to switches using visible function
        for light in range(0, len(S)):
            if visible(S[switch], L[light],Walls) == True: # if true will store lights for switches in dictionary
                graph[S[switch]].append(L[light])
    graph['source'] = []
    
    for switch in range(0, len(S)): 
        graph['source'].append(S[switch]) #The source has three different options it can go out of 
    for light in range(0, len(S)):
        graph[L[light]] = ['sink'] #each of the lights will connect to sink
    for i in lights:
        nodes.append(i)
    for x in switches:
        nodes.append(x)
    print(nodes)
    return flow(nodes, edges) == len(S)
    



#https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/

# finds shortest path between 2 nodes of a graph using BFS
def bfs(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]
 
    # return path if start is goal
    if start == goal:
        return "DONE"
 
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path
 
            # mark node as explored
            explored.append(node)
 
    # in case there's no path between the 2 nodes
    return False
#print(bfs(graph, 'source','sink'))

#print(graph['source'])


def augment(f, p):
    b = 1 # bottleneck
    for i in range(len(p)-1):
        if f[(p[i],)+(p[i+1],)] != None: #If e is forward
            f[(p[i],)+(p[i+1],)]+=b
        else: #If e is backward
            f[(p[i+1],)+(p[i],)]-=b
    return f #f'
        


def flow(nodes, edges):
    
    f = {(False):None}
    for n in nodes:
        for e in graph[n]:
            f[(n,) + (e,)] = 0
            f[(e,)+(n,)] = None
    
    max_flow = 0
    p = bfs(graph,'source','sink')
    
    #max_flow = 0 # Setting the flow at beginning 0 since there is no path 
    while p:
        f = augment(f,p)
        for i in range(0,len(p)-1): #update edges
            graph[p[i]].remove(p[i+1]) #Always reverse the edge, since f(e) = 1
            graph[p[i+1]].append(p[i])
        #O(n)
        p = bfs(graph,'source','sink') #Find a path from source to sink
        if p == False:
            print("All paths done")
        max_flow += 1
    if max_flow == len(lights):
        print("Ergonomic")
    else:
        print("Not Ergonomic")
    

(edges(switches,lights))
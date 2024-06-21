# This file is based on
# https://github.com/dilsonpereira/Minimum-Cost-Perfect-Matching

class MatchingGraph:
    # n is the number of vertices
    # edges is a list of pairs representing the edges (default = empty list)
    def __init__(self, n: int = 0, edges: list[tuple[int, int]] = []):
        self.n: int = n  # Number of vertices
        self.m: int = 0  # Number of edges
        self.adj_mat: list[list[bool]] = [[False for _ in range(n)] for _ in range(n)]  # Adjacency matrix
        self.adj_list: list[list[int]] = [[] for _ in range(n)]  # Adjacency lists
        self.edges: list[tuple[int, int]] = []  # Array of edges
        self.edge_index: list[list[int]] = [[-1 for _ in range(n)] for _ in range(n)]  # Indices of the edges
        for it in edges:
            self.add_edge(it[0], it[1])
    
    # Returns the number of vertices
    def get_num_vertices(self) -> int:
        return self.n

    # Returns the number of edges
    def get_num_edges(self) -> int:
        return self.m
    
    # Given the edge's index, returns its endpoints as a pair
    def get_edge(self, e: int) -> tuple[int, int]:
        if e >= len(self.edges):
            raise IndexError('Error: edge does not exist')
    
        return self.edges[e]
    
    # Given the endpoints, returns the index
    def get_edge_index(self, u: int, v: int) -> int:
        if u >= self.n or v >= self.n:
            raise IndexError('Error: vertex does not exist')
    
        if self.edge_index[u][v] == -1:
            raise IndexError('Error: edge does not exist')
    
        return self.edge_index[u][v]
    
    # Adds a new vertex to the graph
    def add_vertex(self) -> None:
        for a, e in zip(self.adj_mat, self.edge_index):
            a.append(False)
            e.append(-1)
        self.n += 1
        self.adj_mat.append([False for _ in range(self.n)])
        self.edge_index.append([-1 for _ in range(self.n)])
        self.adj_list.append([])
    
    # Adds a new edge to the graph
    def add_edge(self, u: int, v: int) -> None:
        if u >= self.n or v >= self.n:
            raise IndexError('Error: vertex does not exist')
    
        if self.adj_mat[u][v]:
            return
    
        self.adj_mat[u][v] = True
        self.adj_mat[v][u] = True
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)
    
        self.edges.append((u, v))
        self.edge_index[u][v] = self.m
        self.edge_index[v][u] = self.m
        self.m += 1
    
    # Returns the adjacency list of a vertex
    def get_adj_list(self, v: int) -> list[int]:
        if v >= self.n:
            raise IndexError('Error: vertex does not exist')
    
        return self.adj_list[v]
    
    # Returns the graph's adjacency matrix
    def get_adj_mat(self) -> list[list[bool]]:
        return self.adj_mat
    
# This file is based on
# https://github.com/dilsonpereira/Minimum-Cost-Perfect-Matching

from decimal import Decimal
from collections import deque
from matching_graph import MatchingGraph
from binary_heap import BinaryHeap
from e_blossom_type import EBlossomType

class BlossomMatching:
    # Parametric constructor receives a graph instance
    def __init__(self, g: MatchingGraph):
        self.g: MatchingGraph = g
        self.m: int = g.get_num_edges()
        self.n: int = g.get_num_vertices()
        data_size = 2 * self.n
        self.outer: list[int] = [0] * data_size  # outer[v] gives the index of the outermost blossom that contains v, outer[v] = v if v is not contained in any blossom
        self.deep: list[list[int]] = [[] for _ in range(data_size)]  # deep[v] is a list of all the original vertices contained inside v, deep[v] = v if v is an original vertex
        self.shallow: list[list[int]] = [[] for _ in range(data_size)]  # shallow[v] is a list of the vertices immediately contained inside v, shallow[v] is empty is the default
        self.tip: list[int] = [0] * data_size  # tip[v] is the tip of blossom v
        self.active: list[bool] = [False] * data_size  # true if a blossom is being used
        self.blossom_type: list[EBlossomType] = [EBlossomType.UNLABELED] * data_size  # Even, odd, neither
        self.forest: list[int] = [0] * data_size  # forest[v] gives the father of v in the alternating forest
        self.root: list[int] = [0] * data_size  # root[v] gives the root of v in the alternating forest 
        self.blocked: list[bool] = [False] * data_size  # A blossom can be blocked due to dual costs, this means that it behaves as if it were an original vertex and cannot be expanded
        self.dual: list[Decimal] = [Decimal(0)] * data_size  # dual multipliers associated to the blossoms, if dual[v] > 0, the blossom is blocked and full
        self.slack: list[Decimal] = [Decimal(0)] * self.m  # slack associated to each edge, if slack[e] > 0, the edge cannot be used
        self.mate: list[int] = [0] * data_size  # mate[v] gives the mate of v
        self.visited: list[bool] = [False] * data_size
        self.free: deque[int] = deque()  # List of free blossom indices
        self.perfect: bool = False
        self.forest_list: deque[int] = deque()
    
    # Solves the minimum cost perfect matching problem
    # Receives the a vector whose position i has the cost of the edge with index i
    # If the graph doest not have a perfect matching, a const char * exception will be raised
    # Returns a tuple
    # the first element of the tuple is a list of the indices of the edges in the matching
    # the second is the cost of the matching
    def solve_minimum_cost_perfect_matching(self, cost: list[Decimal]) -> tuple[list[int], Decimal]:
        self.solve_maximum_matching()
        if not self.perfect:
            raise ValueError('Error: The graph does not have a perfect matching')

        self.clear()

        # Initialize slacks (reduced costs for the edges)
        self.slack = list(cost)

        self.positive_costs()

        # If the matching on the compressed graph is perfect, we are done
        self.perfect = False
        while not self.perfect:
            # Run an heuristic maximum matching algorithm
            self.heuristic()
            # Grow a hungarian forest
            self.grow()
            self.update_dual_costs()
            # Set up the algorithm for a new grow step
            self.reset()

        matching: list[int] = self.retrieve_matching()

        obj: Decimal = Decimal(0)
        for i in matching:
            obj += cost[i]

        dual_obj: Decimal = Decimal(0)
        for i in range(2 * self.n):
            if i < self.n:
                dual_obj += self.dual[i]
            elif self.blocked[i]:
                dual_obj += self.dual[i]

        return (matching, obj)

    # Solves the maximum cardinality matching problem
    # Returns a list with the indices of the edges in the matching
    def solve_maximum_matching(self) -> list[int]:
        self.clear()
        self.grow()
        return self.retrieve_matching()

    # Grows an alternating forest
    def grow(self) -> None:
        self.reset()

        # All unmatched vertices will be roots in a forest that will be grown
        # The forest is grown by extending a unmatched vertex w through a matched edge u-v in a BFS fashion
        while self.forest_list:
            w: int = self.outer[self.forest_list.popleft()]

            # w might be a blossom
            # we have to explore all the connections from vertices inside the blossom to other vertices
            for u in self.deep[w]:
                cont: bool = False
                for v in self.g.get_adj_list(u):
                    if self.is_edge_blocked2(u, v):
                        continue

                    # u is even and v is odd
                    if self.blossom_type[self.outer[v]] == EBlossomType.ODD:
                        continue

                    # if v is unlabeled
                    if self.blossom_type[self.outer[v]] != EBlossomType.EVEN:
                        # We grow the alternating forest
                        vm: int = self.mate[self.outer[v]]

                        self.forest[self.outer[v]] = u
                        self.blossom_type[self.outer[v]] = EBlossomType.ODD
                        self.root[self.outer[v]] = self.root[self.outer[u]]
                        self.forest[self.outer[vm]] = v
                        self.blossom_type[self.outer[vm]] = EBlossomType.EVEN
                        self.root[self.outer[vm]] = self.root[self.outer[u]]

                        if not self.visited[self.outer[vm]]:
                            self.forest_list.append(vm)
                            self.visited[self.outer[vm]] = True
                    # If v is even and u and v are on different trees
                    # we found an augmenting path
                    elif self.root[self.outer[v]] != self.root[self.outer[u]]:
                        self.augment(u, v)
                        self.reset()

                        cont = True
                        break
                    # If u and v are even and on the same tree
                    # we found a blossom
                    elif self.outer[u] != self.outer[v]:
                        b: int = self.blossom(u, v)

                        self.forest_list.appendleft(b)
                        self.visited[b] = True

                        cont = True
                        break
                if cont:
                    break

        # Check whether the matching is perfect
        self.perfect = True
        for i in range(self.n):
            if self.mate[self.outer[i]] == -1:
                self.perfect = False

    # Expands a blossom u
    # If expand_blocked is true, the blossom will be expanded even if it is blocked
    def expand(self, u: int, expand_blocked: bool = False) -> None:
        v: int = self.outer[self.mate[u]]

        index: int = self.m
        p: int = -1
        q: int = -1
        # Find the regular edge {p,q} of minimum index connecting u and its mate
        # We use the minimum index to grant that the two possible blossoms u and v will use the same edge for a mate
        for di in self.deep[u]:
            for dj in self.deep[v]:
                if self.is_adjacent(di, dj) and self.g.get_edge_index(di, dj) < index:
                    index = self.g.get_edge_index(di, dj)
                    p = di
                    q = dj

        self.mate[u] = q
        self.mate[v] = p
        # If u is a regular vertex, we are done
        if u < self.n or (self.blocked[u] and not expand_blocked):
            return

        found: bool = False
        # Find the position t of the new tip of the blossom
        it: int = 0
        while it < len(self.shallow[u]) and not found:
            si: int = self.shallow[u][it]
            jt: int = 0
            while jt < len(self.deep[si]) and not found:
                if self.deep[si][jt] == p:
                    found = True
                jt += 1
            it += 1
            if not found:
                self.shallow[u].append(si)
                self.shallow[u].pop(0)
                it -= 1

        it = 0
        # Adjust the mate of the tip
        self.mate[self.shallow[u][it]] = self.mate[u]
        it += 1

        # Now we go through the odd circuit adjusting the new mates
        while it < len(self.shallow[u]):
            itnext = it + 1
            self.mate[self.shallow[u][it]] = self.shallow[u][itnext]
            self.mate[self.shallow[u][itnext]] = self.shallow[u][it]
            itnext += 1
            it = itnext

        # We update the sets blossom, shallow, and outer since this blossom is being deactivated
        for s in self.shallow[u]:
            self.outer[s] = s
            for t in self.deep[s]:
                self.outer[t] = s
        self.active[u] = False
        self.add_free_blossom_index(u)

        # Expand the vertices in the blossom
        for t in self.shallow[u]:
            self.expand(t, expand_blocked)

    # Augments the matching using the path from u to v in the alternating forest
    # Augment the path root[u], ..., u, v, ..., root[v]
    def augment(self, u: int, v: int) -> None:
        # We go from u and v to its respective roots, alternating the matching
        p: int = self.outer[u]
        q: int = self.outer[v]
        outv: int = q
        fp: int = self.forest[p]
        self.mate[p] = q
        self.mate[q] = p
        self.expand(p)
        self.expand(q)
        while fp != -1:
            q = self.outer[self.forest[p]]
            p = self.outer[self.forest[q]]
            fp = self.forest[p]

            self.mate[p] = q
            self.mate[q] = p
            self.expand(p)
            self.expand(q)

        p = outv
        fp = self.forest[p]
        while fp != -1:
            q = self.outer[self.forest[p]]
            p = self.outer[self.forest[q]]
            fp = self.forest[p]

            self.mate[p] = q
            self.mate[q] = p
            self.expand(p)
            self.expand(q)

    # Resets the alternating forest
    def reset(self) -> None:
        for i in range(2 * self.n):
            self.forest[i] = -1
            self.root[i] = i

            if i >= self.n and self.active[i] and self.outer[i] == i:
                self.destroy_blossom(i)

        self.visited = [False] * (2 * self.n)
        self.forest_list.clear()
        for i in range(self.n):
            if self.mate[self.outer[i]] == -1:
                self.blossom_type[self.outer[i]] = EBlossomType.EVEN
                if not self.visited[self.outer[i]]:
                    self.forest_list.append(i)
                self.visited[self.outer[i]] = True
            else:
                self.blossom_type[self.outer[i]] = EBlossomType.UNLABELED

    # Creates a blossom where the tip is the first common vertex in the paths from u and v in the hungarian forest
    # Contracts the blossom w, ..., u, v, ..., w, where w is the first vertex that appears in the paths from u and v to their respective roots
    def blossom(self, u: int, v: int) -> int:
        t: int = self.get_free_blossom_index()

        is_in_path: list[bool] = [False] * (2 * self.n)

        # Find the tip of the blossom
        u_: int = u
        while u_ != -1:
            is_in_path[self.outer[u_]] = True

            u_ = self.forest[self.outer[u_]]

        v_: int = self.outer[v]
        while not is_in_path[v_]:
            v_ = self.outer[self.forest[v_]]
        self.tip[t] = v_

        # Find the odd circuit, update shallow, outer, blossom and deep
        # First we construct the set shallow (the odd circuit)
        circuit: deque[int] = deque()
        u_ = self.outer[u]
        circuit.appendleft(u_)
        while u_ != self.tip[t]:
            u_ = self.outer[self.forest[u_]]
            circuit.appendleft(u_)

        self.shallow[t].clear()
        self.deep[t].clear()
        for it in circuit:
            self.shallow[t].append(it)

        v_ = self.outer[v]
        while v_ != self.tip[t]:
            self.shallow[t].append(v_)
            v_ = self.outer[self.forest[v_]]

        # Now we construct deep and update outer
        for u_ in self.shallow[t]:
            self.outer[u_] = t
            for jt in self.deep[u_]:
                self.deep[t].append(jt)
                self.outer[jt] = t

        self.forest[t] = self.forest[self.tip[t]]
        self.blossom_type[t] = EBlossomType.EVEN
        self.root[t] = self.root[self.tip[t]]
        self.active[t] = True
        self.outer[t] = t
        self.mate[t] = self.mate[self.tip[t]]

        return t

    def update_dual_costs(self) -> None:
        e1: Decimal = Decimal(0)
        e2: Decimal = Decimal(0)
        e3: Decimal = Decimal(0)
        inite1: bool = False
        inite2: bool = False
        inite3: bool = False
        for i in range(self.m):
            u: int = self.g.get_edge(i)[0]
            v: int = self.g.get_edge(i)[1]

            if (self.blossom_type[self.outer[u]] == EBlossomType.EVEN and self.blossom_type[self.outer[v]] == EBlossomType.UNLABELED) or \
               (self.blossom_type[self.outer[v]] == EBlossomType.EVEN and self.blossom_type[self.outer[u]] == EBlossomType.UNLABELED):
                if (not inite1) or e1 > self.slack[i]:
                    e1 = self.slack[i]
                    inite1 = True
            elif self.outer[u] != self.outer[v] and self.blossom_type[self.outer[u]] == EBlossomType.EVEN and self.blossom_type[self.outer[v]] == EBlossomType.EVEN:
                if (not inite2) or e2 > self.slack[i]:
                    e2 = self.slack[i]
                    inite2 = True
        for i in range(self.n, 2 * self.n):
            if self.active[i] and i == self.outer[i] and self.blossom_type[self.outer[i]] == EBlossomType.ODD and (not inite3 or e3 > self.dual[i]):
                e3 = self.dual[i]
                inite3 = True
        e: Decimal = Decimal(0)
        if inite1:
            e = e1
        elif inite2:
            e = e2
        elif inite3:
            e = e3

        if e > e2 / 2 and inite2:
            e = e2 / 2
        if e > e3 and inite3:
            e = e3

        for i in range(2 * self.n):
            if i != self.outer[i]:
                continue

            if self.active[i] and self.blossom_type[self.outer[i]] == EBlossomType.EVEN:
                self.dual[i] += e
            elif self.active[i] and self.blossom_type[self.outer[i]] == EBlossomType.ODD:
                self.dual[i] -= e

        for i in range(self.m):
            u: int = self.g.get_edge(i)[0]
            v: int = self.g.get_edge(i)[1]

            if self.outer[u] != self.outer[v]:
                if self.blossom_type[self.outer[u]] == EBlossomType.EVEN and self.blossom_type[self.outer[v]] == EBlossomType.EVEN:
                    self.slack[i] -= 2 * e
                elif self.blossom_type[self.outer[u]] == EBlossomType.ODD and self.blossom_type[self.outer[v]] == EBlossomType.ODD:
                    self.slack[i] += 2 * e
                elif (self.blossom_type[self.outer[v]] == EBlossomType.UNLABELED and self.blossom_type[self.outer[u]] == EBlossomType.EVEN) or (self.blossom_type[self.outer[u]] == EBlossomType.UNLABELED and self.blossom_type[self.outer[v]] == EBlossomType.EVEN):
                    self.slack[i] -= e
                elif (self.blossom_type[self.outer[v]] == EBlossomType.UNLABELED and self.blossom_type[self.outer[u]] == EBlossomType.ODD) or (self.blossom_type[self.outer[u]] == EBlossomType.UNLABELED and self.blossom_type[self.outer[v]] == EBlossomType.ODD):
                    self.slack[i] += e
        for i in range(self.n, 2 * self.n):
            if self.dual[i] > 0:
                self.blocked[i] = True
            elif self.active[i] and self.blocked[i]:
                # The blossom is becoming unblocked
                if self.mate[i] == -1:
                    self.destroy_blossom(i)
                else:
                    self.blocked[i] = False
                    self.expand(i)

    # Resets all data structures 
    # Sets up the algorithm for a new run
    def clear(self) -> None:
        self.clear_blossom_indices()

        for i in range(2 * self.n):
            self.outer[i] = i
            self.deep[i].clear()
            if i < self.n:
                self.deep[i].append(i)
            self.shallow[i].clear()
            if i < self.n:
                self.active[i] = True
            else:
                self.active[i] = False

            self.blossom_type[i] = EBlossomType.UNLABELED
            self.forest[i] = -1
            self.root[i] = i

            self.blocked[i] = False
            self.dual[i] = Decimal(0)
            self.mate[i] = -1
            self.tip[i] = i
        self.slack = [Decimal(0)] * self.m

    # Destroys a blossom recursively
    def destroy_blossom(self, t: int) -> None:
        if t < self.n or (self.blocked[t] and self.dual[t] > 0):
            return

        for s in self.shallow[t]:
            self.outer[s] = s
            for jt in self.deep[s]:
                self.outer[jt] = s

            self.destroy_blossom(s)

        self.active[t] = False
        self.blocked[t] = False
        self.add_free_blossom_index(t)
        self.mate[t] = -1

    # Uses an heuristic algorithm to find the maximum matching of the graph
    # Vertices will be selected in non-decreasing order of their degree
    # Each time an unmatched vertex is selected, it is matched to its adjacent unmatched vertex of minimum degree
    def heuristic(self) -> None:
        degree: list[int] = [0] * self.n
        b: BinaryHeap = BinaryHeap()

        for i in range(self.m):
            if self.is_edge_blocked1(i):
                continue

            p: tuple[int, int] = self.g.get_edge(i)
            u: int = p[0]
            v: int = p[1]

            degree[u] += 1
            degree[v] += 1

        for i in range(self.n):
            b.insert(Decimal(degree[i]), i)

        while len(b) > 0:
            u: int = b.delete_min()
            if self.mate[self.outer[u]] == -1:
                min: int = -1
                for v in self.g.get_adj_list(u):
                    if self.is_edge_blocked2(u, v) or self.outer[u] == self.outer[v] or self.mate[self.outer[v]] != -1:
                        continue

                    if min == -1 or degree[v] < degree[min]:
                        min = v
                if min != -1:
                    self.mate[self.outer[u]] = min
                    self.mate[self.outer[min]] = u

    # Modifies the costs of the graph so the all edges have positive costs
    def positive_costs(self) -> None:
        min_edge: Decimal = Decimal(0)
        for s in self.slack:
            if min_edge > s:
                min_edge = s

        for i in range(self.m):
            self.slack[i] -= min_edge

    def retrieve_matching(self) -> list[int]:
        matching: list[int] = []

        for i in range(2 * self.n):
            if self.active[i] and self.mate[i] != -1 and self.outer[i] == i:
                self.expand(i, True)

        for i in range(self.m):
            u: int = self.g.get_edge(i)[0]
            v: int = self.g.get_edge(i)[1]

            if self.mate[u] == v:
                matching.append(i)
        return matching

    def get_free_blossom_index(self) -> int:
        return self.free.pop()

    def add_free_blossom_index(self, i: int) -> None:
        self.free.append(i)

    def clear_blossom_indices(self) -> None:
        self.free.clear()
        for i in range(self.n, 2 * self.n):
            self.add_free_blossom_index(i)

    # An edge might be blocked due to the dual costs
    def is_edge_blocked2(self, u: int, v: int) -> bool:
        return self.slack[self.g.get_edge_index(u, v)] > 0
    
    def is_edge_blocked1(self, e: int) -> bool:
        return self.slack[e] > 0

    # Returns true if u and v are adjacent in G and not blocked
    def is_adjacent(self, u: int, v: int) -> bool:
        return self.g.get_adj_mat()[u][v] and not self.is_edge_blocked2(u, v)

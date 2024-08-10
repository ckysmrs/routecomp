from decimal import Decimal

from edge import Edge
from alias_graph import AliasGraph
from matching_graph import MatchingGraph
from blossom_matching import BlossomMatching

## Blossomアルゴリズムのマッチング結果を返す。
#  @param complete_graph 入力の完全グラフ。
#  @return マッチング結果のグラフ。
def blossom(complete_graph: AliasGraph) -> AliasGraph:
    num_vertex: int = complete_graph.get_node_size()
    num_edge: int   = complete_graph.get_edge_size()

    nodes: set[int]           = complete_graph.get_copy_of_nodes()
    tmp_to_org_map: list[int] = list(nodes)

    g = MatchingGraph(num_vertex)
    cost: list[Decimal] = [Decimal(0)] * num_edge
    for edge in complete_graph.edge_generator():
        u: int = tmp_to_org_map.index(complete_graph.get_alias_node(edge.get_node1()))
        v: int = tmp_to_org_map.index(complete_graph.get_alias_node(edge.get_node2()))
        c: Decimal = edge.get_cost()
        g.add_edge(u, v)
        cost[g.get_edge_index(u, v)] = c
    m = BlossomMatching(g)
    solution: tuple[list[int], Decimal] = m.solve_minimum_cost_perfect_matching(cost)
    matching: list[int] = solution[0]
    matching_graph = AliasGraph()
    for it in matching:
        e: tuple[int, int] = g.get_edge(it)
        matching_graph.add_edge(Edge(tmp_to_org_map[e[0]], tmp_to_org_map[e[1]], Decimal(1)))
    return matching_graph

from decimal import Decimal

from edge import Edge
from alias_graph import AliasGraph
from binary_heap import BinaryHeap
from dijkstra_node import DijkstraNode
from dijkstra_path import DijkstraPath

## ダイクストラ法。

## ダイクストラ法で最短経路探索を行う。
#  @param graph    探索するグラフ。
#  @param start_id 探索のスタートノードのID。
#  @param goal_id  探索のゴールノードのID。
#  @return 探索結果の経路。
def get_shortest_path(graph: AliasGraph, start_id: int, goal_id: int) -> DijkstraPath:
    node_list: list[DijkstraNode] = make_node_list(graph)
    open_list: BinaryHeap = BinaryHeap()
    for n in node_list:
        open_list.insert(n.get_score(), n.get_id())

    start_node: DijkstraNode = DijkstraNode.get_dijkstra_node_by_id(node_list, start_id)
    goal_node: DijkstraNode  = DijkstraNode.get_dijkstra_node_by_id(node_list, goal_id)

    if start_node is not None:
        start_node.open(None, Decimal(0), open_list)

    result_path = DijkstraPath()
    if goal_node is not None:
        while len(open_list) > 0:
            min_id = open_list.delete_min()
            target: DijkstraNode = DijkstraNode.get_dijkstra_node_by_id(node_list, min_id)
            if target == goal_node:
                open_list.clear()
            else:
                target.expand(node_list, open_list)

        if goal_node.get_parent_node() is None:
            return result_path

        result_path.add(goal_node)
        while result_path[0].get_parent_node() is not None:
            result_path.insert(0, result_path[0].get_parent_node())
    return result_path

## ノードリストを返す。
#  @param graph 対象グラフ。
#  @return ノードリスト。
def make_node_list(graph: AliasGraph) -> list[DijkstraNode]:
    node_list: list[DijkstraNode] = []
    for edge in graph.edge_generator():
        if not contains(node_list, graph.get_alias_node(edge.get_node1())):
            node_list.append(DijkstraNode(graph.get_alias_node(edge.get_node1())))
        if not contains(node_list, graph.get_alias_node(edge.get_node2())):
            node_list.append(DijkstraNode(graph.get_alias_node(edge.get_node2())))
        node_id: int = graph.get_alias_node(edge.get_node1())
        dn: DijkstraNode = DijkstraNode.get_dijkstra_node_by_id(node_list, node_id)
        if dn is not None:
            dn.add_edge(Edge(graph.get_alias_node(edge.get_node1()),
                        graph.get_alias_node(edge.get_node2()),
                        edge.get_cost()))
        node_id = graph.get_alias_node(edge.get_node2())
        dn = DijkstraNode.get_dijkstra_node_by_id(node_list, node_id)
        if dn is not None:
            dn.add_edge(Edge(graph.get_alias_node(edge.get_node1()),
                        graph.get_alias_node(edge.get_node2()),
                        edge.get_cost()))
    return node_list

## ノードリストが指定ノードを含んでいるときTrueを返す。
#  @param nodes ノードリスト。
#  @param node_id 検索するノードのID。
#  @return ノードリストが指定ノードを含んでいるときTrue。
def contains(nodes: list[DijkstraNode], node_id: int) -> bool:
    for dn in nodes:
        if dn.get_id() == node_id:
            return True

    return False

## 指定ノード間の最小コストを返す。
#  @param graph 探索するグラフ。
#  @param start 経路の始点。
#  @param goal  経路の終点。
#  @return 始点と終点間の最小コスト。
def get_shortest_length(graph: AliasGraph, start: int, goal: int) -> Decimal:
    path: DijkstraPath = get_shortest_path(graph, start, goal)
    return path.get_cost()

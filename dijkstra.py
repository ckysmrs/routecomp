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
    goal_nodes = set_costs_to_goals(graph, start_id, [goal_id])
    return generate_dijkstra_path(goal_nodes[0])

## スタートからゴールまでの経路のコストを探索し、ゴールノードを返す。
#  @param graph    探索するグラフ。
#  @param start_id 探索のスタートノードのID。
#  @param goal_ids 探索のゴールノードのIDのリスト。
#  @return ゴールノードのリスト。ゴールノードが存在しないとき要素はNone。
def set_costs_to_goals(graph: AliasGraph, start_id: int, goal_ids: list[int]) -> list[DijkstraNode | None]:
    node_list: list[DijkstraNode] = make_node_list(graph)
    open_list: BinaryHeap = BinaryHeap()
    for n in node_list:
        open_list.insert(n.get_score(), n.get_id())

    start_node: DijkstraNode = DijkstraNode.get_dijkstra_node_by_id(node_list, start_id)
    goal_nodes: list[DijkstraNode] = [DijkstraNode.get_dijkstra_node_by_id(node_list, n) for n in goal_ids]
    targets = [n for n in goal_nodes if n is not None]
    if not targets:
        return goal_nodes

    if start_node is not None:
        start_node.open(None, Decimal(0), open_list)

    while targets and len(open_list) > 0:
        min_id = open_list.delete_min()
        target: DijkstraNode = DijkstraNode.get_dijkstra_node_by_id(node_list, min_id)
        if target in targets:
            targets.remove(target)
        target.expand(node_list, open_list)

    return goal_nodes

## ゴールノードを終点としてパスを生成して返す。
#  @param goal ゴールノード。
#  @return ゴールノードを終点としたパス。
def generate_dijkstra_path(goal: DijkstraNode) -> DijkstraPath:
    result_path = DijkstraPath()
    if goal is None:
        return result_path
    result_path.add(goal)
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

## 指定ノード間の最小コストのリストを返す。
#  @param graph 探索するグラフ。
#  @param start 経路の始点。
#  @param goal  経路の終点のリスト。
#  @return 始点と各終点間の最小コストのリスト。
#          出力リストのインデックスnがstartとgoals[n]間の最小コスト。
def single_source_shortest_length(graph: AliasGraph, start: int, goals: list[int]) -> list[Decimal]:
    goals = set_costs_to_goals(graph, start, goals)
    return [n.get_score() for n in goals]

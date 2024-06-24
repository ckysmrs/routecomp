from edge import Edge
from alias_graph import AliasGraph
import matching
import dijkstra
from dijkstra_path import DijkstraPath

## グラフをオイラーグラフに変換する。
#  @param graph 元のグラフ。
#  @return 変換後のオイラーグラフ。
#  @exception ValueError 元のグラフが連結グラフではないとき。
#                        オイラーグラフへの変換に失敗したとき。
def graph_to_eulerian_graph(graph: AliasGraph) -> AliasGraph:
    if not graph.is_connected():
        raise ValueError('分断ネット')

    initial_graph = AliasGraph.copy_instance(graph)
    branch_list: list[AliasGraph] = pick_up_branch_and_remove(graph)
    make_euler_graph(graph)
    restore_branch_with_duplicating(graph, branch_list)
    # 枝線を復帰してから無駄線を削除しないと、枝線がフローティングになることがある。
    cut_extra_route(graph, initial_graph)

    if not graph.contains_graph(initial_graph):
        raise ValueError('オイラーグラフの作成に失敗しました。')

    return graph

## 枝線の集合グラフのリストを返し、graphからこれらの枝線を取り除く。
#  枝線は次数1のノードを含む辺。いわゆる盲腸線。
#  0, 1, ..., n - 1の順に取り除いたので、n - 1, n - 2, ..., 0の順に元に戻す。
#  @param graph 対象グラフ。
#  @return 枝線の集合グラフのリスト。
def pick_up_branch_and_remove(graph: AliasGraph) -> list[AliasGraph]:
    branch_list: list[AliasGraph] = []
    while True:
        branch_graph: AliasGraph = graph.pick_up_branch_and_remove()
        if branch_graph.is_empty():
            break
        branch_list.append(branch_graph)
    return branch_list

## オイラーグラフに変換する。
#  @param graph 元グラフ。
def make_euler_graph(graph: AliasGraph) -> None:
    local_graph = AliasGraph.copy_instance(graph)
    odd_nodes: list[int] = get_odd_degree_nodes(graph)
    if odd_nodes:
        make_degree_even(odd_nodes, local_graph)
    replace_graph(graph, local_graph)

## 次数が奇数の頂点リストを返す。
#  @param graph 対象グラフ。
#  @return 次数が奇数の頂点リスト。
def get_odd_degree_nodes(graph: AliasGraph) -> list[int]:
    degree_map: dict[int, int] = graph.get_degree_map()
    result: list[int] = []
    for k, v in degree_map.items():
        if v % 2 != 0:
            result.append(k)
    return result

## オイラーグラフを作成する。
#  @param odd_nodes 次数が奇数の頂点リスト。
#  @param graph 元グラフ。
def make_degree_even(odd_nodes: list[int], graph: AliasGraph) -> None:
    c_graph = make_complete_graph(odd_nodes, graph)
    minimum_cost_perfect_matching: AliasGraph = matching.blossom(c_graph)
    add_matching_to_graph(minimum_cost_perfect_matching, graph)

## 指定ノードの完全グラフを返す。
#  @param odd_nodes ノードリスト。
#  @param graph 元データのグラフ。
#  @return 完全グラフ。
def make_complete_graph(odd_nodes: list[int], graph: AliasGraph) -> AliasGraph:
    c_graph = AliasGraph()

    for i in range(len(odd_nodes)):
        for j in range(i + 1, len(odd_nodes)):
            e = Edge(odd_nodes[i],
                    odd_nodes[j],
                    dijkstra.get_shortest_length(graph, odd_nodes[i], odd_nodes[j]))
            c_graph.add_edge(e)
    return c_graph

## マッチングをグラフに追加する。
#  @param matching 追加元のマッチング。
#  @param graph 追加先のグラフ。
def add_matching_to_graph(matching: AliasGraph, graph: AliasGraph) -> None:
    ite_edge = matching.edge_iterator()
    while True:
        try:
            edge: Edge  = next(ite_edge)
            start: int = matching.get_alias_node(edge.get_node1())
            goal: int  = matching.get_alias_node(edge.get_node2())

            d_path: DijkstraPath = dijkstra.get_shortest_path(graph, start, goal)
            node1: int = 0
            node2: int = d_path[0].get_id()

            for i in range(1, len(d_path)):
                node1 = node2
                node2 = d_path[i].get_id()
                e = graph.get_edge_by_nodes(node1, node2)
                if e is not None:
                    graph.add_edge(e)
        except StopIteration:
            break

## graphAの内容をgraphBに置き換える。
#  @param graph_a グラフ。
#  @param graph_b グラフ。
def replace_graph(graph_a: AliasGraph, graph_b: AliasGraph) -> None:
    graph_a.clear()
    graph_a.merge_graph(graph_b)

## 枝線を2重化しながら戻す。
#  branch_graph_listは逆順に処理する。
#  @param graph 戻し先のグラフ。
#  @param branch_graph_list 枝線の集合グラフリスト。
def restore_branch_with_duplicating(graph: AliasGraph, branch_graph_list: list[AliasGraph]) -> None:
    if not branch_graph_list:
        return

    for i in reversed(range(len(branch_graph_list))):
        branch_graph = AliasGraph.copy_instance(branch_graph_list[i])
        branch_graph.merge_graph(branch_graph)
        graph.merge_graph(branch_graph)

## 余分な路線を省く。
#  @param graph 編集するグラフ。
#  @param initial_graph 初期データグラフ。
def cut_extra_route(graph: AliasGraph, initial_graph: AliasGraph) -> None:
    waste_graph = AliasGraph.copy_instance(graph)
    ite_edge = initial_graph.edge_iterator()
    while True:
        try:
            edge = next(ite_edge)
            waste_graph.remove_edge(edge)
        except StopIteration:
            break

    while not waste_graph.is_empty():
        e = waste_graph.get_edge(0)
        e_number: int = waste_graph.get_number_of_edge(e)
        if e_number >= 2:
            for i in range(e_number // 2 * 2):
                graph.remove_edge(e)
        for i in range(e_number):
            waste_graph.remove_edge(e)

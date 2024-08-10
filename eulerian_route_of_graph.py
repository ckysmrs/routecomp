from alias_graph import AliasGraph

## オイラールートを作る。
#  @param graph 入力グラフ。
#  @param start_node 始点。
#  @return オイラールートのノードリスト。
#  @exception ValueError 入力グラフがオイラーグラフではないとき。
#                        入力グラフからオイラールートが生成できないとき。
def eulerian_route_of_graph(graph: AliasGraph, start_node: int = -1) -> list[list[int]]:
    if not graph.is_euler_graph():
        raise ValueError('オイラーグラフではありません。')
    route: list[list[int]] = generate_initial_euler_circuit(graph, start_node)

    return route

## オイラールートを作る。
#  @param graph 元のグラフ。
#  @param start_node 始点。
#  @return オイラールートのノードリスト。
def generate_initial_euler_circuit(graph: AliasGraph, start_node: int) -> list[list[int]]:
    real_route: list[list[int]]  = []
    work_graph: AliasGraph = AliasGraph.copy_instance(graph)

    while not work_graph.is_empty():
        start_node: int = select_start_node(work_graph, real_route, start_node)
        temp_route = generate_loop_route(work_graph, start_node)
        merge_euler_circuit(real_route, temp_route, work_graph)
    return real_route

## start_nodeから一周するルートを作る。
#  ルートに使用されたエッジはgraphから削除される。
#  @param graph      グラフ。
#  @param start_node 始点。 
#  @return ルート。
#  @exception ValueError ルートが見つからなかったとき。
def generate_loop_route(graph: AliasGraph, start_node: int) -> list[list[int]]:
    start_alias_node = graph.get_alias_node(start_node)
    from_alias_node  = graph.get_alias_node(start_node)
    to_node: int     = -1
    to_alias_node    = -1
    temp_route: list[list[int]]  = []
    while to_alias_node != start_alias_node:
        to_node = graph.get_real_node_from_node(from_alias_node)
        if to_node is None:
            raise ValueError()
        edges = graph.get_edge_list_by_node(from_alias_node)
        route_edge = None
        for e in edges:
            if e.get_node1() == to_node or e.get_node2() == to_node:
                route_edge = e
                break
        if route_edge is None:
            raise ValueError()
        to_alias_node = graph.get_alias_node(to_node)
        real_from_node = route_edge.get_paired_node(to_node)
        temp_route.append([real_from_node, to_node])
        from_alias_node = graph.get_alias_node(to_node)
        graph.remove_edge(route_edge)
    return temp_route

## 始点のIDを返す。エイリアスではなくオリジナルノードのID。
#  @param work_graph 入力グラフ。
#  @param result     オイラールートのリスト。
#  @param start_node 始点。 
#  @return 始点のID。
def select_start_node(work_graph: AliasGraph, result: list[list[int]], start_node: int) -> int:
    if not result:
        if start_node >= 0:
            return start_node
        gen_list = work_graph.edge_generator()
        first_edge = next(gen_list)
        return first_edge.get_node1()

    for alias_nodes in result:
        n = convert_to_alias(alias_nodes[0], work_graph)
        m = convert_to_alias(alias_nodes[1], work_graph)
        if work_graph.contains_node(n):
            edge_list = work_graph.get_edge_list_by_node(n)
            for edge in edge_list:
                if work_graph.get_alias_node(edge.get_node1()) == n:
                    return edge.get_node1()
                if work_graph.get_alias_node(edge.get_node2()) == n:
                    return edge.get_node2()

    if work_graph.contains_node(m):
        edge_list = work_graph.get_edge_list_by_node(m)
        for edge in edge_list:
            if work_graph.get_alias_node(edge.get_node1()) == m:
                return edge.get_node1()
            if work_graph.get_alias_node(edge.get_node2()) == m:
                return edge.get_node2()

    return -1

## オリジナルノードをエイリアスノードに変換する。
#  オリジナルノードはグラフには無く、エイリアス情報のみが残っているかもしれない。
#  @param n オリジナルノード。
#  @param graph: グラフ。
#  @return エイリアスノード。
#          エイリアス情報がないときはオリジナルノードを返す。
def convert_to_alias(n: int, graph: AliasGraph) -> int:
    if n in graph.alias_map:
        return graph.alias_map[n]
    return n

## オイラー回路を合成する。
#  @param graph      合成先グラフ。
#  @param temp_graph 合成するグラフ。
#  @param g エイリアス情報を持つグラフ
def merge_euler_circuit(graph: list[list[int]], temp_graph: list[list[int]], g: AliasGraph) -> None:
    if not graph:
        graph.extend(temp_graph)
        return

    start_node: int = temp_graph[0][0]
    insert_point: int = len(graph) - 1

    while insert_point >= 0:
        node: int = graph[insert_point][1]

        if convert_to_alias(start_node, g) == convert_to_alias(node, g):
            if insert_point == len(graph) - 1:
                graph.extend(temp_graph)
                return
            else:
                graph[insert_point + 1: insert_point + 1] = temp_graph
                return

        insert_point -= 1

    node: int = graph[0][0]
    if convert_to_alias(start_node, g) == convert_to_alias(node, g):
        graph[0: 0] = temp_graph
        return

## スタートノードがエイリアスのとき、スタートノードへの接続をルートデータに追記する。
#  @param route ルートデータ。
#  @param start_node スタートノード。
#  @param graph グラフ。
def add_alias_connect(route: list[list[int]], start_node: int, graph: AliasGraph) -> None:
    alias_to_original = graph.get_alias_dict()
    origs = set()
    for a in alias_to_original:
        if start_node in alias_to_original[a]:
            origs = set(alias_to_original[a])
            origs.remove(start_node)
    for i, p in enumerate(route):
        if p[1] in origs:
            route.insert(i + 1, [p[1], start_node])
            route.insert(i + 2, [start_node, p[1]])
            return
    if route[-1][1] in origs:
        p = route[-1][1]
        route.append([p, start_node])
        route.append([start_node, p])

## ノードがルートにあるときTrueを返す。
#  @param n ノード。
#  @param route ルートデータ。
#  @return ノードがルートにあるときTrue。
def node_in_route(n: int, route: list[list[int]]) -> bool:
    for r in route:
        if n == r[0] or n == r[1]:
            return True
    return False

from decimal import Decimal
from collections.abc import Generator, Iterator

from edge import Edge
from graph import Graph

## Graphにエイリアス機能を付けるラッパー。
class AliasGraph:
    def __init__(self):
        self.graph = Graph()
        self.alias_map: dict[int, int] = dict()  # real -> aliasのマップ

    ## 辺を追加する。辺がNoneの場合は追加しない。
    #  新規のノードのエイリアス情報はリセットされる。
    #  @param edge 追加する辺。
    def add_edge(self, edge: Edge) -> None:
        if edge is None:
            return

        n1 = edge.get_node1()
        n2 = edge.get_node2()
        if not self.graph.contains_node(n1):
            self.alias_map.pop(n1, None)
        if not self.graph.contains_node(n2):
            self.alias_map.pop(n2, None)
        self.graph.add_edge(edge)

    ## 辺を削除する。
    #  @param edge 削除する辺。
    def remove_edge(self, edge: Edge) -> None:
        self.graph.remove_edge(edge)

    def remove_alias_key(self, n: int) -> None:
        if not self.graph.contains_node(n):
            self.alias_map.pop(n, None)

    ## ノードの一覧のコピーを返す。
    #  @return ノードの一覧のコピー。
    def get_copy_of_nodes(self) -> set[int]:
        nodes = self.graph.get_copy_of_nodes()
        for k, v in self.alias_map.items():
            if k in nodes:
                nodes.remove(k)
                nodes.add(v)
        return nodes

    ## 辺のジェネレータを返す。
    #  @return 辺のジェネレータ。
    def edge_generator(self) -> Generator[Edge]:
        for e in self.graph.edge_generator():
            yield e

    ## 辺のイテレータを返す。
    #  @return 辺のイテレータ。
    def edge_iterator(self) -> Iterator:
        return self.graph.edge_iterator()

    ## 辺の数を返す。
    #  @return 辺の数。
    def get_edge_size(self) -> int:
        return self.graph.get_edge_size()

    ## ノードの数を返す。
    #  @return ノードの数。
    def get_node_size(self) -> int:
        return len(self.get_copy_of_nodes())

    ## オリジナルノードの数を返す。
    #  @return オリジナルノードの数。
    def get_real_node_size(self) -> int:
        return self.graph.get_node_size()

    ## 指定されたインデックスの辺を返す。
    #  @param i 返される辺のインデックス。
    #  @return 指定されたインデックスにある辺。
    def get_edge(self, i: int) -> Edge:
        return self.graph.get_edge(i)

    ## 指定のエイリアスノードを結ぶ辺を1本返す。
    #  @param node1 ノード。
    #  @param node2 ノード。
    #  @return 指定のノードを結ぶ辺。辺が無いときはNoneを返す。
    def get_edge_by_nodes(self, node1: int, node2: int) -> Edge | None:
        if node1 in self.alias_map or node2 in self.alias_map:
            return None

        alias_dict = self.get_alias_dict()
        if node1 in alias_dict:
            nodes1 = alias_dict[node1]
        else:
            nodes1 = {node1}
        if node2 in alias_dict:
            nodes2 = alias_dict[node2]
        else:
            nodes2 = {node2}
        for n1 in nodes1:
            for n2 in nodes2:
                e = self.graph.get_edge_by_nodes(n1, n2)
                if e is not None:
                    return e
        return None

    ## 指定のオリジナルノードを結ぶ辺を1本返す。
    #  @param node1 ノード。
    #  @param node2 ノード。
    #  @return 指定のノードを結ぶ辺。辺が無いときはNoneを返す。
    def get_edge_by_real_nodes(self, node1: int, node2: int) -> Edge | None:
        return self.graph.get_edge_by_nodes(node1, node2)

    ## 指定のノードを含む辺のリストを返す。
    #  @param node   対象のノード。
    #  @param e_list 探索する辺のリスト。
    #                指定しないときはこのグラフに含まれる辺を対象にする。
    #  @return 指定のノードを含む辺のリスト。
    def get_edge_list_by_node(self, node: int, e_list: list[Edge] = None) -> list[Edge]:
        if node in self.alias_map:
            return []
        alias_dict: dict[int, set[int]] = self.get_alias_dict()
        if node in alias_dict:
            edge_list = []
            for n in alias_dict[node]:
                local_list = self.graph.get_edge_list_by_node(n, e_list)
                local_list = [e for e in local_list if e not in edge_list]
                edge_list += local_list
            return edge_list

        return self.graph.get_edge_list_by_node(node, e_list)

    ## グラフを空にする。
    def clear(self) -> None:
        self.graph.clear()
        self.alias_map.clear()

    def __eq__(self, other):
        if (other is None) or (not isinstance(other, AliasGraph)):
            return False
        return self.alias_map == other.alias_map and self.graph == other.graph
        
    ## 辺のリストの内容が同じ時Trueを返す。
    #  順序は同じでなくてもよい。
    #  @param edges1 比較する辺リスト。
    #  @param edges2 比較する辺リスト。
    #  @return 2つのリストの内容が同じ時True。
    @staticmethod
    def is_same(edges1: list[Edge], edges2: list[Edge]) -> bool:
        return Graph.is_same(edges1, edges2)

    def __hash__(self):
        return hash(self.graph)

    ## 指定グラフと同じグラフを生成する。辺はシャローコピー。
    #  @param g コピー元のグラフ。
    #  @return  指定されたグラフと同じグラフ。
    @staticmethod
    def copy_instance(g: 'AliasGraph') -> 'AliasGraph':
        new_graph = AliasGraph()
        new_graph.graph = Graph.copy_instance(g.graph)
        new_graph.alias_map = g.alias_map.copy()
        return new_graph

    ## グラフの包含を調べる。
    #  @param g 指定グラフ。
    #  @return このグラフが指定グラフを含んでいるときTrue。
    def contains_graph(self, g: 'AliasGraph') -> bool:
        return self.graph.contains_graph(g.graph)

    ## グラフが空のときTrueを返す。
    #  @return グラフが空のときTrue。
    def is_empty(self) -> bool:
        return self.graph.is_empty()

    ## グラフに含まれる辺の総コストを返す。
    #  @return 総コスト。
    def get_total_cost(self) -> Decimal:
        return self.graph.get_total_cost()

    ## 指定オリジナルノードにつながったオリジナルノードを1つ返す。
    #  指定ノードが無いときはNoneを返す。
    #  @param node 指定ノード。
    #  @return 指定ノードにつながったノード。
    def get_real_node_from_real_node(self, node: int) -> int | None:
        return self.graph.get_node_from_node(node)

    ## 指定エイリアスノードにつながったオリジナルノードを1つ返す。
    #  指定ノードが無いときはNoneを返す。
    #  @param node 指定ノード。
    #  @return 指定ノードにつながったノード。
    def get_real_node_from_node(self, node: int) -> int | None:
        alias_dict = self.get_alias_dict()
        if node in alias_dict:
            for n in alias_dict[node]:
                if self.graph.contains_node(n):
                    return self.graph.get_node_from_node(n)
        else:
            return self.graph.get_node_from_node(node)

    ## 指定のノードを含んでいるかを返す。
    #  @param node 指定のノード。オリジナルまたはエイリアス。
    #  @return 指定のノードを含む時True。
    def contains_node(self, node: int) -> bool:
        if self.graph.contains_node(node):
            return True
        alias_to_original = self.get_alias_dict()
        if node in alias_to_original:
            for orig in alias_to_original[node]:
                if self.graph.contains_node(orig):
                    return True
        return False

    ## 指定の辺を含んでいるかを返す。
    #  @param edge 指定の辺。
    #  @return 指定の辺を含む時True。
    def contains_edge(self, edge: Edge) -> bool:
        return self.graph.contains_edge(edge)

    ## 辺の情報からノードのセットを再作成する。
    def refresh_node_set(self) -> None:
        self.graph.refresh_node_set()

    ## 指定グラフをマージする。
    #  @param graph マージするグラフ。
    #  @exception ValueError 同じノードに異なるエイリアスが設定されているとき。
    def merge_graph(self, graph: 'AliasGraph') -> None:
        self.graph.merge_graph(graph.graph)
        for n in graph.alias_map:
            if n in self.alias_map:
                if self.alias_map[n] != graph.alias_map[n]:
                    raise ValueError('マージするグラフに異なるエイリアスが設定されています')
            else:
                self.alias_map[n] = graph.alias_map[n]

    ## このグラフが連結グラフのときTrueを返す。空グラフのときはFalseを返す。
    #  @return このグラフが連結グラフのときTrue。空グラフのときはFalse。
    def is_connected(self) -> bool:
        convert_graph = self.generate_alias_node_graph()
        return convert_graph.is_connected()

    ## このグラフがオイラーグラフかを返す。
    #  @return このグラフがオイラーグラフのときTrue。
    def is_euler_graph(self) -> bool:
        convert_graph = self.generate_alias_node_graph()
        return convert_graph.is_euler_graph()

    def generate_alias_node_graph(self) -> Graph:
        convert_graph = Graph()
        edge_ite = self.graph.edge_iterator()
        while True:
            try:
                edge = next(edge_ite)
                node1 = self.get_alias_node(edge.get_node1())
                node2 = self.get_alias_node(edge.get_node2())
                convert_graph.add_edge(Edge(node1, node2, Decimal('1')))
            except StopIteration:
                break
        return convert_graph

    ## 指定の辺が何本含まれているかを返す。
    #  @param edge 調べる辺。
    #  @return 指定の辺がこのグラフに含まれている数。
    def get_number_of_edge(self, edge: Edge) -> int:
        return self.graph.get_number_of_edge(edge)

    ## エイリアスノードとそのノードの次数の辞書を返す。
    #  @return ノードとそのノードの次数の辞書。
    def get_degree_map(self) -> dict[int, int]:
        alias_degree = dict()
        real_degree  = self.graph.get_degree_map()
        for n in real_degree:
            if n in self.alias_map:
                if self.alias_map[n] not in alias_degree:
                    alias_degree[self.alias_map[n]] = real_degree[n]
                else:
                    alias_degree[self.alias_map[n]] += real_degree[n]
            else:
                alias_degree[n] = real_degree[n]
        return alias_degree

    ## 枝線(次数1のノードを含む辺)を抜き出し、 その枝線をこのグラフから削除する。
    #  再帰的には処理しないので、処理後に新たに枝線が発生する可能性がある。
    #  @return 枝線の集合グラフ。
    def pick_up_branch_and_remove(self) -> 'AliasGraph':
        degree_map: dict[int, int] = self.get_degree_map()
        branch_graph = AliasGraph()
        for i in degree_map.keys():
            if degree_map[i] == 1:
                branch_graph.add_edge(self.get_edge_list_by_node(i)[0])

        e_ite = branch_graph.edge_iterator()
        while True:
            try:
                e = next(e_ite)
                node1: int = e.get_node1()
                if node1 in self.alias_map:
                    branch_graph.set_alias_node(node1, self.alias_map[node1])
                node2: int = e.get_node2()
                if node2 in self.alias_map:
                    branch_graph.set_alias_node(node2, self.alias_map[node2])
                self.remove_edge(e)
            except StopIteration:
                break

        return branch_graph

    ## ノードのエイリアスを返す。
    #  ノードが無いときはノードをそのまま返す。
    #  @param real ノード。
    #  @return ノードのエイリアス。
    def get_alias_node(self, real: int) -> int:
        if not self.graph.contains_node(real):
            return real
        if real not in self.alias_map:
            return real
        return self.alias_map[real]

    def set_alias_node(self, real: int, alias: int) -> None:
        self.alias_map[real] = alias

    ## エイリアスの辞書を返す。
    #  キーがエイリアスで、値がそのエイリアスに対応するノードのセット。
    #  @return エイリアスの辞書。
    def get_alias_dict(self) -> dict[int, set[int]]:
        alias_dict: dict[int, set[int]] = dict()
        for k, v in self.alias_map.items():
            if v not in alias_dict:
                alias_dict[v] = set()
            alias_dict[v].add(k)
        return alias_dict

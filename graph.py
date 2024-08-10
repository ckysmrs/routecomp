from decimal import Decimal
from collections import deque
from collections.abc import Generator, Iterator

from edge import Edge

## グラフ。次数0のノードは作成不可。
class Graph:
    def __init__(self):
        self.edge_list: list[Edge] = []
        self.node_set: set[int] = set()

    ## 辺を追加する。辺がNoneの場合は追加しない。
    #  @param edge 追加する辺。
    def add_edge(self, edge: Edge) -> None:
        if edge == None:
            return

        self.edge_list.append(edge)
        self.node_set.add(edge.get_node1())
        self.node_set.add(edge.get_node2())

    ## 辺を削除する。
    #  @param edge 削除する辺。
    def remove_edge(self, edge: Edge) -> None:
        self.edge_list.remove(edge)
        self.refresh_node_set()

    ## ノードの一覧のコピーを返す。
    #  @return ノードの一覧のコピー。
    def get_copy_of_nodes(self) -> set[int]:
        return self.node_set.copy()

    ## 辺のジェネレータを返す。
    #  @return 辺のジェネレータ。
    def edge_generator(self) -> Generator[Edge]:
        for e in self.edge_list:
            yield e

    ## 辺のイテレータを返す。
    #  @return 辺のイテレータ。
    def edge_iterator(self) -> Iterator[Edge]:
        return iter(self.edge_list)

    ## 辺の数を返す。
    #  @return 辺の数。
    def get_edge_size(self) -> int:
        return len(self.edge_list)

    ## ノードの数を返す。
    #  @return ノードの数。
    def get_node_size(self) -> int:
        return len(self.node_set)

    ## 指定されたインデックスの辺を返す。
    #  @param i 返される辺のインデックス。
    #  @return 指定されたインデックスにある辺。
    def get_edge(self, i: int) -> Edge:
        return self.edge_list[i]

    ## 指定のノードを結ぶ辺を1本返す。
    #  @param node1 ノード。
    #  @param node2 ノード。
    #  @return 指定のノードを結ぶ辺。辺が無いときはNoneを返す。
    def get_edge_by_nodes(self, node1: int, node2: int) -> Edge | None:
        for e in self.edge_list:
            if e.contains_nodes(node1, node2):
                return e
        return None

    ## 指定のノードを含む辺のリストを返す。
    #  @param node   対象のノード。
    #  @param e_list 探索する辺のリスト。
    #                指定しないときはこのグラフに含まれる辺を対象にする。
    #  @return 指定のノードを含む辺のリスト。
    def get_edge_list_by_node(self, node: int, e_list: list[Edge] = None) -> list[Edge]:
        if e_list == None:
            e_list = self.edge_list
        result: list[Edge] = []
        for e in e_list:
            if e.get_node1() == node or e.get_node2() == node:
                result.append(e)
        return result

    ## グラフを空にする。
    def clear(self) -> None:
        self.edge_list.clear()
        self.node_set.clear()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Graph):
            return False
        return Graph.is_same(other.edge_list, self.edge_list)
        
    ## 辺のリストの内容が同じ時Trueを返す。
    #  順序は同じでなくてもよい。
    #  @param edges1 比較する辺リスト。
    #  @param edges2 比較する辺リスト。
    #  @return 2つのリストの内容が同じ時True。
    @staticmethod
    def is_same(edges1: list[Edge], edges2: list[Edge]) -> bool:
        if (len(edges1) != len(edges2)):
            return False

        copy1: list[Edge] = list(edges1)
        copy2: list[Edge] = list(edges2)

        while copy1:
            e = copy1[0]
            if e in copy2:
                copy1.remove(e)
                copy2.remove(e)
            else:
                return False

        return True

    def __hash__(self):
        result = 17

        listHash = 0
        for e in self.edge_list:
            listHash += hash(e)
        result = 31 * result + listHash

        return hash(result)

    ## 指定グラフと同じグラフを生成する。辺はシャローコピー。
    #  @param g コピー元のグラフ。
    #  @return  指定されたグラフと同じグラフ。
    @staticmethod
    def copy_instance(g: 'Graph') -> 'Graph':
        new_graph = Graph()

        org_list = g.edge_list
        for e in org_list:
            new_graph.add_edge(e)

        return new_graph

    ## グラフの包含を調べる。
    #  @param g 指定グラフ。
    #  @return このグラフが指定グラフを含んでいるときTrue。
    def contains_graph(self, g: 'Graph') -> bool:
        if g.is_empty():
            return True

        e_list: list[Edge] = g.edge_list
        for e in e_list:
            if e not in self.edge_list:
                return False

        return True

    ## グラフが空のときTrueを返す。
    #  @return グラフが空のときTrue。
    def is_empty(self) -> bool:
        return not self.edge_list

    ## グラフに含まれる辺の総コストを返す。
    #  @return 総コスト。
    def get_total_cost(self) -> Decimal:
        sum = Decimal(0)

        for e in self.edge_list:
            sum += e.get_cost()
        return sum

    ## 指定ノードにつながったノードを1つ返す。
    #  指定ノードが無いときはNoneを返す。
    #  @param node 指定ノード。
    #  @return 指定ノードにつながったノード。
    def get_node_from_node(self, node: int) -> int | None:
        for e in self.edge_list:
            n = e.get_paired_node(node)
            if n is not None:
                return n

        return None

    ## 指定のノードを含んでいるかを返す。
    #  @param node 指定のノード。
    #  @return 指定のノードを含む時True。
    def contains_node(self, node: int) -> bool:
        for n in self.node_set:
            if n == node:
                return True
        return False

    ## 指定の辺を含んでいるかを返す。
    #  @param edge 指定の辺。
    #  @return 指定の辺を含む時True。
    def contains_edge(self, edge: Edge) -> bool:
        return edge in self.edge_list

    ## 辺の情報からノードのセットを再作成する。
    def refresh_node_set(self) -> None:
        self.node_set.clear()

        for e in self.edge_list:
            self.node_set.add(e.get_node1())
            self.node_set.add(e.get_node2())

    ## 指定グラフをマージする。
    #  @param graph マージするグラフ。
    def merge_graph(self, graph: 'Graph') -> None:
        self.edge_list.extend(graph.edge_list)
        self.refresh_node_set()

    ## このグラフが連結グラフのときTrueを返す。空グラフのときはFalseを返す。
    #  @return このグラフが連結グラフのときTrue。空グラフのときはFalse。
    def is_connected(self) -> bool:
        if not self.edge_list:
            return False

        self.refresh_node_set()
        searched_node: deque[int] = deque()
        unsearched_node: list[int] = list(self.get_copy_of_nodes())
        unsearched_edge: list[Edge] = list(self.edge_list)

        node: int = unsearched_node[0]
        searched_node.appendleft(node)
        unsearched_node.remove(node)

        while searched_node:
            path_list: list[Edge] = self.get_edge_list_by_node(node, unsearched_edge)
            if path_list:
                path: Edge = path_list[0]
                unsearched_edge.remove(path)
                node = path.get_paired_node(node)
                if node in unsearched_node:
                    unsearched_node.remove(node)
                if not unsearched_node:
                    return True
                searched_node.appendleft(node)
            else:
                node = searched_node.popleft()
                if searched_node:
                    node = searched_node[0]
                else:
                    node = None

        if not unsearched_node:
            return True

        return False

    ## このグラフがオイラーグラフかを返す。
    #  @return このグラフがオイラーグラフのときTrue。
    def is_euler_graph(self) -> bool:
        if self.is_empty():
            return False

        if not self.is_connected():
            return False

        degree_map: dict[int, int] = dict()

        self.refresh_node_set()
        for n in self.get_copy_of_nodes():
            degree_map[n] = 0

        for e in self.edge_list:
            if e.get_node1() >= 0 and e.get_node2() >= 0:
                degree_map[e.get_node1()] += 1
                degree_map[e.get_node2()] += 1

        for node in degree_map.keys():
            if degree_map[node] % 2 != 0:
                return False
        return True

    ## 指定の辺が何本含まれているかを返す。
    #  @param edge 調べる辺。
    #  @return 指定の辺がこのグラフに含まれている数。
    def get_number_of_edge(self, edge: Edge) -> int:
        counter: int = 0
        for e in self.edge_list:
            if e == edge:
                counter += 1
        return counter

    ## ノードとそのノードの次数の辞書を返す。
    #  @return ノードとそのノードの次数の辞書。
    def get_degree_map(self) -> dict[int, int]:
        degree_map: dict[int, int] = dict()
        for e in self.edge_list:
            node1: int = e.get_node1()
            node2: int = e.get_node2()
            if node1 in degree_map:
                degree_map[node1] += 1
            else:
                degree_map[node1] = 1
            if node2 in degree_map:
                degree_map[node2] += 1
            else:
                degree_map[node2] = 1
        return degree_map

    ## 枝線(次数1のノードを含む辺)を抜き出し、 その枝線をこのグラフから削除する。
    #  再帰的には処理しないので、処理後に新たに枝線が発生する可能性がある。
    #  @return 枝線の集合グラフ。
    def pick_up_branch_and_remove(self) -> 'Graph':
        degree_map: dict[int, int] = self.get_degree_map()
        branch_graph = Graph()
        for i in degree_map.keys():
            if degree_map[i] == 1:
                branch_graph.add_edge(self.get_edge_list_by_node(i)[0])

        for e in branch_graph.edge_list:
            self.remove_edge(e)

        return branch_graph
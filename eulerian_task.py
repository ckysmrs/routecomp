import sys
from decimal import Decimal
import itertools

from edge import Edge
from alias_graph import AliasGraph
from graph_to_eulerian_graph import graph_to_eulerian_graph
from eulerian_route_of_graph import eulerian_route_of_graph
import graph_file_loader

class EulerianTask:
    def __init__(self):
        self.node_list: list[str]  = []
        self.start_goal_edge: Edge | None = None

    def gen_eulerian_graph_from_list(self, data_list_file: str, start_point: str, goal_point: str) -> None:
        files = graph_file_loader.read_data_list(data_list_file)
        self.gen_eulerian_graph(files, start_point, goal_point)

    ## (準)オイラーグラフを生成する。
    #  @param data_file   データファイルの場所のリスト。
    #  @param start_point 始点。
    #  @param goal_point  終点。
    #  @exception ValueError 実行中に問題が発生したとき。
    def gen_eulerian_graph(self, data_files: list[str], start_point: str, goal_point: str) -> None:
        self.set_start_and_goal(start_point, goal_point)
        graph, big_cost, self.node_list = graph_file_loader.generate_graph_from_files(data_files)
        if graph is None:
            return
        self.overwrite_start_goal_route(graph, big_cost)

        try:
            graph = graph_to_eulerian_graph(graph)
        except ValueError as e:
            print(e, file=sys.stderr)
            return

        if not graph.is_euler_graph():
            print('ERROR: オイラーグラフの作成に失敗しました。', file=sys.stderr)
            return

        self.print_eulerian_graph(graph)

    ## オイラールートを生成する。
    #  @param data_files  データファイルの場所のリスト。
    #  @param start_point 始点。
    #  @param goal_point  終点。
    #  @exception ValueError 実行中に問題が発生したとき。
    def gen_eulerian_route(self, data_files: list[str], start_point: str, goal_point: str) -> None:
        self.set_start_and_goal(start_point, goal_point)
        graph, big_cost, self.node_list = graph_file_loader.generate_graph_from_files(data_files)
        if graph is None:
            return
        self.overwrite_start_goal_route(graph, big_cost)

        if not graph.is_euler_graph():
            print('ERROR: 入力がオイラーグラフではありません', file=sys.stderr)
            return

        try:
            route = self.generate_euler_route(graph)
            self.print_eulerian_route(route)
        except ValueError:
            print('ERROR: 最終ルートの作成に失敗しました。', file=sys.stderr)
            return

    def run_from_list(self, data_list_file: str, start_point: str, goal_point: str, show_route_list: bool) -> None:
        files = graph_file_loader.read_data_list(data_list_file)
        self.run(files, start_point, goal_point, show_route_list)

    ## オイラールートを生成し、結果を表示する。
    #  @param data_files      データファイルの場所のリスト。
    #  @param start_point     始点。
    #  @param goal_point      終点。
    #  @param show_route_list Trueのとき結果の全エッジリストをログに出力する。
    #  @exception ValueError 実行中に問題が発生したとき。
    def run(self, data_files: list[str], start_point: str, goal_point: str, show_route_list: bool) -> None:
        self.set_start_and_goal(start_point, goal_point)
        graph, big_cost, self.node_list = graph_file_loader.generate_graph_from_files(data_files)
        if graph is None:
            return
        self.show_loaded_data(graph)
        EulerianTask.show_start_goal(self.start_point, self.goal_point, self.node_list)
        self.overwrite_start_goal_route(graph, big_cost)

        try:
            graph = graph_to_eulerian_graph(graph)
        except ValueError as e:
            print(e, file=sys.stderr)
            return

        try:
            route = self.generate_euler_route(graph)
            self.print_result(route, graph.get_total_cost(), show_route_list)
        except ValueError:
            print('最終ルートの作成に失敗しました。', file=sys.stderr)
            return

    def set_start_and_goal(self, start: str, goal: str):
        self.start_point = start
        self.goal_point  = goal

    ## オイラールートを作る。
    #  @param graph オイラーグラフ。
    #  @return オイラールートになるノード列。
    def generate_euler_route(self, graph: AliasGraph) -> list[list[int]]:
        if self.start_point and self.start_point in self.node_list:
            start_node = self.node_list.index(self.start_point)
        else:
            start_node = -1
        route: list[list[int]] = eulerian_route_of_graph(graph, start_node)
        route: list[list[int]]  = [[n[0], n[1]] for n in route]
        if self.start_goal_edge is not None:
            route = EulerianTask.remove_added_edge(self.start_point, self.goal_point, self.node_list, route)
            graph.remove_edge(self.start_goal_edge)
        return route

    ## ノード数、エッジ数、ノードの一覧を表示する。
    #  @param graph グラフ。
    def show_loaded_data(self, graph: AliasGraph) -> None:
        print(f'ノード数: {graph.get_real_node_size()}  エッジ数: {graph.get_edge_size()}')

        index = 0
        print(self.node_list[index], end='')
        index += 1
        while index < graph.get_real_node_size():
            print(f', {self.node_list[index]}', end='')
            index += 1
            if index % 10 == 0:
                print()
        print()

    ## 始点と終点が指定されているとき、グラフにそれらをつなぐエッジを追加する。
    #  @param graph グラフ。
    #  @param big_cost 追加するエッジのコスト。
    def overwrite_start_goal_route(self, graph: AliasGraph, big_cost: Decimal) -> None:
        self.start_goal_edge = None
        if not (EulerianTask.is_valid_node_name(self.start_point, self.node_list) and EulerianTask.is_valid_node_name(self.goal_point, self.node_list)):
            return

        if self.start_point == self.goal_point:
            return

        self.start_goal_edge = Edge(self.node_list.index(self.start_point),
                        self.node_list.index(self.goal_point),
                        big_cost)
        graph.add_edge(self.start_goal_edge)

    ## ノード名が有効のときTrueを返す。
    #  有効とは、リストに登録されており、空文字列やNoneではないこと。
    #  Pure。
    #  @param name ノード名。
    #  @param node_list ノード名のリスト。
    #  @return     ノード名が有効のときTrue。
    @staticmethod
    def is_valid_node_name(name: str, node_list: list[str]) -> bool:
        if not name:
            return False

        return name in node_list

    ## (準)オイラーグラフを表示する。
    #  @param graph オイラーグラフ。
    def print_eulerian_graph(self, graph: AliasGraph) -> None:
        if self.start_goal_edge is not None:
            graph.remove_edge(self.start_goal_edge)

        self.sort_and_print_edges(graph)
        self.sort_and_print_transfers(graph)

    ## グラフのエッジをソートして一覧表示する。
    #  @param graph グラフ。
    def sort_and_print_edges(self, graph: AliasGraph) -> None:
        edges: list[tuple[str, str, Decimal]] = EulerianTask.generate_edge_list(graph, self.node_list)
        EulerianTask.sort_edges(edges)
        EulerianTask.print_edges(edges)

    ## グラフに含まれるエッジを(始点ノード名, 終点ノード名, コスト)の形式でリストにして返す。
    #  始点ノード名は終点ノード名よりも文字列比較で小さい値とする。
    #  Pure。
    #  @param graph グラフ。
    #  @param node_list ノード名のリスト。
    @staticmethod
    def generate_edge_list(graph: AliasGraph, node_list: list[str]) -> list[tuple[str, str, Decimal]]:
        edge_list = []
        for edge in graph.edge_generator():
            if node_list[edge.get_node1()] < node_list[edge.get_node2()]:
                edge_list.append((node_list[edge.get_node1()], node_list[edge.get_node2()], edge.get_cost()))
            else:
                edge_list.append((node_list[edge.get_node2()], node_list[edge.get_node1()], edge.get_cost()))
        return edge_list

    ## edgesの要素のインデックス[0], [1], [2]の優先順位でedgesを昇順に挿入ソートする。
    #  @param edges エッジデータのリスト。
    @staticmethod
    def sort_edges(edges: list[tuple[str, str, Decimal]]) -> None:
        for i in range(1, len(edges)):
            EulerianTask.insert(edges, i)

    ## a[index]をa[0]～a[index - 1]の適切な位置までシフトする。
    #  前提条件: a[0]～a[index - 1]は昇順にソートされている。
    #  @param a     昇順にソートするエッジデータのリスト。
    #  @param index シフトする対象データの位置。
    @staticmethod
    def insert(a: list[tuple[str, str, Decimal]], index: int) -> None:
        value = a[index]
        i = index - 1
        while i >= 0 and value < a[i]:
            a[i + 1] = a[i]
            i -= 1
        a[i + 1] = value

    ## エッジ情報のリストを画面に表示する。
    #  各エッジは始点、終点、コストを空白区切りで表示する。
    #  @param edges エッジ情報のリスト。
    @staticmethod
    def print_edges(edges: list[tuple[str, str, Decimal]]) -> None:
        for e in edges:
            print(f'{e[0]} {e[1]} {e[2]}')

    def sort_and_print_transfers(self, graph: AliasGraph) -> None:
        transfers = EulerianTask.generate_transfer_list(graph, self.node_list)
        EulerianTask.sort_edges(transfers)
        EulerianTask.print_transfers(transfers)

    ## グラフに含まれる同じとみなすノードを(ノード名, ノード名)の形式でリストにして返す。
    #  A、B、Cの3つのノードを同じとみなす場合、(A, B)、(B, C)、(A, C)の3つのデータをリストに加える。
    #  文字列比較で小さいノード名をタプルの先頭にする。
    #  Pure。
    #  @param graph グラフ。
    #  @param node_list ノード名のリスト。
    #  @return 同じとみなすノードの組み合わせのリスト。
    @staticmethod
    def generate_transfer_list(graph: AliasGraph, node_list: list[str]) -> list[tuple[str, str]]:
        transfer_list = []
        alias_dict: dict[int, set[int]] = graph.get_alias_dict()
        for v in alias_dict.values():
            for s, d in itertools.combinations(v, 2):
                if node_list[s] < node_list[d]:
                    transfer_list.append((node_list[s], node_list[d]))
                else:
                    transfer_list.append((node_list[d], node_list[s]))
        return transfer_list

    ## 同じとみなすノードの情報のリストを画面に表示する。
    #  各情報はノード1、ノード2、transferを空白区切りで表示する。
    #  @param edges 同じとみなすノードの情報のリスト。
    @staticmethod
    def print_transfers(transfers: list[tuple[str, str]]) -> None:
        for t in transfers:
            print(f'{t[0]} {t[1]} transfer')

    ## オイラー回路を表示する。
    #  @param route オイラールートのノードリスト。
    def print_eulerian_route(self, route: list[list[int]]) -> None:
        prev_from = route[0][0]
        prev_to   = route[0][1]
        print(self.node_list[prev_from])
        print(self.node_list[prev_to])
        index = 1

        while index < len(route):
            from_node = route[index][0]
            to_node   = route[index][1]
            if prev_to != from_node:
                print(self.node_list[from_node])
            print(self.node_list[to_node])
            index += 1
            prev_from = from_node
            prev_to   = to_node

    ## オイラールートの生成結果を表示する。
    #  @param route           オイラールートのノードリスト。
    #  @param total_cost      オイラールートの総コスト。
    #  @param show_route_list Trueのとき全エッジを表示。
    def print_result(self, route: list[list[int]], total_cost: Decimal, show_route_list: bool) -> None:
        print()
        print(f'最終エッジ数: {len(route)}')
        print(f'総コスト: {total_cost}')
        if show_route_list:
            EulerianTask.print_all_route(route, self.node_list)
        EulerianTask.print_euler_route(route, self.node_list)

    ## オイラー回路を表示する。
    #  @param route オイラールートのノードリスト。
    #  @param node_list ノード名のリスト。
    @staticmethod
    def print_euler_route(route: list[list[int]], node_list: list[str]) -> None:
        print('ルート例:')
        prev_from = route[0][0]
        prev_to   = route[0][1]
        print(f'{node_list[prev_from]} - {node_list[prev_to]}', end='')
        index = 1
        num_show = 2

        while index < len(route):
            from_node = route[index][0]
            to_node   = route[index][1]
            if prev_to != from_node:
                print(f' = {node_list[from_node]}', end='')
                num_show += 1
                if num_show % 10 == 0:
                    print()
            print(f' - {node_list[to_node]}', end='')
            index += 1
            num_show += 1
            if num_show % 10 == 0:
                print()
            prev_from = from_node
            prev_to   = to_node
        print()

    ## 全エッジを表示する。
    #  @param route オイラールートのノードリスト。
    #  @param node_list ノード名のリスト。
    @staticmethod
    def print_all_route(route: list[list[int]], node_list: list[str]) -> None:
        print()
        print('通過エッジ一覧:')
        print(f'{node_list[route[0][0]]} - {node_list[route[0][1]]}')
        for i in range(1, len(route)):
            if route[i][0] != route[i - 1][1]:
                print(f'{node_list[route[i - 1][1]]} = {node_list[route[i][0]]}')
            print(f'{node_list[route[i][0]]} - {node_list[route[i][1]]}')

        print()

    ## オイラールートから追加したダミールートを削除する。
    #  @param start_point ダミールートの始点のノード名。
    #  @param goal_point ダミールートの終点のノード名。
    #  @param node_list ノード名のリスト。
    #  @param route オイラールートのノードリスト。
    #  @return 削除後のノードリスト。
    @staticmethod
    def remove_added_edge(start_point: str, goal_point: str, node_list: list[str], route: list[list[int]]) -> list[list[int]]:
        start_node: int = node_list.index(start_point)
        goal_node: int  = node_list.index(goal_point)

        for i in range(len(route)):
            if route[i][0] == goal_node and route[i][1] == start_node:
                return route[i + 1:] + route[: i]
            if route[i][0] == start_node and route[i][1] == goal_node:
                new_route: list[list[int]] = []
                for j in range(i - 1, -1, -1):
                    new_route.append([route[j][1], route[j][0]])
                for j in range(len(route) - 1, i, -1):
                    new_route.append([route[j][1], route[j][0]])
                return new_route
        return None

    ## 始点と終点を表示する。
    #  @param start_point ダミールートの始点のノード名。
    #  @param goal_point ダミールートの終点のノード名。
    #  @param node_list ノード名のリスト。
    @staticmethod
    def show_start_goal(start_point, goal_point, node_list) -> None:
        if start_point:
            if start_point in node_list:
                print(f'始点: {start_point}', end='')
                if goal_point:
                    if goal_point in node_list:
                        print(f'  終点: {goal_point}')
                    else:
                        print(f'  \'{goal_point}\'が見つかりませんでした')
                else:
                    print()
            else:
                print(f'\'{start_point}\'が見つかりませんでした')

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
        self.show_start_goal()
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
            route = self.remove_added_edge(route)
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

    ## 始点と終点が指定されているとき、それらをつなぐコスト大のルートを追加する。
    #  ルートを追加したとき、Trueを返す。
    #  @param graph 対象グラフ。
    #  @return 始点-終点間のルートをデータに追加したときTrue。
    def overwrite_start_goal_route(self, graph: AliasGraph, big_cost: Decimal) -> None:
        self.start_goal_edge = None
        if not (self.is_valid_station_name(self.start_point) and self.is_valid_station_name(self.goal_point)):
            return

        if self.start_point == self.goal_point:
            return

        self.start_goal_edge = Edge(self.node_list.index(self.start_point),
                        self.node_list.index(self.goal_point),
                        big_cost)
        graph.add_edge(self.start_goal_edge)

    ## ノード名がデータにあればTrueを返す。
    #  @param name ノード名。
    #  @return     ノード名がデータにあればTrue。
    def is_valid_station_name(self, name: str) -> bool:
        if not name:
            return False

        if name in self.node_list:
            return True

        return False

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
        edges: list[tuple[str, str, Decimal]] = self.generate_edge_list(graph)
        EulerianTask.sort_edges(edges)
        EulerianTask.print_edges(edges)

    def generate_edge_list(self, graph: AliasGraph) -> list[tuple[str, str, Decimal]]:
        edge_list = []
        edge_ite = graph.edge_iterator()
        while True:
            try:
                edge: Edge = next(edge_ite)
                if self.node_list[edge.get_node1()] < self.node_list[edge.get_node2()]:
                    edge_list.append((self.node_list[edge.get_node1()], self.node_list[edge.get_node2()], edge.get_cost()))
                else:
                    edge_list.append((self.node_list[edge.get_node2()], self.node_list[edge.get_node1()], edge.get_cost()))
            except StopIteration:
                break
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
        transfers = self.generate_transfer_list(graph)
        EulerianTask.sort_edges(transfers)
        self.print_transfers(transfers)

    def generate_transfer_list(self, graph: AliasGraph) -> list[tuple[str, str]]:
        transfer_list = []
        alias_dict: dict[int, set[int]] = graph.get_alias_dict()
        for v in alias_dict.values():
            for s, d in itertools.combinations(v, 2):
                if self.node_list[s] < self.node_list[d]:
                    transfer_list.append((self.node_list[s], self.node_list[d]))
                else:
                    transfer_list.append((self.node_list[d], self.node_list[s]))
        return transfer_list

    def print_transfers(self, transfers: list[tuple[str, str]]) -> None:
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
            self.print_all_route(route)
        self.print_euler_route(route)

    ## オイラー回路を表示する。
    #  @param route オイラールートのノードリスト。
    def print_euler_route(self, route: list[list[int]]) -> None:
        print('ルート例:')
        prev_from = route[0][0]
        prev_to   = route[0][1]
        print(f'{self.node_list[prev_from]} - {self.node_list[prev_to]}', end='')
        index = 1
        num_show = 2

        while index < len(route):
            from_node = route[index][0]
            to_node   = route[index][1]
            if prev_to != from_node:
                print(f' = {self.node_list[from_node]}', end='')
                num_show += 1
                if num_show % 10 == 0:
                    print()
            print(f' - {self.node_list[to_node]}', end='')
            index += 1
            num_show += 1
            if num_show % 10 == 0:
                print()
            prev_from = from_node
            prev_to   = to_node
        print()

    ## 全エッジを表示する。
    #  @param route オイラールートのノードリスト。
    def print_all_route(self, route: list[list[int]]) -> None:
        print()
        print('通過エッジ一覧:')
        print(f'{self.node_list[route[0][0]]} - {self.node_list[route[0][1]]}')
        for i in range(1, len(route)):
            if route[i][0] != route[i - 1][1]:
                print(f'{self.node_list[route[i - 1][1]]} = {self.node_list[route[i][0]]}')
            print(f'{self.node_list[route[i][0]]} - {self.node_list[route[i][1]]}')

        print()

    ## オイラールートから追加したダミールートを削除する。
    #  @param route オイラールートのノードリスト。
    #  @return 削除後のノードリスト。
    def remove_added_edge(self, route: list[list[int]]) -> list[list[int]]:
        start_node: int = self.node_list.index(self.start_point)
        goal_node: int  = self.node_list.index(self.goal_point)

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
    def show_start_goal(self) -> None:
        if self.start_point:
            if self.start_point in self.node_list:
                print(f'始点: {self.start_point}', end='')
                if self.goal_point:
                    if self.goal_point in self.node_list:
                        print(f'  終点: {self.goal_point}')
                    else:
                        print(f'  \'{self.goal_point}\'が見つかりませんでした')
                else:
                    print()
            else:
                print(f'\'{self.start_point}\'が見つかりませんでした')

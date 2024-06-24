import sys
from decimal import Decimal
import fileinput

from edge import Edge
from alias_graph import AliasGraph

def read_data_list(data_list_file: str) -> list[str]:
    files: list[str] = []
    with fileinput.input(data_list_file, encoding='utf-8') as fin:
        for read_line in fin:
            line_data = remove_after_hash(read_line)
            files.append(line_data.strip())
    return files

def generate_graph_from_files(data_files: list[str]) -> tuple[AliasGraph | None, Decimal, list[str]]:
    graph = AliasGraph()
    transfer_list: list[set[int]] = []
    big_cost, node_list = load_data(graph, data_files, transfer_list)
    big_cost *= 5
    if big_cost < 0:
        return None, big_cost, []

    set_alias(graph, transfer_list, node_list)
    return graph, big_cost, node_list

## グラフデータを読み出す。
#  @param graph 読み出し先のグラフ。
#  @param data_file グラフデータのファイルパスの文字列。
#  @param transfer_list 同じとみなすノードのリスト
#  @return 読み出しに成功したときTrue。
def load_data(graph: AliasGraph, data_files: list[str], transfer_list: list[set[int]]) -> tuple[Decimal, list[str]]:
    graph.clear()
    node_list: list[str] = []
    transfer_list.clear()
    total_cost = Decimal(0)

    with fileinput.input(data_files, encoding='utf-8') as fin:
        try:
            for read_line in fin:
                line_data: list[str] = parse_read_line(read_line)
                if len(line_data) == 0:
                    continue
                elif len(line_data) != 3:
                    print(f'不正なデータがあります: {read_line}', file=sys.stderr)
                    return Decimal(-1), []

                add_new_nodes_to_nodelist(line_data, node_list)

                if line_data[2] == 'transfer':
                    add_transfer(line_data[0], line_data[1], transfer_list, node_list)
                else:
                    weight = Decimal(line_data[2])
                    if weight <= 0:
                        print(f'不正なデータがあります(コストは正の値): {read_line}', file=sys.stderr)
                        return Decimal(-1), []
                    edge = Edge(node_list.index(line_data[0]),
                                node_list.index(line_data[1]),
                                weight)
                    graph.add_edge(edge)
                    total_cost += weight
        except OSError:
            print('グラフデータの読み込み中にエラーが発生しました。', file=sys.stderr)
            print('(ファイルが存在しない、ファイルが壊れている、UTF-8で保存していない等。)', file=sys.stderr)
            return Decimal(-1), []
        except TypeError:
            print(f'不正なデータがあります(数値データが必要です): {read_line}', file=sys.stderr)
            return Decimal(-1), []

    return total_cost, node_list

def parse_read_line(read_line: str) -> list[str]:
    data_line = remove_after_hash(read_line)
    return data_line.split()

def remove_after_hash(s: str) -> str:
    hash_index = s.find('#')
    if hash_index >= 0:
        return s[: hash_index]
    return s

def add_new_nodes_to_nodelist(line_data: list[str], node_list: list[str]) -> None:
    if line_data[0] not in node_list:
        node_list.append(line_data[0])
    if line_data[1] not in node_list:
        node_list.append(line_data[1])

def add_transfer(node1: str, node2: str, transfer_list: list[set[int]], node_list: list[str]) -> None:
    transfer_list.append({node_list.index(node1), node_list.index(node2)})
    refresh_transfer(transfer_list)

def refresh_transfer(transfer_list: list[set[int]]) -> None:
    i = 0
    j = i + 1
    while i < len(transfer_list) - 1:
        while j < len(transfer_list):
            if transfer_list[i] & transfer_list[j]:
                transfer_list[i] |= transfer_list[j]
                transfer_list.pop(j)
                i = 0
                j = i
            j += 1
        i += 1
        j = i + 1

def set_alias(graph: AliasGraph, transfer_list: list[set[int]], node_list: list[str]) -> None:
    for s in transfer_list:
        alias_node = len(node_list)
        node_list.append(str(alias_node))
        for node in s:
            graph.set_alias_node(node, alias_node)

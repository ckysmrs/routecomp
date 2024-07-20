from decimal import Decimal

from edge import Edge

## ダイクストラ法での探索に使用するノード。
class DijkstraNode:
    ## ダイクストラ法用のノードを構築する。
    #  @param id このノードのID。
    def __init__(self, id: int):
        self.id: int = id
        self.score: Decimal = Decimal('Infinity')
        self.parent_node: 'DijkstraNode' = None
        self.edge_list: list[Edge] = []

    ## このノードから行けるノードを展開する。
    #  @param node_list  ノードリスト。
    #  @param open_list  探索中ノードリスト。
    def expand(self, node_list: list['DijkstraNode'], open_list: list['DijkstraNode']) -> None:
        for e in self.edge_list:
            destination = self.get_destination(e, node_list)
            if destination is not None:
                destination.open(self, self.score + e.get_cost(), open_list)

        if self in open_list:
            open_list.remove(self)

    ## このノードのスコアと始点ノードを更新する。
    #  @param parent_node このノードへの始点ノード。
    #  @param new_score   このノードまでのスコア。
    #  @param open_list   探索中ノードリスト。
    def open(self, parent_node: 'DijkstraNode', new_score: Decimal, open_list: list['DijkstraNode']) -> None:
        if self in open_list:
            if new_score < self.score:
                self.parent_node = parent_node
                self.score = new_score

    ## このノードから指定の辺で行けるノードを返す。
    #  @param edge      このノードに接続された辺。
    #  @param node_list ノードリスト。
    #  @return このノードから指定の辺で行けるノード。
    def get_destination(self, edge: Edge, node_list: list['DijkstraNode']) -> 'DijkstraNode':
        destination_id: int = edge.get_node1()
        if destination_id == self.id:
            destination_id = edge.get_node2()

        return DijkstraNode.get_dijkstra_node_by_id(node_list, destination_id)

    ## このノードに接続された辺を追加する。
    #  @param edge 追加する辺。
    def add_edge(self, edge: Edge) -> None:
        self.edge_list.append(edge)

    ## IDを返す。
    #  @return ID。
    def get_id(self) -> int:
        return self.id

    ## このノードのスコアを返す。
    #  @return このノードのスコア。
    def get_score(self) -> Decimal:
        return self.score

    ## 親ノードを返す。
    #  @return 親ノード。
    def get_parent_node(self) -> 'DijkstraNode':
        return self.parent_node

    ## このノードから指定IDのノードまでのコストを返す。
    #  @param destination_id 行き先ノードのID。
    #  @return このノードから指定IDのノードまでのコスト。
    def get_weight(self, destination_id: int) -> Decimal:
        weight: Decimal = Decimal(100000)
        for e in self.edge_list:
            node_id: int = e.get_node1()
            if node_id == self.id:
                node_id = e.get_node2()
            if node_id == destination_id:
                weight = e.get_cost()
        return weight

    ## ダイクストラノードをIDで検索する。
    #  @param node_list ノードリスト。
    #  @param id 探索するID。
    #  @return 指定されたIDのダイクストラノード。
    #          存在しないときはNoneを返す。
    @staticmethod
    def get_dijkstra_node_by_id(node_list: list['DijkstraNode'], id: int) -> 'DijkstraNode':
        for dijkstra_node in node_list:
            if dijkstra_node.get_id() == id:
                return dijkstra_node

        return None

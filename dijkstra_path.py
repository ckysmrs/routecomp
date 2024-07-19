from decimal import Decimal

from dijkstra_node import DijkstraNode

## DijkstraNodeのパス。
class DijkstraPath:
    def __init__(self):
        self.path: list[DijkstraNode] = []

    ## パスの最後に指定されたノードを追加する。
    #  @param node このパスに追加されるノード。
    def add(self, node: DijkstraNode) -> None:
        self.path.append(node)

    ## このパス内の指定された位置に指定されたノードを挿入する。その位置とそれ以降にノードがあればそれらを右に移動させ、各要素のインデックスに1を加える。
    #  @param index 指定のノードが挿入される位置のインデックス。
    #  @param node  挿入されるノード。
    def insert(self, index: int, node: DijkstraNode) -> None:
        self.path.insert(index, node)

    ## このパス内の指定された位置にあるノードを返す。
    #  @param index 返されるノードのインデックス。
    #  @return このパス内の指定された位置にあるノード。
    def __getitem__(self, index: int) -> DijkstraNode:
        return self.path[index]

    ## このパス内にあるノードの数を返す。
    #  @return このパス内のノード数。
    def __len__(self) -> int:
        return len(self.path)

    ## パスの総コストを返す。
    #  @return パスの総コスト。
    def get_cost(self) -> Decimal:
        cost: Decimal = Decimal(0)
        path_size: int = len(self.path)

        if path_size >= 2:
            for i in range(path_size - 1):
                weight: Decimal = self.path[i].get_weight(self.path[i + 1].get_id())
                cost += weight

        return cost

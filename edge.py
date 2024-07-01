from dataclasses import dataclass
from decimal import Decimal

## コスト付き無向エッジ。
#  Immutable。
@dataclass(frozen=True)
class Edge:
    node1: int  # ノード(0以上の整数)。
    node2: int  # ノード(0以上の整数)。
    cost: Decimal  # コスト(正の値)。

    ## コンストラクタの引数チェック。
    #  @exception ValueError 引数の値が不正のとき。
    def __post_init__(self):
        if not self.is_valid_arguments(self.node1, self.node2, self.cost):
            raise ValueError(f'Edge constructor: node = ({self.node1}, {self.node2}), cost = {self.cost} is invalid.')

    ## 引数の値が辺の値として適性のときTrueを返す。
    #  @param node1 ノード。
    #  @param node2 ノード。
    #  @param cost  コスト。
    #  @return 引数の値が適性の時True。
    def is_valid_arguments(self, node1: int, node2: int, cost: Decimal) -> bool:
        if not isinstance(node1, int):
            return False
        if not isinstance(node2, int):
            return False
        return node1 >= 0 and node2 >= 0 and cost > 0

    def get_node1(self) -> int:
        return self.node1

    def get_node2(self) -> int:
        return self.node2

    ## コストを返す。
    #  @return コスト。
    def get_cost(self) -> Decimal:
        return self.cost

    ## この辺について、指定されたノードと反対側のノードを返す。
    #  この辺が接続していないノードが指定されたときはNoneを返す。
    #  @param node 指定ノード。
    #  @return 指定ノードの反対側のノード。
    def get_paired_node(self, node: int) -> int | None:
        if node == self.node1:
            return self.node2
        if node == self.node2:
            return self.node1

        return None

    def __eq__(self, o):
        if o is None:
            return False
        if not isinstance(o, Edge):
            return False
        if self.cost != o.cost:
            return False
        if o.node1 == self.node1 and o.node2 == self.node2:
            return True
        if o.node1 == self.node2 and o.node2 == self.node1:
            return True
        return False

    def __hash__(self):
        min_node = min(self.node1, self.node2)
        max_node = max(self.node1, self.node2)
        result = 17
        result = 31 * result + min_node
        result = 31 * result + max_node
        result = 31 * result + self.cost
        return hash(result)

    ## この辺が指定のノードを含んでいるとき、Trueを返す。
    #  @param node ノード。
    #  @return この辺が指定のノードを含むときTrue。
    def contains_node(self, node: int) -> bool:
        if self.node1 == node:
            return True
        if self.node2 == node:
            return True
        return False

    ## この辺が指定の2ノードを含んでいるとき、Trueを返す。
    #  @param node1 ノード。
    #  @param node2 ノード。
    #  @return この辺が指定の2ノードを含むときTrue。
    def contains_nodes(self, node1: int, node2: int) -> bool:
        if self.node1 == node1 and self.node2 == node2:
            return True
        if self.node1 == node2 and self.node2 == node1:
            return True
        return False

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}('
                f'{self.node1!r}, {self.node2!r}, {self.cost!r})')

    def __str__(self) -> str:
        return f'[{self.node1} - {self.node2}, cost: {self.cost}]'

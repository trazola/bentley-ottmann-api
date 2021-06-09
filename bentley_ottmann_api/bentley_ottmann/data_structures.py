from bisect import bisect_left, bisect_right
from heapq import heappop, heappush, heapify
from typing import Optional, Any, Iterable


class PriorityQueue:
    """
    Priority Queue based on heapq.
    """

    def __init__(self, initial_data: Optional[list] = None) -> None:
        self.heapq = []
        if initial_data:
            self.heapq = initial_data
            heapify(self.heapq)

    def remove_by_object_id(self, data: Any) -> None:
        """
        Method removes element from queue by object id.

        Args:
            data: data to remove

        Returns:
            `None`
        """
        for idx, element in enumerate(self):
            if id(element) == id(data):
                del self.heapq[idx]
                heapify(self.heapq)
                break
        heapify(self.heapq)

    def enqueue(self, data: Any) -> None:
        """
        Method pushes data to queue.

        Args:
            data: data to pushed

        Returns:
            `None`
        """
        heappush(self.heapq, data)

    def dequeue(self) -> Any:
        """
        Method popes data to queue.

        Returns:
            element from queue
        """
        try:
            return heappop(self.heapq)
        except IndexError:
            raise Exception("Queue is empty.")

    def __bool__(self) -> bool:
        return bool(self.heapq)

    def __iter__(self):
        return iter(self.heapq)

    def __len__(self) -> int:
        return len(self.heapq)

    def __repr__(self) -> str:
        return str(self.heapq)

    def __contains__(self, item):
        return item in self.heapq


class Node:
    """
    Node class for AVL Tree.
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.parent: Optional[Node] = None
        self.left_child: Optional[Node] = None
        self.right_child: Optional[Node] = None
        self.height = 0

    @property
    def is_leaf(self) -> bool:
        """
        Check node is leaf.
        
        Returns:
            `True` if is leaf otherwise `False`
        """
        return self.height == 0

    def get_max_children_height(self) -> int:
        """
        Method returns max children height.

        Returns:
            max children height
        """
        if self.left_child and self.right_child:
            return max(self.left_child.height, self.right_child.height)
        if self.left_child:
            return self.left_child.height
        if self.right_child:
            return self.right_child.height
        return -1

    def balance(self) -> int:
        """
        Method returns balance node value

        Returns:
            balance value.
        """

        def get_height_for_child(child):
            return child.height if child else -1

        left_child_height, right_child_height = (
            get_height_for_child(child=self.left_child),
            get_height_for_child(child=self.right_child),
        )
        return left_child_height - right_child_height

    def get_children_and_parent(self) -> tuple[Any, Any, Any]:
        """
        Method returns children with parent for node.

        Returns:
            (`right_child`, `left_child`, `parent`)
        """
        return self.right_child, self.left_child, self.parent

    def __repr__(self) -> str:
        return str(self.key)


class BaseTree:
    def __init__(self, initial_data: Optional[Iterable] = None) -> None:
        self.root_node: Optional[Node] = None
        self.nodes = 0
        self.rebalances = 0
        if initial_data:
            for data in initial_data:
                self.insert(key=data)

    def insert(self, key: Any) -> Any:
        raise NotImplementedError

    def find(self, key: Any) -> Any:
        raise NotImplementedError

    def __len__(self):
        return 0 if self.root_node is None else self.root_node.height


class AVLRebalanceMixin:
    """
    AVL Rebalance Mixin
    """

    def _set_new_child(
        self,
        initial_parent: Optional[Node],
        initial_node: Optional[Node],
        new_node: Optional[Node],
    ) -> None:
        """
        Method sets child.

        Args:
            initial_parent: initial parent
            initial_node: initial node
            new_node: new node

        Returns:

        """
        if initial_parent is None:
            self.root_node = new_node
            self.root_node.parent = None
            return
        if initial_parent.right_child == initial_node:
            initial_parent.right_child = new_node
        else:
            initial_parent.left_child = new_node
        new_node.parent = initial_parent

    def rebalance_case_rrc(self, initial_node: Node, initial_parent: Optional[Node]) -> None:
        """
        Methods rebalances AVL tree for `RRC` case.

        Args:
            initial_node: initial node
            initial_parent: initial parent

        Returns:
            `None`
        """
        right = initial_node.right_child
        initial_node.right_child = right.left_child
        if initial_node.right_child:
            initial_node.right_child.parent = initial_node
        right.left_child = initial_node
        initial_node.parent = right
        self._set_new_child(
            initial_parent=initial_parent, initial_node=initial_node, new_node=right
        )
        self.recompute_heights(initial_node)
        self.recompute_heights(right.parent)

    def rebalance_case_rlc(self, initial_node: Node, initial_parent: Optional[Node]) -> None:
        """
        Methods rebalances AVL tree for `RLC` case.

        Args:
            initial_node: initial node
            initial_parent: initial parent

        Returns:
            `None`
        """
        right = initial_node.right_child
        left = right.left_child
        right.left_child = left.right_child
        if right.left_child:
            right.left_child.parent = right
        initial_node.right_child = left.left_child
        if initial_node.right_child:
            initial_node.right_child.parent = initial_node
        left.right_child = right
        right.parent = left
        left.left_child = initial_node
        initial_node.parent = left
        self._set_new_child(
            initial_node=initial_node, initial_parent=initial_parent, new_node=left
        )
        self.recompute_heights(initial_node)
        self.recompute_heights(right)

    def rabalance_case_llc(self, initial_node: Node, initial_parent: Optional[Node]) -> None:
        """
        Methods rebalances AVL tree for `LLC` case.

        Args:
            initial_node: initial node
            initial_parent: initial parent

        Returns:
            `None`
        """
        left = initial_node.left_child
        initial_node.left_child = left.right_child
        if initial_node.left_child:
            initial_node.left_child.parent = initial_node
        left.right_child = initial_node
        initial_node.parent = left
        self._set_new_child(
            initial_parent=initial_parent, initial_node=initial_node, new_node=left
        )
        self.recompute_heights(initial_node)
        self.recompute_heights(left.parent)

    def rabalance_case_lrc(self, initial_node: Node, initial_parent: Optional[Node]) -> None:
        """
        Methods rebalances AVL tree for `LLC` case.

        Args:
            initial_node: initial node
            initial_parent: initial parent

        Returns:
            `None`
        """
        left = initial_node.left_child
        right = left.right_child
        initial_node.left_child = right.right_child
        if initial_node.left_child:
            initial_node.left_child.parent = initial_node
        left.right_child = right.left_child
        if left.right_child:
            left.right_child.parent = left
        right.left_child = left
        left.parent = right
        right.right_child = initial_node
        initial_node.parent = right
        self._set_new_child(
            initial_parent=initial_parent, initial_node=initial_node, new_node=right
        )
        self.recompute_heights(initial_node)
        self.recompute_heights(left)

    def rebalance(self, node: Node) -> None:
        """
        Method rebalances AVL Tree for node.

        Args:
            node: node

        Returns:
            `None`
        """
        self.rebalances += 1
        initial_node = node
        initial_parent = initial_node.parent
        if node.balance() == -2:
            if node.right_child.balance() <= 0:
                return self.rebalance_case_rrc(
                    initial_node=initial_node, initial_parent=initial_parent
                )
            return self.rebalance_case_rlc(
                initial_node=initial_node, initial_parent=initial_parent
            )
        if node.left_child.balance() >= 0:
            return self.rabalance_case_llc(
                initial_node=initial_node, initial_parent=initial_parent
            )
        return self.rabalance_case_lrc(initial_node=initial_node, initial_parent=initial_parent)


class AVLTree(AVLRebalanceMixin, BaseTree):
    """
    AVL Tree class.
    """

    @staticmethod
    def recompute_heights(node: Node) -> None:
        """
        Method recomputes heights.

        Args:
            node: started node

        Returns:
            `None`
        """
        changed, start_node = True, node
        while start_node and changed:
            old_height = start_node.height
            node_max_children_height = start_node.get_max_children_height() + 1
            start_node.height = (
                node_max_children_height
                if (start_node.right_child or start_node.left_child)
                else 0
            )
            changed = start_node.height != old_height
            start_node = start_node.parent

    def find_in_subtree(self, node: Optional[Node], key: Any) -> Optional[Node]:
        """
        Methods find key in subtree.

        Args:
            node: node
            key: search key

        Returns:
            searched node about give node if exists otherwise `None`
        """
        if node is None:
            return None
        if key < node.key:
            return self.find_in_subtree(node.left_child, key)
        if key > node.key:
            return self.find_in_subtree(node.right_child, key)
        return node

    def find(self, key: Any) -> Optional[Node]:
        """
        Method finds node about given key.

        Args:
            key: search key

        Returns:
            searched node about give node if exists otherwise `None`
        """
        return self.find_in_subtree(node=self.root_node, key=key)

    def insert_child(self, parent_node: Node, child_node: Node) -> None:
        """
        Method inserts child node for parent node.

        Args:
            parent_node: parent node
            child_node: child node

        Returns:
            `None`
        """

        def get_one_node(parent_node):
            if parent_node.height == 0:
                node = parent_node
                while node:
                    node.height = node.get_max_children_height() + 1
                    if node.balance() not in [-1, 0, 1]:
                        return node
                    node = node.parent
            return

        node = None
        if child_node.key < parent_node.key:
            if parent_node.left_child:
                self.insert_child(parent_node=parent_node.left_child, child_node=child_node)
            else:
                parent_node.left_child = child_node
                child_node.parent = parent_node
                node = get_one_node(parent_node=parent_node)
        else:
            if right_child := parent_node.right_child:
                self.insert_child(parent_node=right_child, child_node=child_node)
            else:
                parent_node.right_child = child_node
                child_node.parent = parent_node
                node = get_one_node(parent_node=parent_node)
        if node:
            self.rebalance(node)

    def insert(self, key: Any) -> Optional[None]:
        """
        Method insets key to AVL tree.

        Args:
            key: key to insert

        Returns:
            `None`
        """
        new_node = Node(key=key)
        if self.root_node is None:
            self.root_node = new_node
            return new_node
        if self.find(key=key) is None:
            self.nodes += 1
            self.insert_child(parent_node=self.root_node, child_node=new_node)
            return new_node

    def get_left(self, node: Node) -> Optional[Node]:
        """
        Methods returns left node for node.

        Args:
            node: node

        Returns:
            left node for node if exists otherwise `None`
        """
        initial_node = node
        if initial_node is None:
            return None
        if initial_node.left_child is None:
            while initial_node.parent is not None:
                if initial_node.parent.right_child == initial_node:
                    return initial_node.parent
                initial_node = initial_node.parent
            return initial_node.parent
        initial_node = initial_node.left_child
        while initial_node.right_child is not None:
            initial_node = initial_node.right_child
        return initial_node

    def get_right(self, node: Node) -> Optional[Node]:
        """
        Methods returns right node for node.

        Args:
            node: node

        Returns:
            right node for node if exists otherwise `None`
        """
        initial_node = node
        if initial_node is None:
            return None
        if initial_node.right_child is None:
            while initial_node.parent is not None:
                if initial_node.parent.left_child == node:
                    return initial_node.parent
                initial_node = initial_node.parent
            return initial_node.parent
        initial_node = initial_node.right_child
        while initial_node.left_child is not None:
            initial_node = initial_node.left_child
        return initial_node

    def rebalance_all_nodes(self, node: Node) -> None:
        """
        Method rebalances all nodes.

        Args:
            node: node

        Returns:
            `None`
        """
        initial_node = node
        while initial_node:
            if initial_node.balance() not in [-1, 0, 1]:
                self.rebalance(node=initial_node)
            initial_node = initial_node.parent

    @staticmethod
    def set_value_for_parent_children(parent: Node, node: Node, value: Optional[Node]) -> None:
        """
        Method sets value foe parent children.

        Args:
            parent: parent
            node: node
            value: value

        Returns:
            `None`
        """
        if parent.left_child == node:
            parent.left_child = value
            return
        parent.right_child = value

    def remove_leaf(self, node: Node) -> None:
        """
        Methods remove leaf.

        Args:
            node: node to delete

        Returns:
            `None`
        """
        parent = node.parent
        if parent:
            self.set_value_for_parent_children(parent=parent, node=node, value=None)
            self.recompute_heights(node=parent)
        else:
            self.root_node = None
        del node
        self.rebalance_all_nodes(node=parent)

    def remove_branch(self, node: Node) -> None:
        """
        Method remove branch.

        Args:
            node: node to delete

        Returns:
            `None`
        """
        parent = node.parent
        left_child, right_child = node.left_child, node.right_child
        if parent:
            self.set_value_for_parent_children(
                parent=parent, node=node, value=node.right_child or node.left_child
            )
            if node.left_child:
                node.left_child.parent = parent
            else:
                node.right_child.parent = parent
            self.recompute_heights(node=parent)
        del node
        if parent:
            self.rebalance_all_nodes(node=parent)
            return
        if left_child:
            self.root_node = left_child
        else:
            self.root_node = right_child
        self.root_node.parent = None

    def find_smallest(self, node: Node) -> Node:
        """
        Method returns smallest node for node

        Args:
            node: node

        Returns:
            smallest node
        """
        initial_node = node
        while initial_node.left_child:
            initial_node = initial_node.left_child
        return initial_node

    def swap_nodes(self, first_node: Node, second_node: Node) -> None:
        """
        Method swaps nodes.

        Args:
            first_node: first node
            second_node: second node

        Returns:
            `None`
        """
        first_right_child, first_left_child, first_parent = first_node.get_children_and_parent()
        (
            second_right_child,
            second_left_child,
            second_parent,
        ) = second_node.get_children_and_parent()
        first_node.height, second_node.height = second_node.height, first_node.height
        if first_parent:
            self.set_value_for_parent_children(
                parent=first_parent, node=first_node, value=second_node
            )
            second_node.parent = first_parent
        else:
            self.root_node = second_node
            second_node.parent = None
        second_node.left_child = first_left_child
        first_left_child.parent = second_node
        first_node.left_child = second_left_child  # None
        first_node.right_child = second_right_child
        if second_right_child:
            second_right_child.parent = first_node
        if not (second_parent == first_node):
            second_node.right_child = first_right_child
            first_right_child.parent = second_node
            second_parent.left_child = first_node
            first_node.parent = second_parent
        else:
            second_node.right_child = first_node
            first_node.parent = second_node

    def swap_with_successor_and_remove(self, node: Node) -> None:
        """
        Method swaps with successor and remove.

        Args:
            node: node

        Returns:
            `None`
        """
        self.swap_nodes(first_node=node, second_node=self.find_smallest(node.right_child))
        if node.is_leaf:
            return self.remove_leaf(node=node)
        return self.remove_branch(node=node)

    def remove_node(self, node: Node) -> None:
        """
        Method removes node.

        Args:
            node: node

        Returns:
            `None`
        """
        if node is None:
            return
        self.nodes -= 1
        if node.is_leaf:
            return self.remove_leaf(node)
        if bool(node.left_child) ^ bool(node.right_child):
            return self.remove_branch(node)
        return self.swap_with_successor_and_remove(node)

    def remove_key(self, key: Any) -> None:
        """
        Method removes key from tree.

        Args:
            key: key

        Returns:
            `None`
        """
        return self.remove_node(node=self.find(key))

    def inorder(
        self, node: Node, result: Optional[list] = None, node_in_output: bool = False
    ) -> list[Any]:
        """
       Method traverses the tree in `inorder`.

        Args:
            node: node
            result: result
            node_in_output: if `True` method returns node otherwise only values.

        Returns:
            results
        """
        if result is None:
            result = []
        if node is None:
            return result
        if node.left_child:
            result = self.inorder(node.left_child, result, node_in_output)
        if node_in_output:
            result.append(node)
        else:
            result.append(node.key)
        if node.right_child:
            result = self.inorder(node.right_child, result, node_in_output)
        return result

    def lower(self, key: Any) -> Optional[Any]:
        """
        Method returns the greatest element in this set strictly
            less than the given element, or null if there is no such element.

        Args:
            key: key

        Returns:
            item if found
        """
        if self.root_node is None:
            return
        elements = self.inorder(node=self.root_node)
        index = bisect_left(elements, key)
        if index:
            return elements[index - 1]
        return None

    def higher(self, key: Any) -> None:
        """
        Method returns the least element in this set strictly
            greater than the given element, or null if there is no such element.

        Args:
            key: key

        Returns:
            item if found
        """
        if self.root_node is None:
            return
        elements = self.inorder(node=self.root_node)
        index = bisect_right(elements, key)
        if index > len(elements) - 1:
            return
        return elements[index]

# Red-Black Tree implementation for MyStok application

from typing import Optional, List, Tuple
from .stock import Stock


class Node:
    # Node class for Red-Black Tree
    
    def __init__(self, score: float, stock_data: Stock):
        # Initialize a Red-Black Tree node
        self.score = score
        self.stock_data = stock_data
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None
        self.color = "RED" 
    
    def __str__(self) -> str:
        return f"Node(score={self.score}, color={self.color})"


class RedBlackTree:
    
    def __init__(self):
        self.root: Optional[Node] = None
        self.size = 0
    
    def insert(self, score: float, stock_data: Stock) -> bool:
        new_node = Node(score, stock_data)
        
        if self.root is None:
            self.root = new_node
            new_node.color = "BLACK" 
        else:
            current = self.root
            parent = None
            
            while current is not None:
                parent = current
                if score < current.score:
                    current = current.left
                else:
                    current = current.right
            
            new_node.parent = parent
            if score < parent.score:
                parent.left = new_node
            else:
                parent.right = new_node
            
            self.fix_insert(new_node)
        
        self.size += 1
        return True
    
    def fix_insert(self, node: Node):
        while node.parent is not None and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.left_rotate(node.parent.parent)
        
        self.root.color = "BLACK"
    
    def left_rotate(self, node: Node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child
    
    def right_rotate(self, node: Node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child
    
    def search(self, score: float) -> Optional[Stock]:
        current = self.root
        while current is not None:
            if score == current.score:
                return current.stock_data
            elif score < current.score:
                current = current.left
            else:
                current = current.right
        return None
    
    def get_stocks_in_range(self, min_score: float, max_score: float) -> List[Tuple[float, Stock]]:
        result = []
        self.range_search_helper(self.root, min_score, max_score, result)
        return result
    
    def range_search_helper(self, node: Optional[Node], min_score: float, max_score: float, result: List[Tuple[float, Stock]]):
        if node is None:
            return

        if min_score < node.score:
            self.range_search_helper(node.left, min_score, max_score, result)
        
        if min_score <= node.score <= max_score:
            result.append((node.score, node.stock_data))

        if max_score > node.score:
            self.range_search_helper(node.right, min_score, max_score, result)
    
    def get_size(self) -> int:
        return self.size
    
    def is_empty(self) -> bool:
        return self.root is None 
# Max Heap implementation for MyStok application

from typing import List, Tuple, Optional
from .stock import Stock


class MaxHeap:
    def __init__(self):
        self.heap: List[Tuple[float, Stock]] = []
    
    def insert(self, score: float, stock_data: Stock) -> None:
        self.heap.append((score, stock_data))
        self.heapify_up(len(self.heap) - 1)
    
    def extract_max(self) -> Optional[Tuple[float, Stock]]:
        if not self.heap:
            return None
        
        max_item = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if self.heap:
            self.heapify_down(0)
        
        return max_item
    
    def get_top_k(self, k: int) -> List[Tuple[float, Stock]]:
        if k <= 0:
            return []
    
        temp_heap = MaxHeap()
        temp_heap.heap = self.heap.copy()
        
        result = []
        for _ in range(min(k, len(temp_heap.heap))):
            item = temp_heap.extract_max()
            if item is not None:
                result.append(item)
        
        return result
    
    def peek_max(self) -> Optional[Tuple[float, Stock]]:
        return self.heap[0] if self.heap else None
    
    def heapify_up(self, index: int) -> None:
        parent = (index - 1) // 2
        if parent >= 0 and self.heap[index][0] > self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.heapify_up(parent)
    
    def heapify_down(self, index: int) -> None:
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
            largest = left
        
        if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
            largest = right
        
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self.heapify_down(largest)
    
    def build_heap(self, items: List[Tuple[float, Stock]]) -> None:
        self.heap = items.copy()
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.heapify_down(i)
    
    def get_size(self) -> int:
        return len(self.heap)
    
    def is_empty(self) -> bool:
        return len(self.heap) == 0
    
    def clear(self) -> None:
        self.heap.clear() 
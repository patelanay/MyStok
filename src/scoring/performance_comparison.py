import time
from typing import List, Tuple, Dict, Any
from ..data_structures.stock import Stock
from ..data_structures.red_black_tree import RedBlackTree
from ..data_structures.max_heap import MaxHeap
from .stock_scorer import StockScorer


class PerformanceComparator:
    # Compares performance between Red-Black Tree and Max Heap data structures
    
    def __init__(self):
        self.red_black_tree = RedBlackTree()
        self.max_heap = MaxHeap()
    
    def compare_performance(self, stocks: List[Stock], risk_profile: str, time_investment: str, sector_preference: str, top_k: int = 10) -> Dict[str, Any]:
        scorer = StockScorer(risk_profile, time_investment, sector_preference)
        
        # Filter stocks by sector
        sector_stocks = scorer.filter_by_sector(stocks)
        
        if not sector_stocks:
            return {
                "error": "No stocks found for the selected sector", "red_black_tree": {}, "max_heap": {}
            }
        
        # Score all stocks based on user input
        scored_stocks = scorer.score_stocks(sector_stocks)
        
        # Test Red-Black Tree performance
        rb_results = self.test_red_black_tree(scored_stocks, top_k)
        
        # Test Max Heap performance
        heap_results = self.test_max_heap(scored_stocks, top_k)
        
        return {
            "red_black_tree": rb_results,
            "max_heap": heap_results,
            "total_stocks": len(sector_stocks)
        }
    
    def test_red_black_tree(self, scored_stocks: List[Tuple[float, Stock]], top_k: int) -> Dict[str, Any]:
        start_time = time.time()
        
        self.red_black_tree = RedBlackTree()
        
        # Insert all stocks
        for score, stock in scored_stocks:
            self.red_black_tree.insert(score, stock)
        
        # Get top stock recommendations
        if scored_stocks:
            max_score = max(score for score, _ in scored_stocks)
            min_score = max_score - 100 
            top_stocks = self.red_black_tree.get_stocks_in_range(min_score, max_score)
            # Sort by score
            top_stocks.sort(key=lambda x: x[0], reverse=True)
            top_stocks = top_stocks[:top_k]
        else:
            top_stocks = []
        
        total_time = time.time() - start_time
        
        return {
            "total_time": total_time,
            "top_stocks": top_stocks,
            "tree_size": self.red_black_tree.get_size()
        }
    
    def test_max_heap(self, scored_stocks: List[Tuple[float, Stock]], top_k: int) -> Dict[str, Any]:
        # Test Max Heap performance
        start_time = time.time()
        
        self.max_heap = MaxHeap()
        
        # Insert all stocks
        for score, stock in scored_stocks:
            self.max_heap.insert(score, stock)
        
        top_stocks = self.max_heap.get_top_k(top_k)
        
        total_time = time.time() - start_time
        
        return {
            "total_time": total_time,
            "top_stocks": top_stocks,
            "heap_size": self.max_heap.get_size()
        }
    
    def get_performance_summary(self, results: Dict[str, Any]) -> str:
        # Make a performance comparison summary
        if "error" in results:
            return results["error"]
        
        rb_time = results["red_black_tree"]["total_time"]
        heap_time = results["max_heap"]["total_time"]
        
        if rb_time < heap_time:
            winner = "Red-Black Tree"
            diff = heap_time - rb_time
        else:
            winner = "Max Heap"
            diff = rb_time - heap_time
        
        summary = f"\nPerformance Comparison:\nRed-Black Tree: {rb_time:.6f}s\nMax Heap: {heap_time:.6f}s\nWinner: {winner} ({diff:.6f}s faster)\n"
        
        return summary 
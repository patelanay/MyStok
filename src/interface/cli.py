
#Terminal interface for MyStok application.

import sys
from typing import List, Tuple, Dict, Any
from ..data_processing.data_loader import DataLoader
from ..data_processing.sector_grouper import SectorGrouper
from ..data_structures.red_black_tree import RedBlackTree
from ..data_structures.max_heap import MaxHeap
from ..scoring.stock_scorer import StockScorer
from ..scoring.performance_comparison import PerformanceComparator
from ..data_structures.stock import Stock


class MyStokCLI:
    # Terminal-based user interface for MyStok application
    
    def __init__(self, csv_path: str = "resources/World-Stock-Prices-Dataset.csv"):
        # Make CLI
        self.data_loader = DataLoader(csv_path)
        self.sector_grouper = SectorGrouper()
        self.red_black_tree = RedBlackTree()
        self.max_heap = MaxHeap()
        self.performance_comparator = PerformanceComparator()
        self.stocks = []
    
    def run(self) -> None:
        # Main application loop
        print("Welcome to MyStok - Stock Recommendation System")
        print("Team: Project 3 Group 55")
        print("Members: James Jean Philipe, Ignatius Martin, Anay Patel")
        
        try:
            # Load data
            print("\nLoading stock data...")
            self.stocks = self.data_loader.load_stocks()
            
            if not self.stocks:
                print("Error: No stock data loaded. Please check the CSV file.")
                return
            
            print(f"Successfully loaded {len(self.stocks)} stocks.")
            
            # Get user inputs
            risk_profile = self.get_risk_profile()
            time_investment = self.get_time_investment()
            sector_preference = self.get_sector_preference()
            data_structure_choice = self.get_data_structure_choice()
            
            # Process and display recommendations 
            if data_structure_choice == "compare":
                self.compare_performance(risk_profile, time_investment, sector_preference)
            else:
                recommendations = self.get_recommendations(risk_profile, time_investment, sector_preference, data_structure_choice)
                self.display_recommendations(recommendations, data_structure_choice)
            
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
        except Exception as e:
            print(f"\nError: {e}")
    
    def get_risk_profile(self) -> str:
        # Get user risk profile preference
        print("\nRisk Profile:")
        print("1. Low (Conservative) - Prefer stable, low-volatility stocks")
        print("2. Medium (Balanced) - Moderate risk tolerance")
        print("3. High (Aggressive) - Comfortable with high volatility")
        
        while True:
            try:
                choice = input("Enter your choice (1-3): ").strip()
                if choice == "1":
                    return "low"
                elif choice == "2":
                    return "medium"
                elif choice == "3":
                    return "high"
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                sys.exit(0)
    
    def get_time_investment(self) -> str:
        # Get user time investment preference
        print("\nInvestment Time Horizon:")
        print("1. Short-term (< 1 year) - Focus on recent performance")
        print("2. Medium-term (1-5 years) - Balanced approach")
        print("3. Long-term (> 5 years) - Focus on long-term trends")
        
        while True:
            try:
                choice = input("Enter your choice (1-3): ").strip()
                if choice == "1":
                    return "short"
                elif choice == "2":
                    return "medium"
                elif choice == "3":
                    return "long"
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                sys.exit(0)
    
    def get_sector_preference(self) -> str:
        # Get user sector preference
        sectors = [
            "technology", "fashion", "healthcare", "finance", "automotive",
            "food", "entertainment", "energy", "consumer_goods", "real_estate"
        ]
        
        print("\nSector Preference:")
        for i, sector in enumerate(sectors, 1):
            print(f"{i}. {sector.title()}")
        
        while True:
            try:
                choice = input(f"Enter your choice (1-{len(sectors)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(sectors):
                    return sectors[choice_num - 1]
                else:
                    print(f"Please enter a number between 1 and {len(sectors)}.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                sys.exit(0)
    
    def get_data_structure_choice(self) -> str:
        # Get user data structure preference
        print("\nData Structure Selection:")
        print("1. Use Max Heap - Efficient for retrieving top k elements")
        print("2. Use Red-Black Tree - Efficient for range queries and balanced operations")
        print("3. Compare Performance - Test both data structures and show performance metrics")
        
        while True:
            try:
                choice = input("Enter your choice (1-3): ").strip()
                if choice == "1":
                    return "max_heap"
                elif choice == "2":
                    return "red_black_tree"
                elif choice == "3":
                    return "compare"
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                sys.exit(0)
    
    def get_recommendations(self, risk_profile: str, time_investment: str, sector_preference: str, data_structure: str) -> List[Tuple[float, Stock, float]]:
        # Get stock recommendations based on user preferences
        print(f"\nAnalyzing stocks for {sector_preference.title()} sector using {data_structure.replace('_', ' ').title()}...")
        
        # Create scorer with user preferences
        scorer = StockScorer(risk_profile, time_investment, sector_preference)
        
        # Filter stocks by sector
        sector_stocks = scorer.filter_by_sector(self.stocks)
        
        if not sector_stocks:
            return []
        
        # Score all stocks
        scored_stocks = scorer.score_stocks(sector_stocks)
        
        # Use selected data structure
        if data_structure == "max_heap":
            recommendations = self.get_recommendations_using_heap(scored_stocks)
        else:  # red_black_tree
            recommendations = self.get_recommendations_using_tree(scored_stocks)
        
        if not recommendations:
            return []
        
        # Calculate certainty percentage
        certainty = scorer.calculate_certainty(recommendations)
        
        # Add certainty to each recommendation
        result = [(score, stock, certainty) for score, stock in recommendations]
        
        return result
    
    def display_recommendations(self, recommendations: List[Tuple[float, Stock, float]], data_structure: str = "unknown") -> None:
        # Display recommendations with certainty percentages
        if not recommendations:
            print("\nNo recommendations found for the selected criteria.")
            print("Try selecting a different sector or adjusting your preferences.")
            return
        
        print(f"\nTOP STOCK RECOMMENDATIONS ({data_structure.replace('_', ' ').title()})")
        
        # Display certainty percentage
        certainty = recommendations[0][2] if recommendations else 0.0
        print(f"Overall Certainty: {certainty:.1f}%")
        
        for i, (score, stock, _) in enumerate(recommendations, 1):
            print(f"\n{i}. {stock.brand_name} ({stock.ticker})")
            print(f"   Score: {score:.1f}/100")
            print(f"   Current Price: ${stock.current_price:.2f}")
            print(f"   Industry: {stock.industry_tag}")
            print(f"   Risk Metrics:")
            print(f"     - Percent Change: {stock.percent_change:.2f}%")
            print(f"     - Year Change: ${stock.year_change:.2f}")
        
        print("\nRECOMMENDATION INTERPRETATION")
        print("- Higher scores indicate better alignment with your preferences")
        print("- Certainty percentage reflects confidence in recommendations")
        print("- Percent Change shows recent price volatility")
        print("- Year Change indicates long-term performance")
        
        # Provide investment advice based on certainty
        if certainty >= 80:
            print("\n💚 HIGH CONFIDENCE: These recommendations align well with your preferences.")
        elif certainty >= 60:
            print("\n🟡 MODERATE CONFIDENCE: Consider these recommendations with additional research.")
        else:
            print("\n🔴 LOW CONFIDENCE: Consider waiting or adjusting your preferences.")
    
    def get_recommendations_using_heap(self, scored_stocks: List[Tuple[float, Stock]]) -> List[Tuple[float, Stock]]:
        # Get recommendations using Max Heap data structure
        # Clear and rebuild heap
        self.max_heap = MaxHeap()
        
        # Insert all stocks into heap
        for score, stock in scored_stocks:
            self.max_heap.insert(score, stock)
        
        # Get top 10 recommendations
        return self.max_heap.get_top_k(10)
    
    def get_recommendations_using_tree(self, scored_stocks: List[Tuple[float, Stock]]) -> List[Tuple[float, Stock]]:
        # Get recommendations using Red-Black Tree data structure
        # Clear and rebuild tree
        self.red_black_tree = RedBlackTree()
        
        # Insert all stocks into tree
        for score, stock in scored_stocks:
            self.red_black_tree.insert(score, stock)
        
        # Get top 10 recommendations using range query
        if scored_stocks:
            max_score = max(score for score, _ in scored_stocks)
            min_score = max_score - 100  # Get a wide range to ensure we get top 10
            top_stocks = self.red_black_tree.get_stocks_in_range(min_score, max_score)
            # Sort by score and take top 10
            top_stocks.sort(key=lambda x: x[0], reverse=True)
            return top_stocks[:10]
        else:
            return []
    
    def compare_performance(self, risk_profile: str, time_investment: str, sector_preference: str) -> None:
        # Compare performance between Red-Black Tree and Max Heap data structures
        print(f"\nComparing performance for {sector_preference.title()} sector...")
        
        # Run performance comparison
        results = self.performance_comparator.compare_performance(
            self.stocks, risk_profile, time_investment, sector_preference
        )
        
        # Display performance summary
        summary = self.performance_comparator.get_performance_summary(results)
        print(summary)
        
        # Display recommendations from both data structures
        if "error" not in results:
            self.display_comparison_results(results)
    
    def display_comparison_results(self, results: Dict[str, Any]) -> None:
        # Display comparison results from both data structures
        rb_results = results["red_black_tree"]
        heap_results = results["max_heap"]
        
        print("\nRECOMMENDATIONS COMPARISON")
        
        # Display Red-Black Tree recommendations
        print("\nRed-Black Tree Recommendations:")
        for i, (score, stock) in enumerate(rb_results["top_stocks"][:5], 1):
            print(f"{i}. {stock.brand_name} ({stock.ticker}) - Score: {score:.1f}")
        
        # Display Max Heap recommendations
        print("\nMax Heap Recommendations:")
        for i, (score, stock) in enumerate(heap_results["top_stocks"][:5], 1):
            print(f"{i}. {stock.brand_name} ({stock.ticker}) - Score: {score:.1f}")
        
        print("\nNote: Both data structures should produce the same top recommendations")
        print("Performance differences are in insertion and query times.")
    
    def show_data_summary(self) -> None:
        # Display a summary of the loaded data
        if not self.stocks:
            print("No data loaded.")
            return
        
        summary = self.data_loader.get_data_summary()
        sector_stats = self.sector_grouper.get_sector_statistics(self.stocks)
        
        print("\nDATA SUMMARY")
        print(f"Total Stocks: {len(self.stocks)}")
        print(f"Date Range: {summary.get('date_range', {}).get('start', 'N/A')} to {summary.get('date_range', {}).get('end', 'N/A')}")
        print("\nStocks by Sector:")
        for sector, count in sorted(sector_stats.items()):
            print(f"  {sector.title()}: {count}") 
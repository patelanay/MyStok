import pygame
import sys
from typing import List, Tuple, Dict, Any
from ..data_processing.data_loader import DataLoader
from ..data_processing.sector_grouper import SectorGrouper
from ..data_structures.red_black_tree import RedBlackTree
from ..data_structures.max_heap import MaxHeap
from ..scoring.stock_scorer import StockScorer
from ..scoring.performance_comparison import PerformanceComparator
from ..data_structures.stock import Stock


class MyStokGUI:
    # Pygame-based graphical user interface for MyStok application
    
    def __init__(self, csv_path: str = "resources/World-Stock-Prices-Dataset.csv"):
        # Initialize pygame and GUI components
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MyStok - Stock Recommendation System")
        
        # Forest green and gold theme
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.FOREST_GREEN = (34, 139, 34)  
        self.GOLD = (255, 215, 0)  
        self.DARK_GOLD = (218, 165, 32) 
        self.GREEN = (0, 200, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BACKGROUND_GRAY = (240, 240, 240) 
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 36)
        self.normal_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize data components
        self.data_loader = DataLoader(csv_path)
        self.sector_grouper = SectorGrouper()
        self.red_black_tree = RedBlackTree()
        self.max_heap = MaxHeap()
        self.performance_comparator = PerformanceComparator()
        self.stocks = []
        
        # GUI state
        self.current_screen = "welcome"
        self.risk_profile = None
        self.time_investment = None
        self.sector_preference = None
        self.data_structure_choice = None
        self.recommendations = []
        self.performance_results = None
        
        # Load data
        self.load_data()
    
    def load_data(self):
        # Load stock data
        try:
            self.stocks = self.data_loader.load_stocks()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.stocks = []
    
    def run(self):
        # Main loop for the GUI
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
            
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def handle_click(self, pos):
        if self.current_screen == "welcome":
            self.handle_welcome_click(pos)
        elif self.current_screen == "risk_profile":
            self.handle_risk_click(pos)
        elif self.current_screen == "time_investment":
            self.handle_time_click(pos)
        elif self.current_screen == "sector_preference":
            self.handle_sector_click(pos)
        elif self.current_screen == "data_structure":
            self.handle_data_structure_click(pos)
        elif self.current_screen == "results":
            self.handle_results_click(pos)
    
    def handle_key(self, key):
        if key == pygame.K_ESCAPE:
            if self.current_screen != "welcome":
                self.current_screen = "welcome"
    
    def handle_welcome_click(self, pos):
        if 300 <= pos[0] <= 700 and 450 <= pos[1] <= 510:
            # Start button clicked
            self.current_screen = "risk_profile"
        elif 300 <= pos[0] <= 700 and 530 <= pos[1] <= 570:
            # CLI button
            self.switch_to_cli()
    
    def handle_risk_click(self, pos):
        if 300 <= pos[0] <= 700:
            if 150 <= pos[1] <= 210:
                self.risk_profile = "low"
                self.current_screen = "time_investment"
            elif 230 <= pos[1] <= 290:
                self.risk_profile = "medium"
                self.current_screen = "time_investment"
            elif 310 <= pos[1] <= 370:
                self.risk_profile = "high"
                self.current_screen = "time_investment"
    
    def handle_time_click(self, pos):
        if 300 <= pos[0] <= 700:
            if 150 <= pos[1] <= 210:
                self.time_investment = "short"
                self.current_screen = "sector_preference"
            elif 230 <= pos[1] <= 290:
                self.time_investment = "medium"
                self.current_screen = "sector_preference"
            elif 310 <= pos[1] <= 370:
                self.time_investment = "long"
                self.current_screen = "sector_preference"
    
    def handle_sector_click(self, pos):
        sectors = ["technology", "fashion", "healthcare", "finance", "automotive", "food", "entertainment", "energy", "consumer_goods", "real_estate"]
        
        if 300 <= pos[0] <= 700:
            for i, sector in enumerate(sectors):
                y = 120 + i * 45
                if y <= pos[1] <= y + 45:
                    self.sector_preference = sector
                    self.current_screen = "data_structure"
                    break
    
    def handle_data_structure_click(self, pos):
        if 300 <= pos[0] <= 700:
            if 150 <= pos[1] <= 210:
                self.data_structure_choice = "max_heap"
                self.get_recommendations()
            elif 230 <= pos[1] <= 290:
                self.data_structure_choice = "red_black_tree"
                self.get_recommendations()
            elif 310 <= pos[1] <= 370:
                self.data_structure_choice = "compare"
                self.compare_performance()
    
    def handle_results_click(self, pos):
        if 300 <= pos[0] <= 700 and 600 <= pos[1] <= 660:
            self.current_screen = "welcome"
            self.reset_state()
    
    def get_recommendations(self):
        # Get stock recommendations for user
        scorer = StockScorer(self.risk_profile, self.time_investment, self.sector_preference)
        sector_stocks = scorer.filter_by_sector(self.stocks)
        
        if not sector_stocks:
            self.recommendations = []
            self.current_screen = "results"
            return
        
        scored_stocks = scorer.score_stocks(sector_stocks)
        
        if self.data_structure_choice == "max_heap":
            recommendations = self.get_recommendations_using_heap(scored_stocks)
        else:
            recommendations = self.get_recommendations_using_tree(scored_stocks)
        
        if recommendations:
            certainty = scorer.calculate_certainty(recommendations)
            self.recommendations = [(score, stock, certainty) for score, stock in recommendations]
        
        self.current_screen = "results"
    
    def compare_performance(self):
        # Compare performance between max heap and red black tree
        results = self.performance_comparator.compare_performance(
            self.stocks, self.risk_profile, self.time_investment, self.sector_preference
        )
        self.performance_results = results
        self.current_screen = "results"
    
    def get_recommendations_using_heap(self, scored_stocks):
        self.max_heap = MaxHeap()
        for score, stock in scored_stocks:
            self.max_heap.insert(score, stock)
        return self.max_heap.get_top_k(10)
    
    def get_recommendations_using_tree(self, scored_stocks):
        self.red_black_tree = RedBlackTree()
        for score, stock in scored_stocks:
            self.red_black_tree.insert(score, stock)
        
        if scored_stocks:
            max_score = max(score for score, _ in scored_stocks)
            min_score = max_score - 100
            top_stocks = self.red_black_tree.get_stocks_in_range(min_score, max_score)
            top_stocks.sort(key=lambda x: x[0], reverse=True)
            return top_stocks[:10]
        return []
    
    def reset_state(self):
        self.risk_profile = None
        self.time_investment = None
        self.sector_preference = None
        self.data_structure_choice = None
        self.recommendations = []
        self.performance_results = None
    
    def switch_to_cli(self):
        # Switch from pygame to command line interface
        print("\nSwitching to Command Line Interface...")
        pygame.quit()
        
        # Use CLI
        from src.interface.cli import MyStokCLI
        cli = MyStokCLI("resources/World-Stock-Prices-Dataset.csv")
        cli.run()
        
        # Exit the program 
        sys.exit(0)
    
    def draw(self):
        # Draw the screen
        self.screen.fill(self.BACKGROUND_GRAY)
        
        if self.current_screen == "welcome":
            self.draw_welcome_screen()
        elif self.current_screen == "risk_profile":
            self.draw_risk_screen()
        elif self.current_screen == "time_investment":
            self.draw_time_screen()
        elif self.current_screen == "sector_preference":
            self.draw_sector_screen()
        elif self.current_screen == "data_structure":
            self.draw_data_structure_screen()
        elif self.current_screen == "results":
            self.draw_results_screen()
    
    def draw_welcome_screen(self):
        # Draw welcome screen
        title = self.title_font.render("MyStok", True, self.FOREST_GREEN)
        subtitle = self.header_font.render("Stock Recommendation System", True, self.FOREST_GREEN)
        team = self.normal_font.render("Team: Project 3 Group 55", True, self.FOREST_GREEN)
        members = self.normal_font.render("Members: James Jean Philipe, Ignatius Martin, Anay Patel", True, self.FOREST_GREEN)
        start_button = self.header_font.render("Click to Start", True, self.WHITE)
        cli_button = self.normal_font.render("Switch to Command Line", True, self.WHITE)
        
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 150))
        self.screen.blit(subtitle, (self.screen_width//2 - subtitle.get_width()//2, 220))
        self.screen.blit(team, (self.screen_width//2 - team.get_width()//2, 290))
        self.screen.blit(members, (self.screen_width//2 - members.get_width()//2, 320))
        
        # Draw start button
        pygame.draw.rect(self.screen, self.FOREST_GREEN, (300, 450, 400, 60))
        pygame.draw.rect(self.screen, self.DARK_GOLD, (300, 450, 400, 60), 3)  
        self.screen.blit(start_button, (self.screen_width//2 - start_button.get_width()//2, 465))
        
        # Draw CLI button 
        pygame.draw.rect(self.screen, self.WHITE, (300, 530, 400, 40)) 
        pygame.draw.rect(self.screen, self.GOLD, (300, 530, 400, 40), 2) 
        cli_button_text = self.normal_font.render("Switch to Command Line", True, self.BLACK)  
        self.screen.blit(cli_button_text, (self.screen_width//2 - cli_button_text.get_width()//2, 540))
    
    def draw_risk_screen(self):
        # Draw risk profile screen
        title = self.header_font.render("Select Risk Profile", True, self.FOREST_GREEN)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 80))
        
        options = [
            ("Low (Conservative)", "Prefer stable, low-volatility stocks"),
            ("Medium (Balanced)", "Moderate risk tolerance"),
            ("High (Aggressive)", "Comfortable with high volatility")
        ]
        
        for i, (option, desc) in enumerate(options):
            y = 150 + i * 80
            pygame.draw.rect(self.screen, self.WHITE, (300, y, 400, 60))
            pygame.draw.rect(self.screen, self.GOLD, (300, y, 400, 60), 2)
            option_text = self.normal_font.render(option, True, self.BLACK)
            desc_text = self.small_font.render(desc, True, self.GRAY)
            
            self.screen.blit(option_text, (320, y + 15))
            self.screen.blit(desc_text, (320, y + 35))
    
    def draw_time_screen(self):
        # Draw time investment screen
        title = self.header_font.render("Select Investment Time Horizon", True, self.FOREST_GREEN)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 80))
        
        options = [
            ("Short-term (< 1 year)", "Focus on recent performance"),
            ("Medium-term (1-5 years)", "Balanced approach"),
            ("Long-term (> 5 years)", "Focus on long-term trends")
        ]
        
        for i, (option, desc) in enumerate(options):
            y = 150 + i * 80
            pygame.draw.rect(self.screen, self.WHITE, (300, y, 400, 60))  
            pygame.draw.rect(self.screen, self.GOLD, (300, y, 400, 60), 2) 
            option_text = self.normal_font.render(option, True, self.BLACK)
            desc_text = self.small_font.render(desc, True, self.GRAY)
            
            self.screen.blit(option_text, (320, y + 15))
            self.screen.blit(desc_text, (320, y + 35))
    
    def draw_sector_screen(self):
        # Draw sector preference screen
        title = self.header_font.render("Select Sector Preference", True, self.FOREST_GREEN)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 80))
        
        sectors = ["Technology", "Fashion", "Healthcare", "Finance", "Automotive",
                  "Food", "Entertainment", "Energy", "Consumer Goods", "Real Estate"]
        
        for i, sector in enumerate(sectors):
            y = 120 + i * 45
            pygame.draw.rect(self.screen, self.WHITE, (300, y, 400, 45))  
            pygame.draw.rect(self.screen, self.GOLD, (300, y, 400, 45), 2)  
            sector_text = self.normal_font.render(sector, True, self.BLACK)
            self.screen.blit(sector_text, (320, y + 12))
    
    def draw_data_structure_screen(self):
        # Draw data structure screen
        title = self.header_font.render("Select Data Structure", True, self.FOREST_GREEN)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 80))
        
        options = [
            ("Max Heap"),
            ("Red-Black Tree"),
            ("Compare Performance")
        ]
        
        for i, option in enumerate(options):
            y = 150 + i * 80
            pygame.draw.rect(self.screen, self.WHITE, (300, y, 400, 60)) 
            pygame.draw.rect(self.screen, self.GOLD, (300, y, 400, 60), 2) 
            option_text = self.normal_font.render(option, True, self.BLACK)
            
            self.screen.blit(option_text, (320, y + 20))
    
    def draw_results_screen(self):
        title = self.header_font.render("Results", True, self.FOREST_GREEN)
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 40))
        
        if self.data_structure_choice == "compare":
            self.draw_performance_results()
        else:
            self.draw_recommendation_results()
        
        # Draw back button
        pygame.draw.rect(self.screen, self.FOREST_GREEN, (300, 600, 400, 60))
        pygame.draw.rect(self.screen, self.DARK_GOLD, (300, 600, 400, 60), 3) 
        back_text = self.header_font.render("Back to Start", True, self.WHITE)
        self.screen.blit(back_text, (self.screen_width//2 - back_text.get_width()//2, 615))
    
    def draw_performance_results(self):
        # Draw performance comparison results
        if not self.performance_results or "error" in self.performance_results:
            error_text = self.normal_font.render("No performance data available", True, self.RED)
            self.screen.blit(error_text, (self.screen_width//2 - error_text.get_width()//2, 150))
            return
        
        rb_time = self.performance_results["red_black_tree"]["total_time"]
        heap_time = self.performance_results["max_heap"]["total_time"]
        
        if rb_time < heap_time:
            winner = "Red-Black Tree"
            diff = heap_time - rb_time
        else:
            winner = "Max Heap"
            diff = rb_time - heap_time
        
        results = [
            f"Red-Black Tree: {rb_time:.6f}s",
            f"Max Heap: {heap_time:.6f}s",
            f"Winner: {winner} ({diff:.6f}s faster)"
        ]
        
        for i, result in enumerate(results):
            y = 120 + i * 50
            result_text = self.normal_font.render(result, True, self.BLACK)
            self.screen.blit(result_text, (self.screen_width//2 - result_text.get_width()//2, y))
    
    def draw_recommendation_results(self):
        if not self.recommendations:
            no_results = self.normal_font.render("No recommendations found", True, self.RED)
            self.screen.blit(no_results, (self.screen_width//2 - no_results.get_width()//2, 150))
            return
        
        # Display top 5 recommendations 
        for i, (score, stock, certainty) in enumerate(self.recommendations[:5]):
            y = 120 + i * 80
            stock_text = self.normal_font.render(f"{i+1}. {stock.brand_name} ({stock.ticker})", True, self.BLACK)
            score_text = self.small_font.render(f"Score: {score:.1f}/100", True, self.FOREST_GREEN)
            price_text = self.small_font.render(f"Price: ${stock.current_price:.2f}", True, self.GRAY)
            
            self.screen.blit(stock_text, (self.screen_width//2 - stock_text.get_width()//2, y))
            self.screen.blit(score_text, (self.screen_width//2 - score_text.get_width()//2, y + 25))
            self.screen.blit(price_text, (self.screen_width//2 - price_text.get_width()//2, y + 45))
        
        # Display certainty
        if self.recommendations:
            certainty = self.recommendations[0][2]
            certainty_text = self.normal_font.render(f"Certainty: {certainty:.1f}%", True, self.GREEN)
            self.screen.blit(certainty_text, (self.screen_width//2 - certainty_text.get_width()//2, 520)) 
from typing import List, Tuple
from ..data_structures.stock import Stock
from ..data_processing.sector_grouper import SectorGrouper


class StockScorer:
#Calculates stock relevance scores based on user preferences.   
#Uses 50% risk and 50% time weights for scoring.

    def __init__(self, risk_profile: str, time_investment: str, sector_preference: str):
        self.risk_profile = risk_profile.lower()
        self.time_investment = time_investment.lower()
        self.sector_preference = sector_preference.lower()
        self.sector_grouper = SectorGrouper()
    
    def calculate_score(self, stock: Stock) -> float:
        score = 0.0
        
        # Risk scoring (50% weight)
        risk_score = self.calculate_risk_score(stock)
        score += risk_score * 0.50
        
        # Time investment scoring (50% weight)
        time_score = self.calculate_time_score(stock)
        score += time_score * 0.50
        
        return min(100.0, max(0.0, score))
    
    def calculate_risk_score(self, stock: Stock) -> float:
        percent_change = abs(stock.percent_change)
        
        if self.risk_profile == "low":

            return max(0, 100 - percent_change * 2)
        elif self.risk_profile == "medium":

            return max(0, 100 - abs(percent_change - 5) * 5)
        else:  
            #high risk
            return min(100, percent_change * 2)
    
    def calculate_time_score(self, stock: Stock) -> float:
        #Score based on price difference over a year.
        change = stock.year_change
        
        if self.time_investment == "short":
            # looks at recent performance
            return max(0, min(100, 50 + change * 2))
        elif self.time_investment == "medium":
            # Balanced
            return max(0, min(100, 50 + change * 1))
        else:  # long term
            return max(0, min(100, 50 + change * 0.5))
    
    def filter_by_sector(self, stocks: List[Stock]) -> List[Stock]:
        sector_keywords = self.get_sector_keywords(self.sector_preference)
        filtered_stocks = []
        
        for stock in stocks:
            if stock.industry_tag.lower() in sector_keywords:
                filtered_stocks.append(stock)
        
        return filtered_stocks
    
    def get_sector_keywords(self, sector: str) -> List[str]:
        sector_mapping = {
            "technology": ["technology", "e-commerce", "social media"],
            "fashion": ["fitness", "footwear", "apparel", "retail"],
            "healthcare": ["healthcare"],
            "finance": ["finance", "cryptocurrency"],
            "automotive": ["automotive", "aviation"],
            "food": ["food", "food & beverage"],
            "entertainment": ["entertainment", "gaming", "music"],
            "energy": ["energy"],
            "consumer_goods": ["consumer goods"],
            "real_estate": ["hospitality"]
        }
        return sector_mapping.get(sector.lower(), [])
    
    def score_stocks(self, stocks: List[Stock]) -> List[Tuple[float, Stock]]:
        scored_stocks = []
        
        for stock in stocks:
            score = self.calculate_score(stock)
            scored_stocks.append((score, stock))
        
        # Sort by score in descending order
        scored_stocks.sort(key=lambda x: x[0], reverse=True)
        
        return scored_stocks
    
    def get_top_recommendations(self, stocks: List[Stock], top_k: int = 10) -> List[Tuple[float, Stock]]:
        #Get top stock recommendations
        sector_stocks = self.filter_by_sector(stocks)
        
        if not sector_stocks:
            return []
        
        # Score the filtered stocks
        scored_stocks = self.score_stocks(sector_stocks)
        
        return scored_stocks[:top_k]
    
    def calculate_certainty(self, scored_stocks: List[Tuple[float, Stock]]) -> float:
    
        #Calculate certainty percentage for recommendations.
        if not scored_stocks:
            return 0.0
        
        # Calculate average score
        scores = [score for score, _ in scored_stocks]
        avg_score = sum(scores) / len(scores)
        
        # Calculate score variance (lower variance = higher certainty)
        variance = sum((score - avg_score) ** 2 for score in scores) / len(scores)
        
        # Convert to certainty percentage
        # Higher average score and lower variance = higher certainty
        certainty = min(100.0, avg_score * (1 - variance / 10000))
        
        return max(0.0, certainty) 
# Sector grouping logic for MyStok application

from typing import Dict, List, Set


class SectorGrouper:
    
    def __init__(self):
        # Initialize the sector groupe
        self.sector_mappings = {
            "technology": ["technology", "e-commerce", "social media"],
            "fashion": ["footwear", "apparel", "fitness"],
            "healthcare": ["healthcare", "fitness"],
            "finance": ["finance", "cryptocurrency"],
            "automotive": ["automotive", "aviation"],
            "food": ["food", "food & beverage"],
            "entertainment": ["entertainment", "gaming", "music"],
            "energy": ["energy"],
            "consumer_goods": ["consumer goods", "retail"],
            "real_estate": ["hospitality"]
        }
    
    def categorize_stock(self, industry_tag: str) -> str:
        # Categorize stock based on industry tag
        if not industry_tag:
            return "other"
        
        industry_lower = industry_tag.lower()
        
        # Check each sector's keywords
        for sector, keywords in self.sector_mappings.items():
            if any(keyword in industry_lower for keyword in keywords):
                return sector
        
        return "other"
    
    def get_available_sectors(self) -> List[str]:
        # Get list
        return list(self.sector_mappings.keys()) + ["other"]
    
    def get_sector_keywords(self, sector: str) -> List[str]:
        return self.sector_mappings.get(sector.lower(), [])
    
    def add_custom_sector(self, sector_name: str, keywords: List[str]) -> None:
        # Add a custom sector with keywords
        self.sector_mappings[sector_name.lower()] = keywords
    
    def get_sector_statistics(self, stocks: List) -> Dict[str, int]:
        # Get statistics of stocks
        sector_counts = {}
        
        for stock in stocks:
            sector = self.categorize_stock(stock.industry_tag)
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        return sector_counts
    
    def filter_stocks_by_sector(self, stocks: List, sector: str) -> List:
        # Filter stocks
        filtered_stocks = []
        
        for stock in stocks:
            if self.categorize_stock(stock.industry_tag) == sector.lower():
                filtered_stocks.append(stock)
        
        return filtered_stocks 
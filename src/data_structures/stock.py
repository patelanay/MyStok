# Stock data model for MyStok application

from typing import List, Optional


class Stock:
    # Represents a stock with its information
    
    def __init__(self, ticker: str, brand_name: str, industry_tag: str, current_price: float, historical_data: List[float]):
        # Initialize a Stock object
        self.ticker = ticker
        self.brand_name = brand_name
        self.industry_tag = industry_tag
        self.current_price = current_price
        self.historical_data = historical_data
        
        # Calculate metrics
        self.percent_change = self.calculate_percent_change()
        self.year_change = self.calculate_year_change()
    
    def calculate_percent_change(self) -> float:
        # Calculate percent change for risk assessment
        if len(self.historical_data) < 2:
            return 0.0
        
        previous_price = self.historical_data[-2]
        if previous_price == 0:
            return 0.0
        
        return ((self.current_price - previous_price) / previous_price) * 100
    
    def calculate_year_change(self) -> float:
        # Calculate difference from 1 year ago
        if len(self.historical_data) < 365:
            return 0.0
        
        price_1_year_ago = self.historical_data[-365]
        return self.current_price - price_1_year_ago
    
    def __str__(self) -> str:
        return f"{self.brand_name} ({self.ticker}) - ${self.current_price:.2f}"
    
    def __repr__(self) -> str:
        return (f"Stock(ticker='{self.ticker}', brand_name='{self.brand_name}', "
                f"industry_tag='{self.industry_tag}', current_price={self.current_price})") 
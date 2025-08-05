# Data loader for MyStok application

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from ..data_structures.stock import Stock


class DataLoader:
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = None
    
    def load_stocks(self) -> List[Stock]:
        # Load stock data from CSV
        try:
            self.data = pd.read_csv(self.csv_path)
            
            # Clean data
            self.clean_data()
            
            # Group data by stock
            stocks = []
            grouped_data = self.data.groupby(['Ticker', 'Brand_Name', 'Industry_Tag'])
            
            for group_key, group in grouped_data:
                ticker, brand_name, industry_tag = group_key
                # Sort by date
                group_sorted = group.sort_values('Date')
                
                # Get price data 
                prices = group_sorted['Close'].tolist()
                
                if len(prices) >= 2:  
                    current_price = prices[-1]  
                    historical_data = prices
                    
                    # Create Stock object
                    stock = Stock(
                        ticker=ticker,
                        brand_name=brand_name,
                        industry_tag=industry_tag,
                        current_price=current_price,
                        historical_data=historical_data
                    )
                    stocks.append(stock)
            
            return stocks
            
        except FileNotFoundError:
            print(f"Error: CSV file not found at {self.csv_path}")
            return []
        except Exception as x:
            print(f"Error loading data: {x}")
            return []
    
    def clean_data(self) -> None:
        # Clean the loaded data
        if self.data is None:
            return
        
        # Get rid of rows with missing data
        essential_columns = ['Date', 'Ticker', 'Brand_Name', 'Industry_Tag', 'Close']
        self.data = self.data.dropna(subset=essential_columns)
        
        # Convert date column to datetime
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        
        # Get rid of rows with invalid prices
        self.data = self.data[self.data['Close'] > 0]
        
        # Get rid of duplicate entries
        self.data = self.data.drop_duplicates(subset=['Date', 'Ticker'])
        
        # Sort by date and ticker
        self.data = self.data.sort_values(['Ticker', 'Date'])
    
    def get_data_summary(self) -> Dict[str, Any]:
        # Get a summary of the data
        if self.data is None:
            return {}
        
        return {
            'total_rows': len(self.data),
            'unique_stocks': self.data['Ticker'].nunique(),
            'date_range': {
                'start': self.data['Date'].min(),
                'end': self.data['Date'].max()
            },
            'sectors': self.data['Industry_Tag'].value_counts().to_dict(),
            'price_stats': {
                'min': self.data['Close'].min(),
                'max': self.data['Close'].max(),
                'mean': self.data['Close'].mean(),
                'median': self.data['Close'].median()
            }
        }
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Stock]:
        try:
            # Read CSV file
            data = pd.read_csv(self.csv_path)
            data['Date'] = pd.to_datetime(data['Date'])
            
            # Filter by date range
            mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
            filtered_data = data[mask]

            stocks = []
            grouped_data = filtered_data.groupby(['Ticker', 'Brand_Name', 'Industry_Tag'])
            
            for group_key, group in grouped_data:
                ticker, brand_name, industry_tag = group_key
                group_sorted = group.sort_values('Date')
                prices = group_sorted['Close'].tolist()
                
                if len(prices) >= 2:
                    current_price = prices[-1]
                    historical_data = prices
                    
                    stock = Stock(
                        ticker=ticker,
                        brand_name=brand_name,
                        industry_tag=industry_tag,
                        current_price=current_price,
                        historical_data=historical_data
                    )
                    stocks.append(stock)
            
            return stocks
            
        except Exception as x:
            print(f"Error filtering data: {x}")
            return [] 
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os

def setup_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

logger = setup_logger()

class RetailDataProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = None
        
    def load_data(self):
        """Load the online retail dataset"""
        try:
            self.data = pd.read_excel(self.input_file)
            logger.info(f"Loaded {len(self.data)} records")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
            
    def clean_data(self):
        """Clean and preprocess the data"""
        try:
            # Remove rows with missing values
            self.data = self.data.dropna()
            
            # Remove cancelled orders (negative quantities)
            self.data = self.data[self.data['Quantity'] > 0]
            
            # Remove rows with zero or negative unit price
            self.data = self.data[self.data['UnitPrice'] > 0]
            
            # Calculate total amount for each transaction
            self.data['TotalAmount'] = self.data['Quantity'] * self.data['UnitPrice']
            
            logger.info(f"Data cleaned. Remaining records: {len(self.data)}")
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise
            
    def create_daily_aggregates(self):
        """Create daily revenue aggregates"""
        try:
            # Group by date
            daily_data = self.data.groupby('InvoiceDate').agg({
                'TotalAmount': 'sum',
                'Quantity': 'sum',
                'InvoiceNo': 'nunique',
                'CustomerID': 'nunique'
            }).reset_index()
            
            # Rename columns
            daily_data.columns = ['date', 'revenue', 'total_items', 
                                'total_transactions', 'unique_customers']
            
            # Sort by date
            daily_data = daily_data.sort_values('date')
            
            # Create time-based features
            daily_data['year'] = daily_data['date'].dt.year
            daily_data['month'] = daily_data['date'].dt.month
            daily_data['day_of_week'] = daily_data['date'].dt.dayofweek
            daily_data['day_of_month'] = daily_data['date'].dt.day
            
            return daily_data
            
        except Exception as e:
            logger.error(f"Error creating daily aggregates: {str(e)}")
            raise
            
    def create_features(self, df):
        """Create additional features for modeling"""
        try:
            # Create lag features
            for lag in [1, 7, 30]:
                df[f'revenue_lag_{lag}'] = df['revenue'].shift(lag)
                df[f'transactions_lag_{lag}'] = df['total_transactions'].shift(lag)
                
            # Create rolling means
            for window in [7, 30]:
                df[f'revenue_rolling_mean_{window}'] = df['revenue'].rolling(window=window).mean()
                df[f'transactions_rolling_mean_{window}'] = df['total_transactions'].rolling(window=window).mean()
                
            # Create weekend flag
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
            
            # Drop rows with NaN values created by lag features
            df = df.dropna()
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating features: {str(e)}")
            raise
            
    def process_data(self):
        """Run the complete data processing pipeline"""
        try:
            self.load_data()
            self.clean_data()
            daily_data = self.create_daily_aggregates()
            processed_data = self.create_features(daily_data)
            
            logger.info("Data processing completed successfully")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error in processing pipeline: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    input_file = "../data/online_retail.xlsx"  # Update with your file path
    processor = RetailDataProcessor(input_file)
    processed_data = processor.process_data()
    
    # Save processed data
    output_file = "../app/data/processed_retail_data.csv"
    processed_data.to_csv(output_file, index=False)
    logger.info(f"Processed data saved to {output_file}")

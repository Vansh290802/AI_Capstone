import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils.logger import setup_logger

logger = setup_logger('data_ingestion')

class DataIngestionPipeline:
    def __init__(self, data_path: str = '../app/data'):
        self.data_path = data_path
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            
    def fetch_data(self):
        """
        Fetch data from the UCI repository
        Returns: DataFrame with the loaded data
        """
        try:
            # For this example, we'll simulate data fetching
            # In production, you would fetch from actual source
            data = {
                'date': pd.date_range(start='2020-01-01', periods=365, freq='D'),
                'revenue': np.random.normal(1000, 100, 365),
                'country': np.random.choice(['US', 'UK', 'DE', 'FR'], 365)
            }
            df = pd.DataFrame(data)
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise
            
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process and clean the data
        Args:
            df: Raw DataFrame
        Returns:
            Processed DataFrame
        """
        try:
            # Basic processing
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Add features
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day_of_week'] = df['date'].dt.dayofweek
            
            logger.info("Data processing completed successfully")
            return df
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise
            
    def save_data(self, df: pd.DataFrame, filename: str):
        """
        Save processed data
        Args:
            df: Processed DataFrame
            filename: Name of the file to save
        """
        try:
            output_path = os.path.join(self.data_path, filename)
            df.to_csv(output_path, index=False)
            logger.info(f"Data saved successfully to {output_path}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise
            
    def run_pipeline(self):
        """
        Run the complete data ingestion pipeline
        """
        try:
            # Fetch data
            raw_data = self.fetch_data()
            
            # Process data
            processed_data = self.process_data(raw_data)
            
            # Save data
            self.save_data(processed_data, 'processed_data.csv')
            
            logger.info("Data ingestion pipeline completed successfully")
            return processed_data
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.run_pipeline()
from datetime import datetime
import json
import os
from typing import Dict, List
import numpy as np

class PerformanceMonitor:
    def __init__(self):
        self.metrics_file = '../data/metrics.json'
        self.predictions_log = []
        self.initialize_metrics()
        
    def initialize_metrics(self):
        """Initialize or load existing metrics"""
        if os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {
                'predictions_count': 0,
                'average_response_time': 0,
                'error_rate': 0,
                'last_update': datetime.now().isoformat()
            }
            self._save_metrics()
            
    def _save_metrics(self):
        """Save metrics to file"""
        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f)
            
    def log_prediction(self, country: str, prediction: Dict):
        """Log individual prediction"""
        self.predictions_log.append({
            'timestamp': datetime.now().isoformat(),
            'country': country,
            'prediction': prediction
        })
        self.metrics['predictions_count'] += 1
        self._save_metrics()
        
    def get_metrics(self) -> Dict:
        """Get current performance metrics"""
        self.metrics['last_update'] = datetime.now().isoformat()
        return self.metrics
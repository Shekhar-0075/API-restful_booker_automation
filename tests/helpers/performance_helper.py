import time
import statistics
import logging
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

class PerformanceHelper:
    """Simple performance monitoring for API tests"""
    
    def __init__(self):
        self.metrics = []
        self.thresholds = {
            'create_booking': 5000,    # 5 seconds
            'get_booking': 3000,       # 3 seconds  
            'update_booking': 5000,    # 5 seconds
            'delete_booking': 3000,    # 3 seconds
            'search_bookings': 10000   # 10 seconds
        }
    
    def measure_api_call(self, func, operation_name: str, *args, **kwargs):
        """Measure API call performance"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Store metric
        self.metrics.append({
            'operation': operation_name,
            'response_time': response_time,
            'timestamp': start_time
        })
        
        # Check threshold
        threshold = self.thresholds.get(operation_name, 5000)
        if response_time > threshold:
            logger.warning(f"{operation_name} took {response_time:.2f}ms (threshold: {threshold}ms)")
        else:
            logger.info(f"{operation_name} completed in {response_time:.2f}ms")
        
        return result, response_time
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.metrics:
            return {'message': 'No performance data collected'}
        
        response_times = [m['response_time'] for m in self.metrics]
        
        return {
            'total_calls': len(self.metrics),
            'avg_response_time': f"{statistics.mean(response_times):.2f}ms",
            'min_response_time': f"{min(response_times):.2f}ms", 
            'max_response_time': f"{max(response_times):.2f}ms",
            'slowest_operation': max(self.metrics, key=lambda x: x['response_time'])
        }

"""
Example of how another team (marketing team) uses Robert's team extensions.
This simulates a real scenario where your sth/robert_common code is being reused.
"""

# Another team importing your team's extensions
from sth.robert_common.extended_utils import EnhancedLogger, TeamConfigManager, standardized_error_handler
from sth.robert_common.advanced_processing import AdvancedDataProcessor, batch_process_data

class MarketingDataPipeline:
    """Marketing team using Robert team's extensions."""
    
    def __init__(self):
        # Using your enhanced logger
        self.logger = EnhancedLogger("marketing_pipeline", team="marketing_team")
        
        # Using your config manager
        self.config = TeamConfigManager("marketing_team")
        
        # Using your advanced processor
        self.processor = AdvancedDataProcessor("marketing_team")
    
    @standardized_error_handler  # Using your error handling decorator
    def process_customer_data(self, customer_records):
        """Process customer data using Robert team's advanced processing."""
        self.logger.info_with_context(
            "Starting customer data processing",
            record_count=len(customer_records),
            team="marketing_team"
        )
        
        # Define schema for marketing data
        marketing_schema = {
            'required_fields': ['customer_id', 'email', 'signup_date'],
            'field_types': {
                'customer_id': str,
                'email': str,
                'signup_date': str
            }
        }
        
        # Use Robert team's batch processing
        result = batch_process_data(customer_records, "marketing_team")
        
        self.logger.info_with_context(
            "Customer data processing completed",
            successful=result['summary']['successful'],
            failed=result['summary']['failed'],
            avg_quality=result['summary']['average_quality_score']
        )
        
        return result

def main():
    """Example of marketing team using Robert team's code."""
    pipeline = MarketingDataPipeline()
    
    # Sample customer data
    customer_data = [
        {
            'customer_id': 'CUST001',
            'email': 'john@example.com',
            'signup_date': '2025-01-15',
            'source': 'website'
        },
        {
            'customer_id': 'CUST002',
            'email': 'jane@example.com',
            'signup_date': '2025-01-16',
            'source': 'mobile_app'
        }
    ]
    
    # Process using Robert team's extensions
    results = pipeline.process_customer_data(customer_data)
    print(f"Marketing team processed {len(customer_data)} records using Robert team's tools")
    print(f"Success rate: {results['summary']['successful']}/{results['summary']['total_processed']}")

if __name__ == "__main__":
    main()

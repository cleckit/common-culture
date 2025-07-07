"""
Example application that uses the common modules.
"""

from sth.robert_common.utils import shared_logger, CommonBase
from sth.robert_common.data_processor import process_data, validate_input

def main():
    """Main application function."""
    logger = shared_logger(__name__)
    logger.info("Starting application")
    
    # Use common base class
    base = CommonBase()
    print(f"Base status: {base.get_status()}")
    
    # Process some data
    sample_data = {"key": "value", "number": 42}
    validate_input(sample_data)
    result = process_data(sample_data)
    
    logger.info(f"Processed data: {result}")

if __name__ == "__main__":
    main()

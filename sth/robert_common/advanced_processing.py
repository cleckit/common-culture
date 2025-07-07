"""
Advanced data processing extensions.
These functions extend the basic data processing from src/common with team-specific needs.
Other teams found these so useful they started importing them too.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import hashlib

# This would normally import from src/common
# from src.common.data_processing import BaseProcessor, DataValidator
# For demo purposes, we'll simulate these

class AdvancedDataProcessor:
    """
    Enhanced data processor that other teams started using.
    Extends basic processing with validation, caching, and audit trails.
    """
    
    def __init__(self, team_name: str):
        self.team_name = team_name
        self.processing_history = []
    
    def process_with_validation(self, data: Dict[str, Any], schema: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process data with validation and audit trail.
        This became popular because it prevents data corruption issues.
        """
        processing_id = self._generate_processing_id(data)
        
        # Validate input
        validation_result = self._validate_data(data, schema)
        if not validation_result['valid']:
            raise ValueError(f"Data validation failed: {validation_result['errors']}")
        
        # Process the data (extending basic processing)
        processed_data = {
            'processing_id': processing_id,
            'processed_at': datetime.now().isoformat(),
            'processed_by_team': self.team_name,
            'original_data': data,
            'processed_data': self._enhance_data(data),
            'validation_passed': True,
            'data_quality_score': self._calculate_quality_score(data)
        }
        
        # Add to audit trail
        self.processing_history.append({
            'processing_id': processing_id,
            'timestamp': datetime.now().isoformat(),
            'team': self.team_name,
            'data_size': len(str(data)),
            'quality_score': processed_data['data_quality_score']
        })
        
        return processed_data
    
    def _generate_processing_id(self, data: Dict[str, Any]) -> str:
        """Generate unique ID for processing session."""
        data_str = json.dumps(data, sort_keys=True)
        timestamp = datetime.now().isoformat()
        combined = f"{data_str}{timestamp}{self.team_name}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    def _validate_data(self, data: Dict[str, Any], schema: Optional[Dict] = None) -> Dict[str, Any]:
        """Enhanced validation that other teams adopted."""
        errors = []
        
        # Basic validation
        if not isinstance(data, dict):
            errors.append("Data must be a dictionary")
        
        if not data:
            errors.append("Data cannot be empty")
        
        # Check for required fields if schema provided
        if schema and 'required_fields' in schema:
            for field in schema['required_fields']:
                if field not in data:
                    errors.append(f"Missing required field: {field}")
        
        # Check data types if schema provided
        if schema and 'field_types' in schema:
            for field, expected_type in schema['field_types'].items():
                if field in data and not isinstance(data[field], expected_type):
                    errors.append(f"Field {field} must be of type {expected_type.__name__}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'validated_at': datetime.now().isoformat()
        }
    
    def _enhance_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add enhancements that other teams found valuable."""
        enhanced = data.copy()
        
        # Add metadata
        enhanced['_metadata'] = {
            'processed_by_team': self.team_name,
            'processing_version': '2.0',
            'enhancements_applied': [
                'data_normalization',
                'quality_scoring',
                'audit_trail'
            ]
        }
        
        # Normalize string fields
        for key, value in enhanced.items():
            if isinstance(value, str):
                enhanced[key] = value.strip().lower()
        
        return enhanced
    
    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score (other teams use this for reporting)."""
        score = 1.0
        
        # Penalize for missing values
        total_fields = len(data)
        null_fields = sum(1 for v in data.values() if v is None or v == "")
        if total_fields > 0:
            score -= (null_fields / total_fields) * 0.3
        
        # Reward for data richness
        if total_fields > 5:
            score += 0.1
        
        # Check for standard fields that indicate good data quality
        quality_indicators = ['id', 'timestamp', 'source', 'version']
        present_indicators = sum(1 for indicator in quality_indicators if indicator in data)
        score += (present_indicators / len(quality_indicators)) * 0.2
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1


def batch_process_data(data_list: List[Dict[str, Any]], team_name: str) -> Dict[str, Any]:
    """
    Batch processing function that became popular across teams.
    Processes multiple data items efficiently with summary statistics.
    """
    processor = AdvancedDataProcessor(team_name)
    results = []
    summary = {
        'total_processed': 0,
        'successful': 0,
        'failed': 0,
        'average_quality_score': 0.0,
        'processing_errors': []
    }
    
    for i, data_item in enumerate(data_list):
        try:
            result = processor.process_with_validation(data_item)
            results.append(result)
            summary['successful'] += 1
            summary['average_quality_score'] += result['data_quality_score']
        except Exception as e:
            summary['failed'] += 1
            summary['processing_errors'].append({
                'index': i,
                'error': str(e),
                'data_preview': str(data_item)[:100]
            })
    
    summary['total_processed'] = len(data_list)
    if summary['successful'] > 0:
        summary['average_quality_score'] /= summary['successful']
    
    return {
        'results': results,
        'summary': summary,
        'processed_by_team': team_name,
        'batch_id': hashlib.md5(f"{team_name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
    }


def data_export_helper(processed_data: Dict[str, Any], export_format: str = "json") -> str:
    """
    Export helper that other teams adopted for consistent data output.
    """
    if export_format.lower() == "json":
        return json.dumps(processed_data, indent=2, default=str)
    elif export_format.lower() == "csv":
        # Simple CSV export for flat data
        if isinstance(processed_data, dict) and 'results' in processed_data:
            # Handle batch results
            import csv
            import io
            output = io.StringIO()
            if processed_data['results']:
                writer = csv.DictWriter(output, fieldnames=processed_data['results'][0].keys())
                writer.writeheader()
                for result in processed_data['results']:
                    writer.writerow({k: str(v) for k, v in result.items()})
            return output.getvalue()
    
    return str(processed_data)  # Fallback

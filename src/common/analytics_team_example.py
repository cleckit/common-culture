"""
Example of how the analytics team uses Robert's team extensions.
This shows another team finding value in your sth/robert_common code.
"""

from sth.robert_common.extended_utils import EnhancedLogger, create_team_database_connection
from sth.robert_common.advanced_processing import AdvancedDataProcessor, data_export_helper

class AnalyticsReporter:
    """Analytics team leveraging Robert team's utilities."""
    
    def __init__(self):
        self.logger = EnhancedLogger("analytics_reporter", team="analytics_team")
        self.processor = AdvancedDataProcessor("analytics_team")
        
    def generate_team_report(self, team_data):
        """Generate analytics report using Robert team's processing."""
        self.logger.info_with_context(
            "Starting analytics report generation",
            data_points=len(team_data),
            report_type="team_performance"
        )
        
        # Process each team's data
        processed_results = []
        for team_name, data in team_data.items():
            self.logger.info_with_context(
                f"Processing data for {team_name}",
                team=team_name,
                metrics_count=len(data)
            )
            
            result = self.processor.process_with_validation(data)
            processed_results.append({
                'team': team_name,
                'processed_data': result,
                'quality_score': result['data_quality_score']
            })
        
        # Export using Robert team's export helper
        report_json = data_export_helper({
            'report_type': 'team_analytics',
            'generated_by': 'analytics_team',
            'using_extensions_from': 'robert_team',
            'teams_analyzed': processed_results
        })
        
        self.logger.info_with_context(
            "Analytics report completed",
            teams_processed=len(team_data),
            average_quality=sum(r['quality_score'] for r in processed_results) / len(processed_results)
        )
        
        return report_json

def main():
    """Example analytics workflow using Robert team's code."""
    reporter = AnalyticsReporter()
    
    # Sample team performance data
    team_metrics = {
        'marketing_team': {
            'sprint_velocity': 23,
            'bugs_fixed': 8,
            'features_delivered': 5,
            'team_satisfaction': 4.2
        },
        'product_team': {
            'sprint_velocity': 28,
            'bugs_fixed': 12,
            'features_delivered': 7,
            'team_satisfaction': 4.5
        },
        'robert_team': {
            'sprint_velocity': 31,
            'bugs_fixed': 6,
            'features_delivered': 9,
            'team_satisfaction': 4.7,
            'shared_utilities_created': 3  # Robert team creates reusable code!
        }
    }
    
    report = reporter.generate_team_report(team_metrics)
    print("Analytics team generated report using Robert team's extensions")
    print("Report preview:", report[:200] + "...")

if __name__ == "__main__":
    main()

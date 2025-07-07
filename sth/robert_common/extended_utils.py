"""
Extended utilities that build upon src/common functionality.
This shows how your team can create extensions that other teams might want to use.
"""

# This would normally import from src/common (which you don't have write access to)
# from src.common.base_utils import BaseLogger, BaseConfig
# But for this example, we'll simulate it

import logging
from datetime import datetime
from typing import Dict, Any, Optional

class EnhancedLogger:
    """
    Enhanced logger that extends the basic common logger with team-specific features.
    Other teams might want to use this instead of the basic logger.
    """
    
    def __init__(self, name: str, team: str = "robert_team"):
        self.logger = logging.getLogger(f"{team}.{name}")
        self.team = team
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log_with_context(self, level: str, message: str, context: Optional[Dict[str, Any]] = None):
        """Enhanced logging with context information that other teams find useful."""
        context = context or {}
        enhanced_message = f"[{self.team}][{self.session_id}] {message}"
        if context:
            enhanced_message += f" | Context: {context}"
        
        getattr(self.logger, level.lower())(enhanced_message)
        
    def info_with_context(self, message: str, **kwargs):
        """Convenience method that other teams often request."""
        self.log_with_context("info", message, kwargs)


class TeamConfigManager:
    """
    Configuration manager that extends common config with team-specific patterns.
    This became popular with other teams who wanted similar functionality.
    """
    
    def __init__(self, team_name: str):
        self.team_name = team_name
        # Would normally extend from src.common.ConfigBase
        self.base_config = {
            'debug': True,
            'version': '1.0.0'
        }
        
    def get_team_config(self) -> Dict[str, Any]:
        """Get configuration with team-specific overrides."""
        return {
            **self.base_config,
            'team': self.team_name,
            'team_specific_features': {
                'enhanced_logging': True,
                'custom_metrics': True,
                'team_dashboards': f"https://dashboards.company.com/{self.team_name}"
            }
        }
    
    def get_feature_flag(self, feature: str, default: bool = False) -> bool:
        """Feature flag management that other teams adopted."""
        team_features = self.get_team_config().get('team_specific_features', {})
        return team_features.get(feature, default)


def create_team_database_connection(team: str, environment: str = "dev"):
    """
    Database connection helper that became popular across teams.
    Each team gets their own connection with proper naming conventions.
    """
    # This would normally use src.common.database.BaseConnection
    connection_string = f"postgresql://db-{environment}.company.com/{team}_database"
    
    return {
        'connection_string': connection_string,
        'team': team,
        'environment': environment,
        'connection_pool_size': 10,
        'timeout': 30
    }


def standardized_error_handler(func):
    """
    Decorator for standardized error handling that other teams started copying.
    This pattern became so useful that it should probably be moved to main common.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = EnhancedLogger(func.__name__)
            logger.log_with_context(
                "error",
                f"Function {func.__name__} failed",
                {
                    'args': str(args)[:100],  # Truncate for logging
                    'kwargs': str(kwargs)[:100],
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            )
            raise
    return wrapper

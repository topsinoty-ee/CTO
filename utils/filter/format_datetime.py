from datetime import datetime
from utils.filter import filter_bp


@filter_bp.app_template_filter()
def format_datetime(value, format='%d.%m.%y %H:%M'):
    """Format a date time to (dd-mm-yy hh:mm)"""
    if value is None:
        return ""
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(format)

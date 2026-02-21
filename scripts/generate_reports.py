#!/usr/bin/env python3
"""
METEORICA Report Generator
Generates daily, weekly, monthly reports and alerts
"""

import os
import sys
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from meteorica.database.specimen_registry import SpecimenRegistry
    from meteorica.emi import calculate_emi
except ImportError:
    print("Warning: meteorica package not found, using mock data")
    SpecimenRegistry = None


class ReportGenerator:
    """Generate METEORICA reports in various formats"""
    
    def __init__(self, base_dir: str = None):
        """Initialize report generator"""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        
        self.base_dir = Path(base_dir)
        self.daily_dir = self.base_dir / 'daily'
        self.weekly_dir = self.base_dir / 'weekly'
        self.monthly_dir = self.base_dir / 'monthly'
        self.alerts_dir = self.base_dir / 'alerts'
        self.archive_dir = self.base_dir / 'archive'
        self.exports_dir = self.base_dir / 'exports'
        self.templates_dir = self.base_dir / 'templates'
        
        # Create directories if they don't exist
        for dir_path in [self.daily_dir, self.weekly_dir, self.monthly_dir,
                        self.alerts_dir, self.archive_dir, self.exports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize registry if available
        self.registry = None
        if SpecimenRegistry:
            self.registry = SpecimenRegistry()
    
    def daily_report(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Generate daily report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Load template
        template = self._load_template('daily_template.md')
        
        # Generate data
        data = {
            'date': date,
            'new_classifications': self._get_new_classifications('day'),
            'fireball_events': self._get_fireball_events('day'),
            'db_updates': self._get_db_updates('day'),
            'active_alerts': self._get_active_alerts(),
            'classification_table': self._get_classification_table('day'),
            'fireball_table': self._get_fireball_table('day'),
            'alerts_list': self._format_alerts_list(),
            'total_specimens': self._get_total_specimens(),
            'classified_today': self._get_classified_today(),
            'backlog': self._get_backlog()
        }
        
        # Generate report
        report = template.format(**data)
        
        # Save report
        report_file = self.daily_dir / f"{date}_daily.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        # Export copies
        self._export_report(date, 'daily', report, data)
        
        return {
            'status': 'success',
            'report_file': str(report_file),
            'date': date,
            'data': data
        }
    
    def weekly_report(self, year: Optional[int] = None, 
                     week: Optional[int] = None) -> Dict[str, Any]:
        """Generate weekly report"""
        if year is None:
            year = datetime.now().year
        if week is None:
            week = datetime.now().isocalendar()[1]
        
        # Load template
        template = self._load_template('weekly_template.md')
        
        # Calculate date range
        start_date = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w")
        end_date = start_date + timedelta(days=6)
        
        # Generate data
        data = {
            'week': week,
            'year': year,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'total_classifications': self._get_classifications_week(year, week),
            'new_groups': self._get_new_groups_week(year, week),
            'fireball_events': self._get_fireball_events('week', year, week),
            'growth': self._get_growth_week(year, week),
            'group_stats': self._get_group_stats_week(year, week),
            'significant_fireballs': self._get_significant_fireballs_week(year, week),
            'discoveries': self._get_discoveries_week(year, week),
            'emi_distribution': self._get_emi_distribution_week(year, week),
            'alert_summary': self._get_alert_summary_week(year, week),
            'avg_emi': self._get_avg_emi_week(year, week),
            'top_group': self._get_top_group_week(year, week),
            'ungrouped_count': self._get_ungrouped_week(year, week)
        }
        
        # Generate report
        report = template.format(**data)
        
        # Save report
        report_file = self.weekly_dir / f"{year}-W{week:02d}_weekly.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        # Export copies
        self._export_report(f"{year}-W{week:02d}", 'weekly', report, data)
        
        return {
            'status': 'success',
            'report_file': str(report_file),
            'year': year,
            'week': week,
            'data': data
        }
    
    def monthly_report(self, year: Optional[int] = None,
                      month: Optional[int] = None) -> Dict[str, Any]:
        """Generate monthly report"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # Load template
        template = self._load_template('monthly_template.md')
        
        # Month name
        month_name = datetime(year, month, 1).strftime('%B')
        
        # Generate data
        data = {
            'month': month_name,
            'year': year,
            'summary': self._get_monthly_summary(year, month),
            'total_specimens': self._get_total_specimens(),
            'last_month_total': self._get_total_specimens_month(year, month-1),
            'change_total': self._get_change_percent('total', year, month),
            'classifications': self._get_classifications_month(year, month),
            'last_month_class': self._get_classifications_month(year, month-1),
            'change_class': self._get_change_percent('class', year, month),
            'fireball_events': self._get_fireball_events('month', year, month),
            'last_month_fireball': self._get_fireball_events('month', year, month-1),
            'change_fireball': self._get_change_percent('fireball', year, month),
            'new_groups': self._get_new_groups_month(year, month),
            'last_month_groups': self._get_new_groups_month(year, month-1),
            'change_groups': self._get_change_percent('groups', year, month),
            'alerts': self._get_alerts_month(year, month),
            'last_month_alerts': self._get_alerts_month(year, month-1),
            'change_alerts': self._get_change_percent('alerts', year, month),
            'highlights': self._get_highlights_month(year, month),
            'trends': self._get_trends_month(year, month),
            'discoveries': self._get_discoveries_month(year, month),
            'group_distribution': self._get_group_distribution_month(year, month),
            'alert_analysis': self._get_alert_analysis_month(year, month),
            'papers_submitted': self._get_papers_submitted_month(year, month),
            'dois_issued': self._get_dois_issued_month(year, month),
            'citations': self._get_citations_month(year, month),
            'archived_reports': self._get_archived_count_month(year, month),
            'exported_data': self._get_exported_data_month(year, month),
            'next_month_goals': self._get_next_month_goals(year, month)
        }
        
        # Generate report
        report = template.format(**data)
        
        # Save report
        report_file = self.monthly_dir / f"{year}-{month:02d}_monthly.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        # Export copies
        self._export_report(f"{year}-{month:02d}", 'monthly', report, data)
        
        return {
            'status': 'success',
            'report_file': str(report_file),
            'year': year,
            'month': month,
            'data': data
        }
    
    def alert(self, alert_type: str, severity: str, 
             description: str, details: Dict = None) -> Dict[str, Any]:
        """Generate alert"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        alert_id = f"alert_{timestamp}_{alert_type}"
        
        # Severity mapping
        severity_icons = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴',
            'critical': '⚫'
        }
        
        # Load template
        template = self._load_template('alert_template.md')
        
        data = {
            'alert_id': alert_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'severity': severity.capitalize(),
            'severity_icon': severity_icons.get(severity, '⚪'),
            'alert_type': alert_type.replace('_', ' ').capitalize(),
            'status': 'active',
            'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'expires': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'description': description,
            'affected_items': self._get_affected_items(details),
            'recommended_action': self._get_recommended_action(alert_type, severity),
            'details': json.dumps(details or {}, indent=2)
        }
        
        # Generate alert
        alert = template.format(**data)
        
        # Save alert
        alert_file = self.alerts_dir / f"{alert_id}.md"
        with open(alert_file, 'w') as f:
            f.write(alert)
        
        # Export JSON copy
        json_file = self.exports_dir / 'json' / f"{alert_id}.json"
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return {
            'status': 'success',
            'alert_file': str(alert_file),
            'json_file': str(json_file),
            'alert_id': alert_id,
            'data': data
        }
    
    def export_json(self, report_name: str) -> str:
        """Export report as JSON"""
        json_file = self.exports_dir / 'json' / f"{report_name}.json"
        
        # Find corresponding markdown file
        md_file = None
        for dir_path in [self.daily_dir, self.weekly_dir, self.monthly_dir]:
            candidate = dir_path / f"{report_name}.md"
            if candidate.exists():
                md_file = candidate
                break
        
        if md_file:
            # Copy JSON template
            shutil.copy(json_file, self.exports_dir / 'json' / f"{report_name}.json")
        
        return str(json_file)
    
    def archive_old_reports(self, days: int = 30) -> int:
        """Archive reports older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        archived = 0
        
        for report_dir in [self.daily_dir, self.weekly_dir, self.monthly_dir]:
            for report_file in report_dir.glob("*.md"):
                mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
                if mtime < cutoff:
                    # Move to archive
                    dest = self.archive_dir / report_file.name
                    shutil.move(str(report_file), str(dest))
                    archived += 1
        
        return archived
    
    def _load_template(self, template_name: str) -> str:
        """Load template file"""
        template_file = self.templates_dir / template_name
        if template_file.exists():
            with open(template_file) as f:
                return f.read()
        return ""
    
    def _export_report(self, name: str, report_type: str, 
                       content: str, data: Dict):
        """Export report in multiple formats"""
        # JSON export
        json_file = self.exports_dir / 'json' / f"{name}_{report_type}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'report_type': report_type,
                'name': name,
                'generated': datetime.now().isoformat(),
                'content': content,
                'data': data
            }, f, indent=2)
        
        # CSV export (summary)
        csv_file = self.exports_dir / 'csv' / f"{name}_{report_type}.csv"
        with open(csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Key', 'Value'])
            for key, value in data.items():
                writer.writerow([key, str(value)])
    
    # Mock data methods (would be replaced with actual database queries)
    def _get_new_classifications(self, period: str) -> int:
        return 12
    
    def _get_fireball_events(self, period: str, year: int = None, 
                             week: int = None, month: int = None) -> int:
        return 3
    
    def _get_db_updates(self, period: str) -> int:
        return 5
    
    def _get_active_alerts(self) -> int:
        return 2
    
    def _get_classification_table(self, period: str) -> str:
        return "| M001 | Sample | H | 0.92 | 95% |"
    
    def _get_fireball_table(self, period: str) -> str:
        return "| 2026-02-20 10:30 | Sahara | 18.6 km/s | 23 km | Tracked |"
    
    def _format_alerts_list(self) -> str:
        return "- ⚠️ Ungrouped meteorite detected\n- 🔥 Large fireball event"
    
    def _get_total_specimens(self) -> int:
        return 2847
    
    def _get_classified_today(self) -> int:
        return 8
    
    def _get_backlog(self) -> int:
        return 15234
    
    def _get_classifications_week(self, year: int, week: int) -> int:
        return 45
    
    def _get_new_groups_week(self, year: int, week: int) -> int:
        return 2
    
    def _get_growth_week(self, year: int, week: int) -> int:
        return 15
    
    def _get_group_stats_week(self, year: int, week: int) -> str:
        return "| H | 12 | 487 | +2% |"
    
    def _get_significant_fireballs_week(self, year: int, week: int) -> str:
        return "- Chelyabinsk-like event: 18.6 km/s, 23 km altitude"
    
    def _get_discoveries_week(self, year: int, week: int) -> str:
        return "- New ungrouped carbonaceous chondrite"
    
    def _get_emi_distribution_week(self, year: int, week: int) -> str:
        return "Average EMI: 0.76"
    
    def _get_alert_summary_week(self, year: int, week: int) -> str:
        return "| High | 1 | 0 |"
    
    def _get_avg_emi_week(self, year: int, week: int) -> float:
        return 0.76
    
    def _get_top_group_week(self, year: int, week: int) -> str:
        return "H"
    
    def _get_ungrouped_week(self, year: int, week: int) -> int:
        return 3
    
    def _get_monthly_summary(self, year: int, month: int) -> str:
        return "This month saw significant progress in classification..."
    
    def _get_total_specimens_month(self, year: int, month: int) -> int:
        return 2800
    
    def _get_change_percent(self, metric: str, year: int, month: int) -> str:
        return "+5%"
    
    def _get_classifications_month(self, year: int, month: int) -> int:
        return 180
    
    def _get_new_groups_month(self, year: int, month: int) -> int:
        return 3
    
    def _get_alerts_month(self, year: int, month: int) -> int:
        return 8
    
    def _get_highlights_month(self, year: int, month: int) -> str:
        return "- 3 new ungrouped meteorites identified\n- Major fireball event recorded"
    
    def _get_trends_month(self, year: int, month: int) -> str:
        return "Increasing number of carbonaceous chondrites"
    
    def _get_group_distribution_month(self, year: int, month: int) -> str:
        return "H: 35%, L: 30%, LL: 20%, Others: 15%"
    
    def _get_alert_analysis_month(self, year: int, month: int) -> str:
        return "8 alerts generated, 5 resolved"
    
    def _get_papers_submitted_month(self, year: int, month: int) -> int:
        return 2
    
    def _get_dois_issued_month(self, year: int, month: int) -> int:
        return 1
    
    def _get_citations_month(self, year: int, month: int) -> int:
        return 15
    
    def _get_archived_count_month(self, year: int, month: int) -> int:
        return 30
    
    def _get_exported_data_month(self, year: int, month: int) -> str:
        return "45 specimens exported"
    
    def _get_next_month_goals(self, year: int, month: int) -> str:
        return "- Complete classification of backlog\n- Submit paper on ungrouped meteorites"
    
    def _get_affected_items(self, details: Dict) -> str:
        return "- Specimen: METEORICA_001\n- Analysis: MCC, IAF"
    
    def _get_recommended_action(self, alert_type: str, severity: str) -> str:
        return "Review classification and submit to expert committee"


def main():
    """Command line interface for report generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='METEORICA Report Generator')
    parser.add_argument('--daily', action='store_true', help='Generate daily report')
    parser.add_argument('--weekly', action='store_true', help='Generate weekly report')
    parser.add_argument('--monthly', action='store_true', help='Generate monthly report')
    parser.add_argument('--archive', type=int, metavar='DAYS', 
                       help='Archive reports older than DAYS')
    parser.add_argument('--date', help='Date for daily report (YYYY-MM-DD)')
    parser.add_argument('--year', type=int, help='Year for weekly/monthly')
    parser.add_argument('--week', type=int, help='Week number for weekly')
    parser.add_argument('--month', type=int, help='Month number for monthly')
    
    args = parser.parse_args()
    
    gen = ReportGenerator()
    
    if args.daily:
        result = gen.daily_report(args.date)
        print(f"Daily report generated: {result['report_file']}")
    
    if args.weekly:
        result = gen.weekly_report(args.year, args.week)
        print(f"Weekly report generated: {result['report_file']}")
    
    if args.monthly:
        result = gen.monthly_report(args.year, args.month)
        print(f"Monthly report generated: {result['report_file']}")
    
    if args.archive:
        count = gen.archive_old_reports(args.archive)
        print(f"Archived {count} old reports")


if __name__ == '__main__':
    main()

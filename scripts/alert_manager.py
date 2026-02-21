#!/usr/bin/env python3
"""
Alert Manager for METEORICA
Manages alerts and notifications
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

class AlertManager:
    def __init__(self):
        self.alerts_dir = Path("reports/alerts")
        self.exports_dir = Path("reports/exports/json")
        
    def check_ungrouped(self, specimen_data):
        """Check for ungrouped meteorites"""
        if specimen_data.get('group') == 'UNG':
            self.create_alert(
                alert_type='ungrouped',
                severity='high',
                description=f"Ungrouped meteorite detected: {specimen_data.get('id')}",
                details=specimen_data
            )
    
    def check_fireball(self, fireball_data):
        """Check for significant fireball events"""
        if fireball_data.get('energy_kt', 0) > 100:
            self.create_alert(
                alert_type='fireball',
                severity='high',
                description=f"Large fireball detected: {fireball_data.get('event_id')}",
                details=fireball_data
            )
    
    def create_alert(self, alert_type, severity, description, details=None):
        """Create new alert"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        alert_id = f"alert_{timestamp}_{alert_type}"
        
        alert = {
            'id': alert_id,
            'type': alert_type,
            'severity': severity,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(days=7)).isoformat(),
            'status': 'active',
            'details': details or {}
        }
        
        # Save alert
        alert_file = self.alerts_dir / f"{alert_id}.json"
        with open(alert_file, 'w') as f:
            json.dump(alert, f, indent=2)
        
        # Also save to exports
        export_file = self.exports_dir / f"{alert_id}.json"
        with open(export_file, 'w') as f:
            json.dump(alert, f, indent=2)
        
        print(f"Alert created: {alert_id}")
        return alert
    
    def get_active_alerts(self):
        """Get all active alerts"""
        alerts = []
        for alert_file in self.alerts_dir.glob("*.json"):
            with open(alert_file) as f:
                alert = json.load(f)
                if alert['status'] == 'active':
                    # Check if expired
                    expires = datetime.fromisoformat(alert['expires'])
                    if datetime.now() > expires:
                        alert['status'] = 'expired'
                        self.update_alert(alert)
                    else:
                        alerts.append(alert)
        return alerts
    
    def resolve_alert(self, alert_id):
        """Resolve an alert"""
        alert_file = self.alerts_dir / f"{alert_id}.json"
        if alert_file.exists():
            with open(alert_file) as f:
                alert = json.load(f)
            alert['status'] = 'resolved'
            alert['resolved_at'] = datetime.now().isoformat()
            with open(alert_file, 'w') as f:
                json.dump(alert, f, indent=2)
            return True
        return False
    
    def update_alert(self, alert):
        """Update alert status"""
        alert_file = self.alerts_dir / f"{alert['id']}.json"
        with open(alert_file, 'w') as f:
            json.dump(alert, f, indent=2)


if __name__ == '__main__':
    manager = AlertManager()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'list':
            alerts = manager.get_active_alerts()
            print(f"Active alerts: {len(alerts)}")
            for alert in alerts:
                print(f"  {alert['severity']}: {alert['description']}")
        elif sys.argv[1] == 'resolve' and len(sys.argv) > 2:
            if manager.resolve_alert(sys.argv[2]):
                print(f"Alert {sys.argv[2]} resolved")
            else:
                print(f"Alert {sys.argv[2]} not found")

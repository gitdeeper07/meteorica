"""
Integration with fireball camera networks.
"""

class NetworkIntegrator:
    """Integrate multiple fireball networks."""
    
    def __init__(self):
        self.networks = []
    
    def add_network(self, network):
        """Add a fireball network."""
        self.networks.append(network)
    
    def get_all_events(self, time_range):
        """Get events from all networks."""
        events = []
        for network in self.networks:
            events.extend(network.get_events(time_range[0], time_range[1]))
        return events

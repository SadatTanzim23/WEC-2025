"""
Trade system - balances resources between villages
"""

import math
import constants as C

class TradeCart:
    """Represents a cart traveling between villages with resources"""
    def __init__(self, from_village, to_village, resources, start_pos, end_pos):
        self.from_village = from_village
        self.to_village = to_village
        self.resources = resources  # Dict of resources being transported
        self.position = list(start_pos)  # Current position [x, y]
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.progress = 0.0  # 0 to 1
        
        # Calculate distance and duration
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        self.distance = math.sqrt(dx*dx + dy*dy)
        self.duration = C.SECONDS_PER_MONTH  # Takes one month cycle
        self.elapsed = 0.0
    
    def update(self, dt):
        """Update cart position"""
        self.elapsed += dt
        self.progress = min(1.0, self.elapsed / self.duration)
        
        # Linear interpolation
        self.position[0] = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        self.position[1] = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        
        return self.progress >= 1.0  # Returns True when arrived


class TradeSystem:
    """Manages resource balancing and trade between villages"""
    def __init__(self, villages):
        self.villages = villages
        self.active_carts = []
    
    def calculate_trades(self):
        """Main algorithm: balance resources across all villages"""
        trades = []  # List of (from_village, to_village, resource, amount)
        
        # Build network of alive villages
        alive_villages = [v for v in self.villages if v.is_alive]
        
        # For each resource type
        for resource in C.RESOURCES:
            # Calculate surplus and deficit for each village
            surpluses = []  # (village, surplus_amount)
            deficits = []   # (village, deficit_amount, urgency)
            
            for village in alive_villages:
                survival_threshold, growth_threshold = village.calculate_thresholds()
                current = village.resources[resource]
                
                # Check if village is blocked from receiving (plague, lightning)
                can_receive = not (
                    village.has_event_type('plague') or
                    village.has_event_type('lightning')
                )
                
                # Determine if surplus or deficit
                if current > growth_threshold * 1.5:
                    # Has surplus
                    surplus = current - growth_threshold
                    surpluses.append((village, surplus))
                
                elif current < growth_threshold and can_receive:
                    # Has deficit
                    deficit = growth_threshold - current
                    
                    # Calculate urgency (closer to death = higher urgency)
                    if current < survival_threshold:
                        urgency = 1000  # CRITICAL - city will die
                    else:
                        urgency = deficit / growth_threshold
                    
                    deficits.append((village, deficit, urgency))
            
            # Sort deficits by urgency (most urgent first)
            deficits.sort(key=lambda x: x[2], reverse=True)
            
            # Allocate resources from surplus to deficit
            for deficit_village, deficit_amount, urgency in deficits:
                needed = deficit_amount
                
                # Find nearest surplus villages
                surplus_distances = []
                for surplus_village, surplus_amount in surpluses:
                    if surplus_amount > 0:
                        # Calculate distance
                        dx = surplus_village.position[0] - deficit_village.position[0]
                        dy = surplus_village.position[1] - deficit_village.position[1]
                        distance = math.sqrt(dx*dx + dy*dy)
                        
                        # Check if route is blocked
                        route_blocked = (
                            surplus_village.has_event_type('lightning') or
                            surplus_village.has_event_type('plague')
                        )
                        
                        if not route_blocked:
                            surplus_distances.append((surplus_village, surplus_amount, distance))
                
                # Sort by distance (nearest first)
                surplus_distances.sort(key=lambda x: x[2])
                
                # Allocate from nearest surplus villages
                for surplus_village, surplus_amount, distance in surplus_distances:
                    if needed <= 0:
                        break
                    
                    # Calculate how much to send
                    send_amount = min(needed, surplus_amount, surplus_amount * 0.6)  # Max 60% of surplus
                    
                    if send_amount > 5:  # Only send if meaningful amount
                        trades.append((surplus_village, deficit_village, resource, send_amount))
                        
                        # Update surplus tracking
                        for i, (v, amt) in enumerate(surpluses):
                            if v == surplus_village:
                                surpluses[i] = (v, amt - send_amount)
                                break
                        
                        needed -= send_amount
        
        return trades
    
    def execute_trades(self, trades):
        """Create trade carts for all trades"""
        for from_village, to_village, resource, amount in trades:
            # Deduct resources from source
            from_village.resources[resource] -= amount
            
            # Apply trade efficiency
            actual_amount = amount * C.TRADE_EFFICIENCY
            
            # Create cart
            cart = TradeCart(
                from_village.name,
                to_village.name,
                {resource: actual_amount},
                from_village.position,
                to_village.position
            )
            self.active_carts.append(cart)
    
    def update(self, dt):
        """Update all active trade carts"""
        completed = []
        
        for cart in self.active_carts:
            if cart.update(dt):
                completed.append(cart)
        
        # Deliver completed carts
        for cart in completed:
            # Find destination village
            for village in self.villages:
                if village.name == cart.to_village:
                    # Add resources
                    for resource, amount in cart.resources.items():
                        village.resources[resource] += amount
                    break
            
            self.active_carts.remove(cart)
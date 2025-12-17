from typing import Tuple, List
from utils import test_interieur_safezone
import random
import math

class QIXMovement:
    """
    Handles QIX enemy movement with target-based curved trajectory algorithm.
    
    The QIX moves towards random targets using curved paths with sine wave
    patterns, changing targets more frequently when close to the current target.
    """
    
    def __init__(self, playfield_bounds: Tuple[Tuple[float, float], Tuple[float, float]], 
                 qix_size: float, initial_speed: float):
        """
        Initialize QIX movement system.
        
        Args:
            playfield_bounds: ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))
            qix_size: Size of the QIX square
            initial_speed: Base movement speed
        """
        self.bounds_top_left = playfield_bounds[0]
        self.bounds_bottom_right = playfield_bounds[1]
        self.qix_size = qix_size
        self.base_speed = initial_speed
        self.boundary_offset = 25.0
        
        # Current position
        self.x = (self.bounds_top_left[0] + self.bounds_bottom_right[0]) / 2
        self.y = (self.bounds_top_left[1] + self.bounds_bottom_right[1]) / 2
        
        # Movement state
        self.target_x = random.uniform(self.bounds_top_left[0] + 50, self.bounds_bottom_right[0] - 50)
        self.target_y = random.uniform(self.bounds_top_left[1] + 50, self.bounds_bottom_right[1] - 50)
        self.movement_timer = 0
        
        # Arc parameters for single-curve trajectory
        self.arc_direction = random.choice([-1, 1])  # Left or right curve
        self.arc_strength = random.uniform(1.5, 2.5)  # How pronounced the arc is
        self.trajectory_start_x = self.x  # Starting position for this trajectory
        self.trajectory_start_y = self.y
        self.total_trajectory_distance = 0.0  # Will be set when target changes
    
    def _choose_new_target(self, unsafe_zone: List[Tuple[float, float]]) -> None:
        """Choose a new target avoiding safe zones using simple but effective sampling."""
        margin = 30
        
        for _ in range(8):  # Just 8 attempts
            new_target_x = random.uniform(self.bounds_top_left[0] + margin, self.bounds_bottom_right[0] - margin)
            new_target_y = random.uniform(self.bounds_top_left[1] + margin, self.bounds_bottom_right[1] - margin)
            
            if test_interieur_safezone(unsafe_zone, new_target_x, new_target_y):
                self._set_new_target(new_target_x, new_target_y)
                return
        
        # Pick direction from current position
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(80, 150)
        fallback_x = self.x + math.cos(angle) * distance
        fallback_y = self.y + math.sin(angle) * distance
        
        # Clamp to valid bounds
        fallback_x = max(self.bounds_top_left[0] + margin, min(self.bounds_bottom_right[0] - margin, fallback_x))
        fallback_y = max(self.bounds_top_left[1] + margin, min(self.bounds_bottom_right[1] - margin, fallback_y))
        
        self._set_new_target(fallback_x, fallback_y)
    
    def _set_new_target(self, x: float, y: float) -> None:
        """Set new target and reset arc parameters."""
        self.target_x = x
        self.target_y = y
        # Reset arc parameters for new trajectory
        self.arc_direction = random.choice([-1, 1])
        self.arc_strength = random.uniform(1.5, 2.5)
        self.trajectory_start_x = self.x
        self.trajectory_start_y = self.y
        self.total_trajectory_distance = math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
    
    def _update_arc_parameters(self) -> None:
        """Gradually evolve arc parameters for dynamic movement patterns."""
        # Occasionally adjust arc parameters slightly for variation
        if random.random() < 0.003:  # 0.3% chance each frame
            self.arc_strength += random.uniform(-0.2, 0.2)
            self.arc_strength = max(1.0, min(3.0, self.arc_strength))
    
    def update(self, unsafe_zone: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Update QIX position and return new coordinates.
        
        Args:
            unsafe_zone: List of unsafe zone coordinates to avoid
            
        Returns:
            Tuple of (new_x, new_y) coordinates
        """
        self.movement_timer += 1
        
        # Gradually evolve arc parameters for dynamic behavior
        self._update_arc_parameters()
        
        # Calculate distance to current target
        dx_to_target = self.target_x - self.x
        dy_to_target = self.target_y - self.y
        distance_to_target = (dx_to_target**2 + dy_to_target**2)**0.5
        
        # Probability of changing target increases as QIX gets closer
        max_distance = 200
        proximity_factor = max(0, (max_distance - distance_to_target) / max_distance)
        change_probability = proximity_factor * 0.02
        
        # Change target based on proximity or randomly
        if distance_to_target < 30 or random.random() < change_probability:
            self._choose_new_target(unsafe_zone)
            # Recalculate after potential target change
            dx_to_target = self.target_x - self.x
            dy_to_target = self.target_y - self.y
            distance_to_target = (dx_to_target**2 + dy_to_target**2)**0.5
        
        # Calculate movement with single arc trajectory
        if distance_to_target > 5:
            # Base direction to target
            dir_x = dx_to_target / distance_to_target
            dir_y = dy_to_target / distance_to_target
            
            # Calculate perpendicular direction for arc
            perp_x = -dir_y  # Perpendicular to movement direction
            perp_y = dir_x
            
            # Calculate trajectory progress (0.0 at start, 1.0 at target)
            if self.total_trajectory_distance > 0:
                distance_traveled = math.sqrt((self.x - self.trajectory_start_x)**2 + (self.y - self.trajectory_start_y)**2)
                trajectory_progress = min(distance_traveled / self.total_trajectory_distance, 1.0)
            else:
                trajectory_progress = 0.0
            
            # Create single arc curve using sine function
            arc_value = math.sin(trajectory_progress * math.pi) * self.arc_direction * self.arc_strength
            
            # Apply arc offset with stronger effect
            curved_dir_x = dir_x + perp_x * arc_value * 0.4
            curved_dir_y = dir_y + perp_y * arc_value * 0.4
            
            # Normalize the curved direction
            curved_length = math.sqrt(curved_dir_x**2 + curved_dir_y**2)
            if curved_length > 0:
                curved_dir_x /= curved_length
                curved_dir_y /= curved_length
            
            # Move with arc trajectory
            current_speed = self.base_speed * 0.8
            dx = curved_dir_x * current_speed
            dy = curved_dir_y * current_speed
        else:
            # Minor movement when very close to target
            dx = random.uniform(-1, 1) * self.base_speed * 0.2
            dy = random.uniform(-1, 1) * self.base_speed * 0.2
        
        # Check boundaries and safe zones
        next_x = self.x + dx
        next_y = self.y + dy
        
        # Handle boundary collision or safe zone entry
        if (next_x <= self.bounds_top_left[0] + self.boundary_offset or 
            next_x >= self.bounds_bottom_right[0] - self.boundary_offset or
            next_y <= self.bounds_top_left[1] + self.boundary_offset or 
            next_y >= self.bounds_bottom_right[1] - self.boundary_offset or
            not test_interieur_safezone(unsafe_zone, next_x, next_y)):
            self._choose_new_target(unsafe_zone)
        
        # Apply movement with boundary constraints
        self.x = max(self.bounds_top_left[0] + self.boundary_offset, 
                    min(self.bounds_bottom_right[0] - self.boundary_offset, next_x))
        self.y = max(self.bounds_top_left[1] + self.boundary_offset, 
                    min(self.bounds_bottom_right[1] - self.boundary_offset, next_y))
        
        return (self.x, self.y)
    
    def get_position(self) -> Tuple[float, float]:
        """Get current QIX position."""
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float) -> None:
        """Set QIX position (useful for initialization)."""
        self.x = x
        self.y = y
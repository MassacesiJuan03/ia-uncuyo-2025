import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent

class RandomAgent(BaseAgent):
    """
    Your vacuum cleaner agent implementation.
    """
    
    def __init__(self, server_url="http://localhost:5000", **kwargs):
        super().__init__(server_url, "RandomAgent", **kwargs)
        
        # Add your initialization code here
        self.movements = [self.up, self.down, self.left, self.right, self.idle, self.suck]
            
    def get_strategy_description(self):
        return "Random Agent: Moves randomly "
    
    def think(self):
        """
        Your agent's decision-making logic goes here.
        Return True if an action was performed, False to end simulation.
        """
        if not self.is_connected():
            return False
        
        
        perception = self.get_perception()
        if not perception or perception.get('is_finished', True):
            return False

        # REGLA: Realizar una acción aleatoria
        move_function = random.choice(self.movements)
        return move_function()

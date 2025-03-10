import pygame
import numpy as np

class AI_Agent:
    
    def __init__(self) -> None:
        pass

    def getAction (self, q_values):#, state
        """Get the action based on the DQN output (3 Q-values)."""
        #if len(q_values) != 3:
         #   raise ValueError("Expected 3 Q-values (Left, Stay, Right).")

        action_index = np.argmax(q_values)

        return action_index

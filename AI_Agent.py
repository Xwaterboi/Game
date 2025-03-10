import numpy as np
import torch
from DQN import DQN  # Import the DQN class

class AI_Agent:
    def __init__(self, dqn_model, device=torch.device("cpu")):
        self.dqn_model = dqn_model.to(device)
        self.device = device

    def getAction(self, state):
        """Get the action based on the DQN output."""
        self.dqn_model.eval()
        with torch.no_grad():
            state_tensor = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
            q_values = self.dqn_model(state_tensor).cpu().numpy()[0]
            action_index = np.argmax(q_values)
            return action_index

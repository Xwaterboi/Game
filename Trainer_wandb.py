import pygame
import torch
#from CONSTANTS import *
from Environment import Environment  # This should represent your game environment
from AI_Agent import AI_Agent
from ReplayBuffer import ReplayBuffer
import os
from graphics import Background
from DQN import DQN

# Commented out Wandb import
# import wandb  

def main():

    pygame.init()
    WIDTH = 400
    HEIGHT = 800
    # Initialize the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Car Game')

    # Initialize the Background for rendering
    background = Background(WIDTH, HEIGHT)

    # Initialize the Environment (this should handle the logic of the car, obstacles, etc.)
    env = Environment()  # Pass the surface to the Environment class
    background.render(env)  # Initial render

    # DQN Setup
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    dqn_model = DQN()

    MODEL_PATH = "model/DQN.pth"  # Ensure cross-platform path

    dqn_model.load_params(MODEL_PATH)
    print("Model loaded successfully!")
    # DQN Agent setup
    player = AI_Agent(dqn_model=dqn_model)
    player_hat = AI_Agent(dqn_model=dqn_model)
    player_hat.DQN = player.DQN.copy()  # Copy model for the target network
    batch_size = 128
    buffer = ReplayBuffer(path=None)
    learning_rate = 0.0001
    epochs = 200000  # Total number of epochs
    start_epoch = 0
    C, tau = 3, 0.001
    loss = torch.tensor(0)
    avg = 0
    scores, losses, avg_score = [], [], []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim, [5000*1000, 10000*1000, 15000*1000, 20000*1000, 25000*1000, 30000*1000], gamma=0.5)
    step = 0

    # Load checkpoint if exists
    num = 200
    checkpoint_path = f"Data/checkpoint{num}.pth"
    buffer_path = f"Data/buffer{num}.pth"
    resume_wandb = False
    if os.path.exists(checkpoint_path):
        resume_wandb = True
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch'] + 1
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        losses = checkpoint['loss']
        scores = checkpoint['scores']
        avg_score = checkpoint['avg_score']

    player.DQN.train()
    player_hat.DQN.eval()

    # Main loop
    for epoch in range(start_epoch, epochs):
        env.reset()  # Reset the environment (start a new game)
        end_of_game = False
        state = env.state()  # Get the initial state of the environment
        
        while not end_of_game:
            print(step, end='\r')
            step += 1
            background.render(env)  # Render the game state on the screen

            # Handle events like quitting
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return

            # Get action from the agent
            action = player.get_Action(state=state, epoch=epoch)
            reward, done = env.move(action=action)  # Get the reward and whether the game is done
            next_state = env.state()  # Get the next state after the action

            # Store the experience in the replay buffer
            buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32),
                        next_state, torch.tensor(done, dtype=torch.float32))

            # If the game ends, update the best score and break
            if done:
                best_score = max(best_score, env.score)
                break

            state = next_state

            # If buffer is too small, continue to the next loop
            if len(buffer) < 5000:
                continue

            # Sample a batch and train the agent
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = player.Q(states, actions)
            next_actions, Q_hat_Values = player_hat.get_Actions_Values(next_states)

            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            scheduler.step()

        if epoch % C == 0:
            player_hat.fix_update(dqn=player.DQN)  # Update the target network

        print(f'epoch: {epoch} loss: {loss:.7f} LR: {scheduler.get_last_lr()} step: {step} ' \
               f'score: {env.score} best_score: {best_score}')
        step = 0

        if epoch % 10 == 0:
            scores.append(env.score)
            losses.append(loss.item())

        avg = (avg * (epoch % 10) + env.score) / (epoch % 10 + 1)
        if (epoch + 1) % 10 == 0:
            avg_score.append(avg)
            print(f'average score last 10 games: {avg}')
            avg = 0

        if epoch % 1000 == 0 and epoch > 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'loss': losses,
                'scores': scores,
                'avg_score': avg_score
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)

WHITE = (255, 255, 255)
BLACK = (0,0,0)
def write(surface, text, pos=(50, 20)):
    font = pygame.font.SysFont("arial", 36)
    text_surface = font.render(text, True, BLACK, WHITE)
    surface.blit(text_surface, pos)


if __name__ == "__main__":
    main()

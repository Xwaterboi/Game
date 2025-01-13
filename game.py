import pygame
import sprites
from graphics import Background
import random
from Human_Agent import Human_Agent
from Environment import Environment



pygame.init()
run=True
FPS = 60
WINDOWWIDTH = 400
WINDOWHEIGHT = 800

clock = pygame.time.Clock()
background=Background(WINDOWWIDTH, WINDOWHEIGHT)
env = Environment()
background.render(env)
player = Human_Agent()
class game:
    def __init__(self):
        pass

    def start_new_game(self):
        self.loop()

    
    def loop(self):
        """Resets the environment, agent, and game state to start a new game."""
        self.score = 0
        # Reinitialize the agent and environment objects (reset their state)
        clock = pygame.time.Clock()
        background=Background(WINDOWWIDTH, WINDOWHEIGHT)
        env = Environment()
        background.render(env)
        player = Human_Agent()

        self.duration = 30000
        start_time = pygame.time.get_ticks()
        # Start the game loop for the new game
        run = True
        win=False
        while run:
            dt = clock.tick(FPS) 
            win=False
            pygame.event.pump()

            events = pygame.event.get()
            for event in events:
                if event.type==pygame.QUIT:
                    run=False
                    pygame.quit()
                    exit()
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time >= self.duration :
                print("30 seconds! win!")
                win=True
                
                
            if env.score >=5:
                print("5 points! win!")
                win=True
                

            action = player.getAction(events)  













            env.move(action=action)
            done = env.update()
            done=win
            if done:
                background.end_screen()
            else:
                background.render(env)
            pygame.display.flip()

        pygame.quit()
game=game()
game.start_new_game()
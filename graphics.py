import pygame
from Environment import *
# Colors
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height-100
        self.down = 0

        pygame.font.init()
        self.display = pygame.display.set_mode((width,height))#+100
        self.header_surf = pygame.Surface((width, 100))
        self.surface = pygame.Surface((width, height))
        self.header_surf.fill(WHITE)
        self.header_rect = pygame.Rect(0, 0, width, 100)
        self.surface.fill(GRAY)
        self.draw_dashed_lines()
      
        
        pygame.display.set_caption('Endless Road')
        

    def draw_dashed_lines(self):
        dash_length = 15
        dash_width = 5
        lane_width = 80
        

        for x in range(lane_width, self.width, lane_width):
            self.draw_dashed_line((x, self.down), (x, self.height), dash_width, dash_length)

    def draw_dashed_line(self, start_pos, end_pos, width, dash_length):
        x1, y1 = start_pos
        x2, y2 = end_pos

        if x1 == x2:  # Vertical dashed line
            y_coords = list(range(y1, y2, dash_length * 2))
            for y in y_coords:
                pygame.draw.line(self.surface, WHITE, (x1, y), (x2, y + dash_length), width)
    
    def write (self,surface, text, pos = (50, 20)):
        font = pygame.font.SysFont("arial", 36)
        text_surface = font.render(text, True, BLACK, WHITE)
        surface.blit(text_surface, pos)

    def draw_surface (self):
        self.down = (self.down + 1) % 30
        width, height = self.width, self.height
        self.surface = pygame.Surface((width, height))
        self.surface.fill(GRAY)
        self.draw_dashed_lines()

    # def render(self, env):
    #     #self.good=Environment.score
    #     self.draw_surface()
    #     self.display.blit(self.header_surf, (0, 0))
    #     self.display.blit(self.surface, (0, 100))
    #     self.write (surface=self.header_surf, text="Score: " + str(env.score))
    
    #     for obstacle in env.obstacles_group:
    #         if obstacle.rect.colliderect(self.header_rect):
    #             obstacle.visible = False
    #         else:
    #             obstacle.visible = True
    #     env.car.draw(self.display)
    #     env.obstacles_group.draw(self.display)
    #     env.good_points_group.draw(self.display)  
    def render(self, env):
        self.draw_surface()  # Redraw scrolling background
       
        # Draw the score
        self.write(surface=self.header_surf, text="Score: " + str(env.score))

        # Draw obstacles and good points with an offset
        for obstacle in env.obstacles_group:
            self.surface.blit(obstacle.image, (obstacle.rect.x, obstacle.rect.y))
        
        for good_point in env.good_points_group:
            self.surface.blit(good_point.image, (good_point.rect.x, good_point.rect.y))

        # Draw car without any offset
        env.car.draw(self.surface)
        self.display.blit(self.header_surf, (0, 0))  # Draw the header
        self.display.blit(self.surface, (0, 100))  # Draw the main play surface



            
    
    

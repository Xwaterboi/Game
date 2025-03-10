from sprites import *
import torch
import graphics as D
class Environment:
    def __init__(self) -> None:
        self.car = Car(2)
        self.obstacles_group = pygame.sprite.Group()
        self.good_points_group= pygame.sprite.Group()
        #self.spawn_timer = 0
        self.score=0


    def move (self, action):
        lane = self.car.lane
        if action == 1 and lane < 4:
            self.car.lane +=1
        if action == -1 and lane > 0:
            self.car.lane -=1
    
    # def _check_obstacle_placement(self, obstacle):
    #     collided=pygame.sprite.spritecollide(obstacle,self.obstacles_group,True)
    #     return collided is not None
    def _check_obstacle_placement(self, obstacle):
        collided = pygame.sprite.spritecollide(obstacle, self.obstacles_group, False)
        collided2 = pygame.sprite.spritecollide(obstacle, self.good_points_group, False)
        return len(collided) == 0 and len(collided2) == 0  # Return True if no collisions

       

    def Max_obstacle_check(self):
        """Checks if there are more than 10 obstacles in the game."""
        if len(self.obstacles_group) >= 10:
            return True  # More than 10 obstacles exist
        else:
            return False # 10 or fewer obstacles exist
            
    def Max_GoodPoints_check(self):
        """Checks if there are more than 10 good points in the game."""
        if len(self.good_points_group) >= 5:
            return True  # More than 5 points exist
        else:
            return False # 5 or fewer points exist
        
    def add_obstacle(self):
        spawn_probability = 0.017  
        if random.random() < spawn_probability:
            obstacle = Obstacle()
            obstacle.rect.x = random.randrange(0, 400, 80)
            obstacle.rect.y = -obstacle.rect.height  # Spawn at the top of the screen
            if self._check_obstacle_placement(obstacle) and self.Max_obstacle_check() is False:
                self.obstacles_group.add(obstacle)


    def add_coins (self):
        # Spawn good points (optional)
        spawn_good_point_probability = 0.007  
        if random.random() < spawn_good_point_probability:
            good_point = GoodPoint()
            if self._check_obstacle_placement(good_point) and self.Max_GoodPoints_check() is False:
                self.good_points_group.add(good_point)

    def car_colide(self) -> bool :
        colides = pygame.sprite.spritecollide(self.car,self.obstacles_group,False)
        return len(colides) ==0

    def AddGood(self):
        # pointCollided=pygame.sprite.spritecollide(self.car,self.good_points_group,True)
        # if len(pointCollided) != 0:
        #     self.score+=1
        # Custom collision detection for coins
        if len(pygame.sprite.spritecollide(self.car,self.good_points_group,True)) !=0:
             self.score += 1  # Increment the score
        for sprite in self.good_points_group:
            rect = sprite.rect


    def reset(self):#for AI, we dont need screen,  print is good enough.
        from game import game
        print(self.score)
        game.loop()

    def state(self):
        state_list = []

        # 1. Car's Lane
        state_list.append(self.car.lane)  # Add the car's lane 0-4

        # 2. Obstacle Positions
        for obstacle in self.obstacles_group:
            state_list.append(obstacle.lane)  # X-coordinate of obstacle
            state_list.append(obstacle.rect.y/100)  # Y-coordinate of obstacle
        while (len(state_list)<21):
            state_list.append(-1)  
            state_list.append(-1)  
        # 3. Good Point Positions
        for good_point in self.good_points_group:
            state_list.append(good_point.lane)  # X-coordinate of good point
            state_list.append(good_point.rect.y/100)  # Y-coordinate of good point
        while (len(state_list)<41):
            state_list.append(-1)  
            state_list.append(-1)


        return torch.tensor(state_list, dtype=torch.float32)

    def update (self):
        
        self.add_obstacle()
        self.add_coins()
        if not self.car_colide():
           return True
        self.AddGood()

        # Update game objects
        self.car.update()
        self.obstacles_group.update()
        self.good_points_group.update()
        for obstacle in self.obstacles_group:
            if obstacle.rect.top > 800 :
                obstacle.kill()
                self.obstacles_group.remove(obstacle)
        for GoodPoint in self.good_points_group:
            if GoodPoint.rect.top > 800 :
                GoodPoint.kill()
                self.good_points_group.remove(obstacle)
        return False
        # self.spawn_timer += 1 `` # Optional, for tracking spawn frequency
        # Check for off-screen obstacles and remove them
        # for obstacle in self.obstacles_group:
        #     if obstacle.rect.top > 800:
                 
        
        

    


from sprites import *

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

       


    def add_obstacle(self):
        spawn_probability = 0.017  
        if random.random() < spawn_probability:
            obstacle = Obstacle()
            obstacle.rect.x = random.randrange(0, 400, 80)
            obstacle.rect.y = -obstacle.rect.height  # Spawn at the top of the screen
            if self._check_obstacle_placement(obstacle):
                self.obstacles_group.add(obstacle)


    def add_coins (self):
        # Spawn good points (optional)
        spawn_good_point_probability = 0.007  
        if random.random() < spawn_good_point_probability:
            good_point = GoodPoint()
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



    def update (self):
        
        self.add_obstacle()
        self.add_coins()
        if self.car_colide() is False:
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
                 
        
        

    


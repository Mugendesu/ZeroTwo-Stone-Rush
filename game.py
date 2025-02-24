import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120 
STONE_INTERAL = 30
START_SCENE = 'start'
PLAY_SCENE = 'play'
GAME_OVER_DISPLAY_TIME = 120

class Stone:
    def __init__(self , x , y):
        self.x = x
        self.y = y
    
    def update(self):
        if self.y < SCREEN_HEIGHT : self.y += 1
        
    def draw(self):
        pyxel.blt(self.x , self.y , 0 , 8 , 0 , 8 , 8 , pyxel.COLOR_BLACK)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH , SCREEN_HEIGHT , title='ZeroTwo Rush')
        pyxel.mouse(True)
        self.current_scene = START_SCENE
        pyxel.load('my_resource.pyxres')
        pyxel.playm(0 , loop=True)
        pyxel.run(self.update , self.draw)
    
    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.stones = []
        self.is_collision = False
        self.score = 0
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIME
        
    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE
        
    def update_play_scene(self):
        
        if self.is_collision :
            if self.game_over_display_timer > 0: self.game_over_display_timer -= 1
            else : self.current_scene = START_SCENE
            return
        
        # To move the Player
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 12: self.player_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > -4 : self.player_x -= 1
        
        if pyxel.frame_count % STONE_INTERAL == 0:
            self.stones.append(Stone(pyxel.rndi(0 , SCREEN_WIDTH - 8) , 0))
        
        # To update the position of the Stone 
        # if self.stone_y < SCREEN_HEIGHT and not self.is_collision : self.stone_y += 1
        
        for stone in self.stones.copy():
            stone.update()
            
            # To declare Collision
            if (self.player_x <= stone.x <= self.player_x + 8 and 
                self.player_y <= stone.y <= self.player_y + 8): 
                self.is_collision = True
                
            if stone.y >= SCREEN_HEIGHT:
                self.score += 1
                self.stones.remove(stone)
    
    def update(self):
        # Escape to quit the game
        if pyxel.btnp(pyxel.KEY_ESCAPE): pyxel.quit()
        
        if self.current_scene == START_SCENE : self.update_start_scene()
        elif self.current_scene == PLAY_SCENE: self.update_play_scene()
        
    def draw_start_scene(self):
        pyxel.blt(0 , 0 , 0 , 32 , 0 , 160 , 120)
        pyxel.text(SCREEN_WIDTH // 10 , SCREEN_HEIGHT // 10 , 'Click to Start' , pyxel.COLOR_RED)
    
    def draw_play_scene(self):
        # Background
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        
        # Score
        pyxel.text(10 , 10 , f'Score:{self.score}' , pyxel.COLOR_WHITE)
        
        # Player
        pyxel.blt(self.player_x , self.player_y , 0 , 16 , 0 , 16 , 16 , pyxel.COLOR_BLACK)
        
        # Stone
        # pyxel.blt(self.stone_x , self.stone_y , 0 , 8 , 0 , 8 , 8 , pyxel.COLOR_BLACK)
        for stone in self.stones:
            stone.draw()
                
        if self.is_collision : 
            pyxel.text(SCREEN_WIDTH // 2 - 20 , SCREEN_HEIGHT // 2 , 'Game Over' , pyxel.COLOR_YELLOW)
            pyxel.text(SCREEN_WIDTH // 2 - 20 , SCREEN_HEIGHT // 2 + 10 , f'Score = {self.score}' , pyxel.COLOR_YELLOW)
            
            
    def draw(self):
        if self.current_scene == START_SCENE : self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE : self.draw_play_scene()
        
        
App()
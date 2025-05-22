+      1: import pygame
+      2: import sys
+      3: import random
+      4:
+      5: # Initialize pygame
+      6: pygame.init()
+      7:
+      8: # Game constants
+      9: SCREEN_WIDTH = 400
+     10: SCREEN_HEIGHT = 600
+     11: GRAVITY = 0.25
+     12: BIRD_JUMP = -5
+     13: PIPE_GAP = 150
+     14: PIPE_FREQUENCY = 1500  # milliseconds
+     15: SCROLL_SPEED = 4
+     16:
+     17: # Colors
+     18: WHITE = (255, 255, 255)
+     19: BLACK = (0, 0, 0)
+     20: NEW_RELIC_PURPLE = (142, 59, 198)
+     21: NEW_RELIC_GREEN = (11, 193, 95)
+     22:
+     23: # Create the screen
+     24: screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
+     25: pygame.display.set_caption('New Relic Bird Game')
+     26:
+     27: # Clock for controlling frame rate
+     28: clock = pygame.time.Clock()
+     29:
+     30: # Font for score display
+     31: font = pygame.font.SysFont('Arial', 30)
+     32:
+     33: class Bird:
+     34:     def __init__(self):
+     35:         self.x = 50
+     36:         self.y = int(SCREEN_HEIGHT / 2)
+     37:         self.vel_y = 0
+     38:         self.width = 40
+     39:         self.height = 30
+     40:         self.alive = True
+     41:
+     42:     def update(self):
+     43:         # Apply gravity and update position
+     44:         self.vel_y += GRAVITY
+     45:         self.y += self.vel_y
+     46:
+     47:         # Keep bird on screen
+     48:         if self.y < 0:
+     49:             self.y = 0
+     50:             self.vel_y = 0
+     51:         if self.y + self.height > SCREEN_HEIGHT:
+     52:             self.y = SCREEN_HEIGHT - self.height
+     53:             self.alive = False
+     54:
+     55:     def jump(self):
+     56:         self.vel_y = BIRD_JUMP
+     57:
+     58:     def draw(self):
+     59:         # Draw the bird (a simple rectangle with New Relic purple)
+     60:         pygame.draw.rect(screen, NEW_RELIC_PURPLE, (self.x, self.y, self.width, self.height))
+     61:         # Add an eye
+     62:         pygame.draw.circle(screen, WHITE, (self.x + 30, self.y + 10), 5)
+     63:         pygame.draw.circle(screen, BLACK, (self.x + 30, self.y + 10), 2)
+     64:         # Add a beak
+     65:         pygame.draw.polygon(screen, (255, 165, 0), [(self.x + 40, self.y + 15),
+     66:                                                    (self.x + 50, self.y + 15),
+     67:                                                    (self.x + 40, self.y + 20)])
+     68:
+     69: class Pipe:
+     70:     def __init__(self, x):
+     71:         self.x = x
+     72:         self.height = random.randint(150, 400)
+     73:         self.top_pipe_height = self.height - PIPE_GAP // 2
+     74:         self.bottom_pipe_y = self.height + PIPE_GAP // 2
+     75:         self.passed = False
+     76:         self.pipe_width = 60
+     77:
+     78:     def update(self):
+     79:         self.x -= SCROLL_SPEED
+     80:
+     81:     def draw(self):
+     82:         # Draw top pipe
+     83:         pygame.draw.rect(screen, NEW_RELIC_GREEN,
+     84:                         (self.x, 0, self.pipe_width, self.top_pipe_height))
+     85:         # Draw bottom pipe
+     86:         pygame.draw.rect(screen, NEW_RELIC_GREEN,
+     87:                         (self.x, self.bottom_pipe_y, self.pipe_width,
+     88:                          SCREEN_HEIGHT - self.bottom_pipe_y))
+     89:
+     90:     def check_collision(self, bird):
+     91:         # Create rectangles for collision detection
+     92:         bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
+     93:         top_pipe_rect = pygame.Rect(self.x, 0, self.pipe_width, self.top_pipe_height)
+     94:         bottom_pipe_rect = pygame.Rect(self.x, self.bottom_pipe_y, self.pipe_width,
+     95:                                       SCREEN_HEIGHT - self.bottom_pipe_y)
+     96:
+     97:         # Check for collision
+     98:         if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
+     99:             return True
+    100:         return False
+    101:
+    102: def draw_score(score):
+    103:     score_text = font.render(f'Score: {score}', True, BLACK)
+    104:     screen.blit(score_text, (10, 10))
+    105:
+    106: def draw_game_over(score):
+    107:     # Create semi-transparent overlay
+    108:     overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
+    109:     overlay.set_alpha(128)
+    110:     overlay.fill(BLACK)
+    111:     screen.blit(overlay, (0, 0))
+    112:
+    113:     # Game over text
+    114:     game_over_font = pygame.font.SysFont('Arial', 50)
+    115:     game_over_text = game_over_font.render('GAME OVER', True, WHITE)
+    116:     screen.blit(game_over_text,
+    117:                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
+    118:                 SCREEN_HEIGHT // 3))
+    119:
+    120:     # Score text
+    121:     score_font = pygame.font.SysFont('Arial', 30)
+    122:     score_text = score_font.render(f'Score: {score}', True, WHITE)
+    123:     screen.blit(score_text,
+    124:                (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
+    125:                 SCREEN_HEIGHT // 2))
+    126:
+    127:     # Restart text
+    128:     restart_font = pygame.font.SysFont('Arial', 25)
+    129:     restart_text = restart_font.render('Press SPACE to restart', True, WHITE)
+    130:     screen.blit(restart_text,
+    131:                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
+    132:                 SCREEN_HEIGHT // 2 + 50))
+    133:
+    134: def main():
+    135:     bird = Bird()
+    136:     pipes = []
+    137:     score = 0
+    138:     last_pipe = pygame.time.get_ticks()
+    139:     game_active = True
+    140:
+    141:     # Game loop
+    142:     running = True
+    143:     while running:
+    144:         clock.tick(60)  # 60 FPS
+    145:
+    146:         # Event handling
+    147:         for event in pygame.event.get():
+    148:             if event.type == pygame.QUIT:
+    149:                 running = False
+    150:
+    151:             if event.type == pygame.KEYDOWN:
+    152:                 if event.key == pygame.K_SPACE:
+    153:                     if game_active:
+    154:                         bird.jump()
+    155:                     else:
+    156:                         # Restart game
+    157:                         bird = Bird()
+    158:                         pipes = []
+    159:                         score = 0
+    160:                         last_pipe = pygame.time.get_ticks()
+    161:                         game_active = True
+    162:
+    163:         # Clear screen
+    164:         screen.fill(WHITE)
+    165:
+    166:         if game_active:
+    167:             # Update bird
+    168:             bird.update()
+    169:             bird.draw()
+    170:
+    171:             # Generate pipes
+    172:             time_now = pygame.time.get_ticks()
+    173:             if time_now - last_pipe > PIPE_FREQUENCY:
+    174:                 pipes.append(Pipe(SCREEN_WIDTH))
+    175:                 last_pipe = time_now
+    176:
+    177:             # Update and draw pipes
+    178:             for pipe in pipes:
+    179:                 pipe.update()
+    180:                 pipe.draw()
+    181:
+    182:                 # Check for collision
+    183:                 if pipe.check_collision(bird):
+    184:                     game_active = False
+    185:
+    186:                 # Check if bird passed the pipe
+    187:                 if not pipe.passed and pipe.x + pipe.pipe_width < bird.x:
+    188:                     pipe.passed = True
+    189:                     score += 1
+    190:
+    191:             # Remove pipes that are off screen
+    192:             pipes = [pipe for pipe in pipes if pipe.x > -pipe.pipe_width]
+    193:
+    194:             # Check if bird hit the ground
+    195:             if not bird.alive:
+    196:                 game_active = False
+    197:
+    198:             # Draw score
+    199:             draw_score(score)
+    200:         else:
+    201:             # Draw game over screen
+    202:             draw_game_over(score)
+    203:
+    204:         # Update display
+    205:         pygame.display.update()
+    206:
+    207:     pygame.quit()
+    208:     sys.exit()
+    209:
+    210: if __name__ == "__main__":
+    211:     main()

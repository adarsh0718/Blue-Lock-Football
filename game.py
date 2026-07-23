import pygame
import sys
import math
import random
from entities import Player, Ball
from physics import GoalNetPhysics, handle_ball_pitch_bounds
from ai import FootballAI

# Screen Dimensions
WIDTH = 1000
HEIGHT = 600
FPS = 60

# Vintage Color Palette
PITCH_GREEN_LIGHT = (93, 124, 66)    # Washed-out olive green light strip
PITCH_GREEN_DARK = (84, 112, 60)     # Washed-out olive green dark strip
CHALK_CREAM = (235, 226, 202)        # Muted chalk white for lines
ROPE_CREAM = (215, 205, 185)         # Goalnet cord
TEAM1_BLUE = (35, 75, 140)           # Vintage Royal Blue (Blue Lock)
TEAM2_RED = (178, 34, 34)            # Vintage Red (Anti-Blue Lock)
WHITE = (250, 245, 235)
BLACK = (0, 0, 0)
GOLD_SEPIA = (212, 175, 55)          # Vintage gold
DARK_WOOD = (60, 45, 30)             # Borders
LIGHT_TAN = (244, 230, 200)

# Field margins
MARGIN_X = 50
MARGIN_Y = 30
PITCH_W = WIDTH - 2 * MARGIN_X
PITCH_H = HEIGHT - 2 * MARGIN_Y
GOAL_Y1 = 240
GOAL_Y2 = 360
GOAL_W = 120

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, is_confetti=False, is_splash=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.is_confetti = is_confetti
        self.is_splash = is_splash
        self.angle = random.uniform(0, 360) if is_confetti else 0
        self.spin = random.uniform(-4, 4) if is_confetti else 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.is_confetti:
            self.vy += 0.08 # Gravity
            self.angle += self.spin
        elif self.is_splash:
            self.size += 0.2 # Expand splash ripple
        else:
            # Rain or kick dust decay
            self.vx *= 0.96
            self.vy *= 0.96
        self.lifetime -= 1

    def draw(self, screen):
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        p_surf = pygame.Surface((int(self.size * 2 + 2), int(self.size * 2 + 2)), pygame.SRCALPHA)
        c = (self.color[0], self.color[1], self.color[2], alpha)
        
        if self.is_confetti:
            pygame.draw.rect(p_surf, c, (0, 0, int(self.size), int(self.size * 1.4)))
            rot_surf = pygame.transform.rotate(p_surf, self.angle)
            screen.blit(rot_surf, (self.x - rot_surf.get_width()//2, self.y - rot_surf.get_height()//2))
        elif self.is_splash:
            # Draw concentric circular ripple
            pygame.draw.circle(p_surf, c, (int(self.size), int(self.size)), int(self.size), 1)
            screen.blit(p_surf, (self.x - self.size, self.y - self.size))
        else:
            # Rain droplet line drawing
            if abs(self.vx) > 0 or abs(self.vy) > 0:
                pygame.draw.line(screen, c, (self.x, self.y), (self.x - self.vx * 1.5, self.y - self.vy * 1.5), int(self.size))
            else:
                pygame.draw.circle(p_surf, c, (self.size, self.size), self.size)
                screen.blit(p_surf, (self.x - self.size, self.y - self.size))

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Championship Football 1978: Vintage 5v5")
        self.clock = pygame.time.Clock()
        
        # Vintage fonts (Georgia serif font used for classy retro newspaper style)
        self.font_title = pygame.font.SysFont("Georgia", 52, bold=True)
        self.font_subtitle = pygame.font.SysFont("Georgia", 24, bold=False)
        self.font_subtitle_bold = pygame.font.SysFont("Georgia", 24, bold=True)
        self.font_hud = pygame.font.SysFont("Georgia", 32, bold=True)
        self.font_player = pygame.font.SysFont("Georgia", 13, bold=True)
        self.font_overlay = pygame.font.SysFont("Georgia", 60, bold=True)
        
        self.state = 'MENU'
        
        # Menu selections
        # 0: Game Mode (vs Computer / 2 Player)
        # 1: Weather (Sunny / Evening / Raining / Night)
        # 2: Controls
        # 3: Start Match
        # 4: Exit
        self.menu_selection = 0
        
        # Defaults
        self.mode = 'VS_COMPUTER'
        self.weather = 'SUNNY'
        
        self.score_team1 = 0
        self.score_team2 = 0
        self.match_time = 90 * 60
        self.time_remaining = self.match_time
        
        self.players = []
        self.ball = None
        self.left_net = None
        self.right_net = None
        
        self.p1_controlled_idx = 4 # Default Attacker Team 1
        self.p2_controlled_idx = 9 # Default Attacker Team 2
        
        self.p1_charge = 0.0
        self.p1_charging = False
        self.p2_charge = 0.0
        self.p2_charging = False
        
        self.ai_handler_team1 = FootballAI(1, WIDTH, HEIGHT, GOAL_Y1, GOAL_Y2, MARGIN_X, MARGIN_Y)
        self.ai_handler_team2 = FootballAI(2, WIDTH, HEIGHT, GOAL_Y1, GOAL_Y2, MARGIN_X, MARGIN_Y)
        
        self.particles = []
        self.screen_shake = 0
        self.goal_banner_timer = 0
        self.scoring_team = 0
        
        # --- Pre-calculate Vintage Overlay Filters for performance ---
        
        # 1. CRT Scanlines Layer (Dark faint horizontal bars)
        self.crt_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 3):
            pygame.draw.line(self.crt_overlay, (0, 0, 0, 24), (0, y), (WIDTH, y), 1)
            
        # 2. Evening Sunset Amber Filter
        self.evening_filter = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.evening_filter.fill((215, 110, 30, 34)) # Amber tint overlay
        
        # 3. Night Lighting Dark Overlay and Spotlight Mask
        self.night_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Create a single soft radial spotlight mask
        self.spotlight_mask = pygame.Surface((250, 250), pygame.SRCALPHA)
        for r in range(125, 0, -2):
            # Gradient brightness: clear out opacity subtractively
            alpha = int(((125 - r) / 125.0) ** 1.6 * 210)
            pygame.draw.circle(self.spotlight_mask, (0, 0, 0, alpha), (125, 125), r)

    def reset_positions(self):
        # 5v5 Setup:
        # Team 1 (Crimson Red, moving left-to-right)
        # 0: GK, 1: DEF 1, 2: DEF 2, 3: MID, 4: ATT
        p_gk_1 = Player(85, HEIGHT//2, 1, 'GK', 1, TEAM1_BLUE)
        p_def_1a = Player(240, HEIGHT//2 - 100, 1, 'DEF', 2, TEAM1_BLUE)
        p_def_1b = Player(240, HEIGHT//2 + 100, 1, 'DEF', 3, TEAM1_BLUE)
        p_mid_1 = Player(360, HEIGHT//2, 1, 'MID', 6, TEAM1_BLUE)
        p_att_1 = Player(450, HEIGHT//2, 1, 'ATT', 9, TEAM1_BLUE)
        
        # Team 2 (Royal Blue, moving right-to-left)
        # 5: GK, 6: DEF 1, 7: DEF 2, 8: MID, 9: ATT
        p_gk_2 = Player(WIDTH - 85, HEIGHT//2, 2, 'GK', 13, TEAM2_RED)
        p_def_2a = Player(WIDTH - 240, HEIGHT//2 - 100, 2, 'DEF', 4, TEAM2_RED)
        p_def_2b = Player(WIDTH - 240, HEIGHT//2 + 100, 2, 'DEF', 5, TEAM2_RED)
        p_mid_2 = Player(WIDTH - 360, HEIGHT//2, 2, 'MID', 8, TEAM2_RED)
        p_att_2 = Player(WIDTH - 450, HEIGHT//2, 2, 'ATT', 10, TEAM2_RED)
        
        self.players = [
            p_gk_1, p_def_1a, p_def_1b, p_mid_1, p_att_1,
            p_gk_2, p_def_2a, p_def_2b, p_mid_2, p_att_2
        ]
        
        # Apply weather states to all players
        for p in self.players:
            p.set_weather(self.weather)

        # Reset ball & set weather physics
        self.ball = Ball(WIDTH//2, HEIGHT//2)
        self.ball.set_weather(self.weather)
        
        # Controlled index maps
        self.p1_controlled_idx = 4 # Attacker index
        self.players[4].controlled = True
        
        self.p2_controlled_idx = 9 # Attacker index Team 2
        if self.mode == 'TWO_PLAYER':
            self.players[9].controlled = True
        else:
            self.players[9].controlled = False

        self.p1_charge = 0.0
        self.p1_charging = False
        self.p2_charge = 0.0
        self.p2_charging = False
        
        # Re-rig nets
        self.left_net = GoalNetPhysics(GOAL_Y1, GOAL_Y2, MARGIN_X, MARGIN_X - 24, is_left=True)
        self.right_net = GoalNetPhysics(GOAL_Y1, GOAL_Y2, WIDTH - MARGIN_X, WIDTH - MARGIN_X + 24, is_left=False)
        
        self.particles.clear()

    def start_new_match(self):
        self.score_team1 = 0
        self.score_team2 = 0
        self.time_remaining = self.match_time
        self.reset_positions()
        self.state = 'MATCH'

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.state == 'MENU':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for i in range(5):
                        item_y = 230 + i * 50
                        if item_y - 20 <= my <= item_y + 25:
                            if self.menu_selection == i:
                                if i == 0:
                                    self.mode = 'TWO_PLAYER' if self.mode == 'VS_COMPUTER' else 'VS_COMPUTER'
                                elif i == 1:
                                    weathers = ['SUNNY', 'EVENING', 'RAINING', 'NIGHT']
                                    idx = (weathers.index(self.weather) + 1) % len(weathers)
                                    self.weather = weathers[idx]
                                else:
                                    self.select_menu_option()
                            else:
                                self.menu_selection = i
                                if i in [2, 3, 4]:
                                    self.select_menu_option()
                            break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.menu_selection = (self.menu_selection - 1) % 5
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.menu_selection = (self.menu_selection + 1) % 5
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        # Cycle options
                        if self.menu_selection == 0:
                            self.mode = 'TWO_PLAYER' if self.mode == 'VS_COMPUTER' else 'VS_COMPUTER'
                        elif self.menu_selection == 1:
                            weathers = ['SUNNY', 'EVENING', 'RAINING', 'NIGHT']
                            idx = (weathers.index(self.weather) - 1) % len(weathers)
                            self.weather = weathers[idx]
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.menu_selection == 0:
                            self.mode = 'TWO_PLAYER' if self.mode == 'VS_COMPUTER' else 'VS_COMPUTER'
                        elif self.menu_selection == 1:
                            weathers = ['SUNNY', 'EVENING', 'RAINING', 'NIGHT']
                            idx = (weathers.index(self.weather) + 1) % len(weathers)
                            self.weather = weathers[idx]
                    elif event.key == pygame.K_RETURN:
                        self.select_menu_option()
                        
            elif self.state == 'CONTROLS':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 'MENU'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.state = 'MENU'
                        
            elif self.state == 'MATCH':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'MENU'
                    
                    # P1 Pass / Switch Player
                    if event.key == pygame.K_f:
                        p1_active = self.players[self.p1_controlled_idx]
                        if self.ball.owner == p1_active:
                            self.pass_ball(p1_active, 1)
                        else:
                            self.switch_controlled_player(team_id=1)
                            
                    # P2 Pass / Switch Player
                    if event.key == pygame.K_k and self.mode == 'TWO_PLAYER':
                        p2_active = self.players[self.p2_controlled_idx]
                        if self.ball.owner == p2_active:
                            self.pass_ball(p2_active, 2)
                        else:
                            self.switch_controlled_player(team_id=2)

                    # Shoot charges
                    if event.key == pygame.K_g:
                        p1_active = self.players[self.p1_controlled_idx]
                        if self.ball.owner == p1_active:
                            self.p1_charging = True
                            self.p1_charge = 0.0
                            
                    if event.key == pygame.K_l and self.mode == 'TWO_PLAYER':
                        p2_active = self.players[self.p2_controlled_idx]
                        if self.ball.owner == p2_active:
                            self.p2_charging = True
                            self.p2_charge = 0.0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_g:
                        if self.p1_charging:
                            p1_active = self.players[self.p1_controlled_idx]
                            self.shoot_ball(p1_active, self.p1_charge, 1)
                            self.p1_charging = False
                            self.p1_charge = 0.0
                            
                    if event.key == pygame.K_l and self.mode == 'TWO_PLAYER':
                        if self.p2_charging:
                            p2_active = self.players[self.p2_controlled_idx]
                            self.shoot_ball(p2_active, self.p2_charge, 2)
                            self.p2_charging = False
                            self.p2_charge = 0.0

            elif self.state == 'GAME_OVER':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_new_match()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_new_match()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'MENU'

    def select_menu_option(self):
        if self.menu_selection == 2:
            self.state = 'CONTROLS'
        elif self.menu_selection == 3:
            self.start_new_match()
        elif self.menu_selection == 4:
            pygame.quit()
            sys.exit()

    def switch_controlled_player(self, team_id):
        teammate_indices = [0, 1, 2, 3, 4] if team_id == 1 else [5, 6, 7, 8, 9]
        outfield_indices = [idx for idx in teammate_indices if self.players[idx].role != 'GK']
        
        closest_idx = outfield_indices[0]
        min_dist = 999999.0
        for idx in outfield_indices:
            p = self.players[idx]
            dist = math.hypot(self.ball.x - p.x, self.ball.y - p.y)
            if dist < min_dist:
                min_dist = dist
                closest_idx = idx
                
        if team_id == 1:
            self.players[self.p1_controlled_idx].controlled = False
            self.p1_controlled_idx = closest_idx
            self.players[closest_idx].controlled = True
        else:
            self.players[self.p2_controlled_idx].controlled = False
            self.p2_controlled_idx = closest_idx
            self.players[closest_idx].controlled = True

    def pass_ball(self, player, team_id):
        teammate_indices = [1, 2, 3, 4] if team_id == 1 else [6, 7, 8, 9]
        
        face_dx = math.cos(player.angle)
        face_dy = math.sin(player.angle)
        
        best_teammate = None
        best_score = -999.0
        
        for idx in teammate_indices:
            tm = self.players[idx]
            if tm != player:
                tx = tm.x - player.x
                ty = tm.y - player.y
                dist = math.hypot(tx, ty)
                if dist > 0:
                    tx_norm = tx / dist
                    ty_norm = ty / dist
                    alignment = tx_norm * face_dx + ty_norm * face_dy
                    if alignment > best_score:
                        best_score = alignment
                        best_teammate = tm
                        
        if best_teammate:
            dx = best_teammate.x - player.x
            dy = best_teammate.y - player.y
            dist = math.hypot(dx, dy)
            power = max(5.5, min(9.5, dist * 0.045))
            vx = (dx / dist) * power
            vy = (dy / dist) * power
            
            # 25% chance of slight loft on pass if distance is far
            vz = 2.4 if dist > 190.0 and random.random() < 0.25 else 0.0
            self.ball.kick(vx, vy, vz, player)
            
            self.spawn_kick_particles(player.x + face_dx*11, player.y + face_dy*11, vx, vy)
            
            # Switch controlled focus
            if team_id == 1:
                self.players[self.p1_controlled_idx].controlled = False
                self.p1_controlled_idx = self.players.index(best_teammate)
                best_teammate.controlled = True
            else:
                self.players[self.p2_controlled_idx].controlled = False
                self.p2_controlled_idx = self.players.index(best_teammate)
                best_teammate.controlled = True

    def shoot_ball(self, player, charge, team_id):
        goal_x = WIDTH - MARGIN_X if team_id == 1 else MARGIN_X
        goal_y = (GOAL_Y1 + GOAL_Y2) / 2.0
        
        dx = goal_x - player.x
        dy = goal_y - player.y
        dist = math.hypot(dx, dy)
        
        charge_ratio = min(1.0, charge / 30.0)
        power = 5.8 + charge_ratio * 6.0
        vz = charge_ratio * 4.4 # Loft Z acceleration
        
        if dist > 0:
            vx = (dx / dist) * power
            vy = (dy / dist) * power
            
            dev = (1.0 - charge_ratio) * 0.16
            rad = math.atan2(vy, vx) + random.uniform(-dev, dev)
            vx = math.cos(rad) * power
            vy = math.sin(rad) * power
            
            self.ball.kick(vx, vy, vz, player)
            self.spawn_kick_particles(player.x + math.cos(player.angle)*11, player.y + math.sin(player.angle)*11, vx, vy, count=10)
            self.screen_shake = int(3 + charge_ratio * 5)

    def spawn_kick_particles(self, x, y, vx, vy, count=6):
        # Spawns vintage dust/turf particle sparks
        for _ in range(count):
            pvx = vx * 0.25 + random.uniform(-1.2, 1.2)
            pvy = vy * 0.25 + random.uniform(-1.2, 1.2)
            color = (235, 215, 175) # Beige dust
            self.particles.append(Particle(x, y, pvx, pvy, color, random.uniform(1.8, 3.2), random.randint(12, 24)))

    def spawn_turf_particles(self, player):
        # Heavy grass kick-ups from vintage leather boots
        if random.random() < 0.35:
            px = player.x - math.cos(player.angle) * 8
            py = player.y - math.sin(player.angle) * 8
            pvx = -player.vx * 0.2 + random.uniform(-0.4, 0.4)
            pvy = -player.vy * 0.2 + random.uniform(-0.4, 0.4)
            # Washed out turf green particle colors
            color = (80 + random.randint(-8, 8), 105 + random.randint(-10, 10), 55 + random.randint(-6, 6))
            self.particles.append(Particle(px, py, pvx, pvy, color, random.uniform(1.2, 2.2), random.randint(8, 16)))

    def spawn_goal_confetti(self, goal_x, goal_y):
        # Retro color confetti rain
        for _ in range(100):
            vx = random.uniform(-3.5, 3.5) + (-2.5 if goal_x > WIDTH/2 else 2.5)
            vy = random.uniform(-7, -1.8)
            color = random.choice([TEAM1_BLUE, TEAM2_RED, GOLD_SEPIA, LIGHT_TAN, WHITE])
            self.particles.append(Particle(goal_x, goal_y, vx, vy, color, random.uniform(2.5, 5.0), random.randint(45, 85), is_confetti=True))

    def update(self):
        if self.state in ['MENU', 'CONTROLS']:
            return
            
        if self.state in ['MATCH', 'GOAL_SCB']:
            if self.state == 'MATCH':
                self.time_remaining -= 1
                if self.time_remaining <= 0:
                    self.state = 'GAME_OVER'
                    return
            
            if self.screen_shake > 0:
                self.screen_shake -= 1

            keys = pygame.key.get_pressed()
            
            # --- P1 Input Handling ---
            p1_active = self.players[self.p1_controlled_idx]
            p1_dx, p1_dy = 0, 0
            if keys[pygame.K_w]: p1_dy = -1
            if keys[pygame.K_s]: p1_dy = 1
            if keys[pygame.K_a]: p1_dx = -1
            if keys[pygame.K_d]: p1_dx = 1
            
            p1_sprint = keys[pygame.K_LSHIFT]
            p1_active.move(p1_dx, p1_dy, p1_sprint)
            if p1_active.is_sprinting:
                self.spawn_turf_particles(p1_active)
                
            if self.p1_charging:
                if self.ball.owner != p1_active:
                    self.p1_charging = False
                    self.p1_charge = 0.0
                else:
                    self.p1_charge = min(30.0, self.p1_charge + 1.0)
            
            # --- P2 Input Handling ---
            if self.mode == 'TWO_PLAYER':
                p2_active = self.players[self.p2_controlled_idx]
                p2_dx, p2_dy = 0, 0
                if keys[pygame.K_UP]: p2_dy = -1
                if keys[pygame.K_DOWN]: p2_dy = 1
                if keys[pygame.K_LEFT]: p2_dx = -1
                if keys[pygame.K_RIGHT]: p2_dx = 1
                
                p2_sprint = keys[pygame.K_RSHIFT]
                p2_active.move(p2_dx, p2_dy, p2_sprint)
                if p2_active.is_sprinting:
                    self.spawn_turf_particles(p2_active)
                    
                if self.p2_charging:
                    if self.ball.owner != p2_active:
                        self.p2_charging = False
                        self.p2_charge = 0.0
                    else:
                        self.p2_charge = min(30.0, self.p2_charge + 1.0)
            
            # --- AI Updates for teammates and computer ---
            for i, p in enumerate(self.players):
                teammates = self.players[0:5] if p.team == 1 else self.players[5:10]
                opponents = self.players[5:10] if p.team == 1 else self.players[0:5]
                
                if p.team == 1:
                    if i == self.p1_controlled_idx:
                        pass
                    else:
                        self.ai_handler_team1.update_ai_player(p, self.ball, teammates, opponents)
                else:
                    if self.mode == 'TWO_PLAYER' and i == self.p2_controlled_idx:
                        pass
                    else:
                        self.ai_handler_team2.update_ai_player(p, self.ball, teammates, opponents)
                
                p.update_bounds(WIDTH, HEIGHT, MARGIN_X, MARGIN_Y)
            
            # --- Tackle checks ---
            self.handle_tackling()

            # --- Ball physics ---
            self.ball.update(WIDTH, HEIGHT)
            
            # --- Ball grabbing ---
            self.handle_ball_grab()

            # --- Goalnet Collisions & Bounds ---
            handle_ball_pitch_bounds(self.ball, WIDTH, HEIGHT, MARGIN_X, MARGIN_Y, GOAL_Y1, GOAL_Y2)
            self.left_net.update()
            self.right_net.update()
            self.left_net.check_ball_collision(self.ball, self.ball.radius)
            self.right_net.check_ball_collision(self.ball, self.ball.radius)
            
            # --- Weather Rain Droplet Spawns ---
            if self.weather == 'RAINING':
                # Spawn raindrops
                for _ in range(4):
                    rx = random.randint(0, WIDTH)
                    ry = 0
                    rvx = -1.2 + random.uniform(-0.4, 0.4)
                    rvy = 9.0 + random.uniform(1.0, 3.0)
                    self.particles.append(Particle(rx, ry, rvx, rvy, (130, 150, 175), random.uniform(1.0, 1.8), random.randint(40, 58)))
                
                # Randomly splash raindrops hitting ground
                for p in self.particles:
                    if not p.is_splash and not p.is_confetti:
                        # Drop hits ground plane simulation based on lifetime
                        if p.lifetime == 1:
                            # Trigger splash ripple at end of drop life
                            self.particles.append(Particle(p.x, p.y + p.vy, 0, 0, (140, 160, 185), 1.0, 10, is_splash=True))

            # --- Goal Detection ---
            if self.state == 'MATCH':
                # Goal Team 2 (Left net)
                if self.ball.x < MARGIN_X:
                    if GOAL_Y1 <= self.ball.y <= GOAL_Y2:
                        self.score_goal(scoring_team=2)
                
                # Goal Team 1 (Right net)
                elif self.ball.x > WIDTH - MARGIN_X:
                    if GOAL_Y1 <= self.ball.y <= GOAL_Y2:
                        self.score_goal(scoring_team=1)
            
            # Goal announcement transition timer
            if self.state == 'GOAL_SCB':
                self.goal_banner_timer -= 1
                if self.goal_banner_timer <= 0:
                    self.state = 'MATCH'
                    self.reset_positions()

            # --- Update particles ---
            for p in self.particles[:]:
                p.update()
                if p.lifetime <= 0:
                    self.particles.remove(p)

    def handle_tackling(self):
        ball_owner = self.ball.owner
        if ball_owner is None:
            return
            
        keys = pygame.key.get_pressed()
        
        # Player 1 tackle
        if ball_owner.team == 2:
            p1_active = self.players[self.p1_controlled_idx]
            dist = math.hypot(p1_active.x - ball_owner.x, p1_active.y - ball_owner.y)
            if dist < (p1_active.radius + ball_owner.radius + 7.0):
                is_tackle_pressed = keys[pygame.K_f]
                # Slight slip penalty in rain (tackle success is lower or requires closer range)
                tackle_dist = p1_active.radius + ball_owner.radius + (3.0 if self.weather == 'RAINING' else 6.0)
                if (is_tackle_pressed and dist < tackle_dist) or (random.random() < 0.04 and dist < p1_active.radius + ball_owner.radius + 1.5):
                    self.ball.owner = None
                    self.ball.x = (p1_active.x + ball_owner.x) / 2.0
                    self.ball.y = (p1_active.y + ball_owner.y) / 2.0
                    self.ball.vx = random.uniform(-2, 2)
                    self.ball.vy = random.uniform(-2, 2)
                    self.ball.kick_cooldowns[ball_owner] = 30
                    self.spawn_kick_particles(self.ball.x, self.ball.y, 0, 0, count=4)
                    self.screen_shake = 3

        # Player 2 tackle
        if self.mode == 'TWO_PLAYER' and ball_owner.team == 1:
            p2_active = self.players[self.p2_controlled_idx]
            dist = math.hypot(p2_active.x - ball_owner.x, p2_active.y - ball_owner.y)
            if dist < (p2_active.radius + ball_owner.radius + 7.0):
                is_tackle_pressed = keys[pygame.K_k]
                tackle_dist = p2_active.radius + ball_owner.radius + (3.0 if self.weather == 'RAINING' else 6.0)
                if (is_tackle_pressed and dist < tackle_dist) or (random.random() < 0.04 and dist < p2_active.radius + ball_owner.radius + 1.5):
                    self.ball.owner = None
                    self.ball.x = (p2_active.x + ball_owner.x) / 2.0
                    self.ball.y = (p2_active.y + ball_owner.y) / 2.0
                    self.ball.vx = random.uniform(-2, 2)
                    self.ball.vy = random.uniform(-2, 2)
                    self.ball.kick_cooldowns[ball_owner] = 30
                    self.spawn_kick_particles(self.ball.x, self.ball.y, 0, 0, count=4)
                    self.screen_shake = 3
                    
        # AI tackle checks
        for p in self.players:
            if p != ball_owner and p.team != ball_owner.team and p.role != 'GK':
                dist = math.hypot(p.x - ball_owner.x, p.y - ball_owner.y)
                if dist < (p.radius + ball_owner.radius + 1.5):
                    steal_chance = 0.06 if self.weather == 'RAINING' else 0.08
                    if random.random() < steal_chance:
                        self.ball.owner = None
                        self.ball.kick_cooldowns[ball_owner] = 20
                        self.ball.x = (p.x + ball_owner.x) / 2.0
                        self.ball.y = (p.y + ball_owner.y) / 2.0
                        self.ball.vx = random.uniform(-1, 1)
                        self.ball.vy = random.uniform(-1, 1)
                        break

    def handle_ball_grab(self):
        if self.ball.owner is not None:
            return
            
        if self.ball.z >= 13.0: # Ball too high
            return

        for p in self.players:
            cooldown = self.ball.kick_cooldowns.get(p, 0)
            if cooldown > 0:
                continue
                
            dist = math.hypot(p.x - self.ball.x, p.y - self.ball.y)
            if dist < (p.radius + self.ball.radius + 2.0):
                self.ball.owner = p
                self.ball.vx = 0
                self.ball.vy = 0
                self.ball.vz = 0
                
                # Auto switch controls
                if p.team == 1 and not p.controlled:
                    self.players[self.p1_controlled_idx].controlled = False
                    self.p1_controlled_idx = self.players.index(p)
                    p.controlled = True
                elif p.team == 2 and self.mode == 'TWO_PLAYER' and not p.controlled:
                    self.players[self.p2_controlled_idx].controlled = False
                    self.p2_controlled_idx = self.players.index(p)
                    p.controlled = True
                break

    def score_goal(self, scoring_team):
        self.scoring_team = scoring_team
        if scoring_team == 1:
            self.score_team1 += 1
            goal_x = WIDTH - MARGIN_X
        else:
            self.score_team2 += 1
            goal_x = MARGIN_X
            
        self.state = 'GOAL_SCB'
        self.goal_banner_timer = 150
        self.screen_shake = 16
        self.spawn_goal_confetti(goal_x, HEIGHT//2)

    def draw(self):
        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)

        buffer = pygame.Surface((WIDTH, HEIGHT))
        buffer.fill((84, 112, 60)) # Muted base vintage green

        if self.state == 'MENU':
            self.draw_menu(buffer)
        elif self.state == 'CONTROLS':
            self.draw_controls(buffer)
        elif self.state in ['MATCH', 'GOAL_SCB', 'GAME_OVER']:
            self.draw_pitch(buffer)
            
            # Layer 1: Shadows (under players)
            for p in self.players:
                p.draw_shadow(buffer)
            if self.ball:
                self.ball.draw_shadow(buffer)
                
            self.draw_nets(buffer)
            
            # Layer 2: Player bodies
            for p in self.players:
                p.draw(buffer, self.font_player)
                
            # Layer 3: Shoot charge gauges
            if self.state == 'MATCH':
                if self.p1_charging:
                    p = self.players[self.p1_controlled_idx]
                    self.draw_charge_bar(buffer, p, self.p1_charge)
                if self.mode == 'TWO_PLAYER' and self.p2_charging:
                    p = self.players[self.p2_controlled_idx]
                    self.draw_charge_bar(buffer, p, self.p2_charge)

            # Layer 4: Ball
            if self.ball:
                self.ball.draw(buffer)
                
            # Layer 5: Particles
            for p in self.particles:
                p.draw(buffer)

            # Layer 6: Dynamic Weather Lighting overlays
            if self.weather == 'EVENING':
                buffer.blit(self.evening_filter, (0, 0))
            elif self.weather == 'NIGHT':
                self.draw_night_spotlights(buffer)

            # Layer 7: HUD
            self.draw_hud(buffer)
            
            # Layer 8: Match state overlays
            if self.state == 'GOAL_SCB':
                self.draw_goal_banner(buffer)
            elif self.state == 'GAME_OVER':
                self.draw_game_over(buffer)

        # Apply CRT Scanline Overlay
        buffer.blit(self.crt_overlay, (0, 0))

        # Output to screen with shake offsets
        self.screen.blit(buffer, (shake_x, shake_y))
        pygame.display.flip()

    def draw_night_spotlights(self, surf):
        # 1. Fill night overlay with deep dark blue
        self.night_overlay.fill((14, 14, 28, 205))
        
        # 2. Subtract light centers around the ball and players
        # The subtractive blending removes the opacity from the dark blue layer
        if self.ball:
            # Spotlight follows the ground X,Y (ball shadow location)
            self.night_overlay.blit(self.spotlight_mask, (self.ball.x - 125, self.ball.y - 125), special_flags=pygame.BLEND_RGBA_SUB)
            
        for p in self.players:
            self.night_overlay.blit(self.spotlight_mask, (p.x - 125, p.y - 125), special_flags=pygame.BLEND_RGBA_SUB)
            
        # 3. Blit the night mask over the screen
        surf.blit(self.night_overlay, (0, 0))

    def draw_charge_bar(self, surf, player, charge):
        px, py = int(player.x), int(player.y)
        bar_w = 24
        bar_h = 4
        bx = px - bar_w // 2
        by = py - int(player.radius) - 18
        
        pygame.draw.rect(surf, (70, 50, 30), (bx - 1, by - 1, bar_w + 2, bar_h + 2))
        pygame.draw.rect(surf, (100, 95, 90), (bx, by, bar_w, bar_h))
        fill_w = int(bar_w * (charge / 30.0))
        color = GOLD_SEPIA if (pygame.time.get_ticks() // 50) % 2 == 0 else (200, 110, 50)
        pygame.draw.rect(surf, color, (bx, by, fill_w, bar_h))

    def draw_pitch(self, surf):
        # Draw vintage grass lawn stripes
        num_stripes = 16
        stripe_w = WIDTH // num_stripes
        for i in range(num_stripes):
            col = PITCH_GREEN_LIGHT if i % 2 == 0 else PITCH_GREEN_DARK
            pygame.draw.rect(surf, col, (i * stripe_w, 0, stripe_w, HEIGHT))
            
        # Pitch margins
        pygame.draw.rect(surf, CHALK_CREAM, (MARGIN_X, MARGIN_Y, PITCH_W, PITCH_H), 2)
        pygame.draw.line(surf, CHALK_CREAM, (WIDTH//2, MARGIN_Y), (WIDTH//2, HEIGHT - MARGIN_Y), 2)
        
        # Center Circle
        pygame.draw.circle(surf, CHALK_CREAM, (WIDTH//2, HEIGHT//2), 65, 2)
        pygame.draw.circle(surf, CHALK_CREAM, (WIDTH//2, HEIGHT//2), 3)
        
        # Left penalty area
        pygame.draw.rect(surf, CHALK_CREAM, (MARGIN_X, HEIGHT//2 - 125, 100, 250), 2)
        pygame.draw.circle(surf, CHALK_CREAM, (MARGIN_X + 100, HEIGHT//2), 3)
        pygame.draw.rect(surf, CHALK_CREAM, (MARGIN_X, GOAL_Y1, 35, GOAL_W), 2)

        # Right penalty area
        pygame.draw.rect(surf, CHALK_CREAM, (WIDTH - MARGIN_X - 100, HEIGHT//2 - 125, 100, 250), 2)
        pygame.draw.circle(surf, CHALK_CREAM, (WIDTH - MARGIN_X - 100, HEIGHT//2), 3)
        pygame.draw.rect(surf, CHALK_CREAM, (WIDTH - MARGIN_X - 35, GOAL_Y1, 35, GOAL_W), 2)

        # Draw wooden vintage posts (classic brown circles)
        post_color = (110, 85, 60)
        pygame.draw.circle(surf, post_color, (MARGIN_X, GOAL_Y1), 5)
        pygame.draw.circle(surf, post_color, (MARGIN_X, GOAL_Y2), 5)
        pygame.draw.circle(surf, post_color, (WIDTH - MARGIN_X, GOAL_Y1), 5)
        pygame.draw.circle(surf, post_color, (WIDTH - MARGIN_X, GOAL_Y2), 5)

    def draw_nets(self, surf):
        # Draw cord nets
        self.left_net.draw(surf, ROPE_CREAM)
        self.right_net.draw(surf, ROPE_CREAM)

    def draw_hud(self, surf):
        # Score banner backing (Wood border box)
        hud_bg = pygame.Surface((360, 52), pygame.SRCALPHA)
        pygame.draw.rect(hud_bg, (40, 30, 20, 220), (0, 0, 360, 52), border_radius=6)
        pygame.draw.rect(hud_bg, GOLD_SEPIA, (0, 0, 360, 52), 1, border_radius=6)
        surf.blit(hud_bg, (WIDTH//2 - 180, 8))
        
        # Scores (Cream vintage fonts)
        t1_score = self.font_hud.render(f"{self.score_team1:02d}", True, TEAM1_BLUE)
        surf.blit(t1_score, (WIDTH//2 - 150, 14))
        
        divider = self.font_hud.render("-", True, CHALK_CREAM)
        surf.blit(divider, (WIDTH//2 - 6, 14))
        
        t2_score = self.font_hud.render(f"{self.score_team2:02d}", True, TEAM2_RED)
        surf.blit(t2_score, (WIDTH//2 + 105, 14))
        
        # Timer
        mins = (self.time_remaining // 60) // 60
        secs = (self.time_remaining // 60) % 60
        time_text = self.font_hud.render(f"{mins:02d}:{secs:02d}", True, LIGHT_TAN)
        surf.blit(time_text, (WIDTH//2 - 45, 14))

        # Bottom Hints Bar
        hint_surf = pygame.Surface((650, 26), pygame.SRCALPHA)
        pygame.draw.rect(hint_surf, (30, 22, 15, 180), (0, 0, 650, 26), border_radius=4)
        pygame.draw.rect(hint_surf, DARK_WOOD, (0, 0, 650, 26), 1, border_radius=4)
        surf.blit(hint_surf, (WIDTH//2 - 325, HEIGHT - 28))
        
        hint_str = "P1: WASD (Move) | F (Pass/Switch) | G (Shoot/Loft) "
        if self.mode == 'TWO_PLAYER':
            hint_str += "| P2: Arrows (Move) | K (Pass/Switch) | L (Shoot/Loft)"
        else:
            hint_str += "| Team Blue Lock (Player) vs Anti-Blue Lock (Computer) 5v5"
            
        hint_text = self.font_player.render(hint_str, True, LIGHT_TAN)
        surf.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT - 22))

    def draw_menu(self, surf):
        # Draw wood-like bordered panels
        surf.fill((50, 38, 25))
        
        # Inner canvas
        pygame.draw.rect(surf, (84, 112, 60), (30, 30, WIDTH - 60, HEIGHT - 60))
        pygame.draw.rect(surf, GOLD_SEPIA, (26, 26, WIDTH - 52, HEIGHT - 52), 3)
        pygame.draw.rect(surf, CHALK_CREAM, (40, 40, WIDTH - 80, HEIGHT - 80), 1)

        # Title
        t_glow = self.font_title.render("CHAMPIONSHIP FOOTBALL", True, DARK_WOOD)
        t_main = self.font_title.render("CHAMPIONSHIP FOOTBALL", True, CHALK_CREAM)
        surf.blit(t_glow, (WIDTH//2 - t_glow.get_width()//2 + 3, 93))
        surf.blit(t_main, (WIDTH//2 - t_main.get_width()//2, 90))
        
        sub = self.font_subtitle.render("1978 Vintage Retro Edition - 5v5 Simulator", True, GOLD_SEPIA)
        surf.blit(sub, (WIDTH//2 - sub.get_width()//2, 150))
        
        # Menu Options array
        m_mode = f"GAME MODE:  {self.mode.replace('_', ' ')}"
        m_weath = f"ATMOSPHERE:  {self.weather}"
        
        options = [
            m_mode,
            m_weath,
            "CONTROLS LAYOUT GUIDE",
            "START CHAMPIONSHIP MATCH",
            "EXIT TO DESKTOP"
        ]
        
        for i, opt in enumerate(options):
            is_sel = (i == self.menu_selection)
            
            if is_sel:
                box_w = 480
                box_h = 36
                box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                pygame.draw.rect(box_surf, (244, 230, 200, 60), (0, 0, box_w, box_h), border_radius=4)
                pygame.draw.rect(box_surf, GOLD_SEPIA, (0, 0, box_w, box_h), 1, border_radius=4)
                surf.blit(box_surf, (WIDTH//2 - box_w//2, 230 + i * 50))
                
            color = WHITE if is_sel else (185, 175, 150)
            text_str = f">>  {opt}  <<" if is_sel else opt
            
            opt_text = self.font_subtitle_bold.render(text_str, True, color) if is_sel else self.font_subtitle.render(text_str, True, color)
            surf.blit(opt_text, (WIDTH//2 - opt_text.get_width()//2, 235 + i * 50))
            
        # Footnote
        foot = self.font_player.render("Use UP/DOWN to navigate | LEFT/RIGHT to change settings | ENTER to select", True, LIGHT_TAN)
        surf.blit(foot, (WIDTH//2 - foot.get_width()//2, HEIGHT - 55))

    def draw_controls(self, surf):
        surf.fill((50, 38, 25))
        pygame.draw.rect(surf, (40, 52, 35), (30, 30, WIDTH - 60, HEIGHT - 60))
        pygame.draw.rect(surf, GOLD_SEPIA, (26, 26, WIDTH - 52, HEIGHT - 52), 3)
        
        title = self.font_title.render("GAMEPLAY INSTRUCTIONS", True, GOLD_SEPIA)
        surf.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        
        col_w = 410
        box_y = 150
        box_h = 300
        
        # P1 controls box
        p1_box = pygame.Surface((col_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(p1_box, (35, 75, 140, 25), (0, 0, col_w, box_h), border_radius=6)
        pygame.draw.rect(p1_box, TEAM1_BLUE, (0, 0, col_w, box_h), 1, border_radius=6)
        surf.blit(p1_box, (75, box_y))
        
        p1_h = self.font_subtitle_bold.render("PLAYER 1 (BLUE LOCK)", True, TEAM1_BLUE)
        surf.blit(p1_h, (100, box_y + 15))
        
        p1_ctrls = [
            "Movement:  W / A / S / D keys",
            "Sprint:    LEFT SHIFT (uses stamina)",
            "Pass/Tackle:  F key",
            "Switch Active: F key (without ball)",
            "Shoot/Loft:   G key (hold to charge height)",
        ]
        for idx, line in enumerate(p1_ctrls):
            t = self.font_subtitle.render(line, True, WHITE)
            surf.blit(t, (90, box_y + 70 + idx * 40))

        # P2 controls box
        p2_box = pygame.Surface((col_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(p2_box, (178, 34, 34, 25), (0, 0, col_w, box_h), border_radius=6)
        pygame.draw.rect(p2_box, TEAM2_RED, (0, 0, col_w, box_h), 1, border_radius=6)
        surf.blit(p2_box, (WIDTH - col_w - 75, box_y))
        
        p2_h = self.font_subtitle_bold.render("PLAYER 2 (ANTI-BLUE LOCK)", True, TEAM2_RED)
        surf.blit(p2_h, (WIDTH - col_w - 50, box_y + 15))
        
        p2_ctrls = [
            "Movement:  Arrow keys",
            "Sprint:    RIGHT SHIFT (uses stamina)",
            "Pass/Tackle:  K key",
            "Switch Active: K key (without ball)",
            "Shoot/Loft:   L key (hold to charge height)",
        ]
        for idx, line in enumerate(p2_ctrls):
            t = self.font_subtitle.render(line, True, WHITE)
            surf.blit(t, (WIDTH - col_w - 60, box_y + 70 + idx * 40))
            
        prompt = self.font_subtitle.render("Press ESCAPE or ENTER to return to main menu", True, LIGHT_TAN)
        surf.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT - 80))

    def draw_goal_banner(self, surf):
        overlay = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
        overlay.fill((40, 30, 20, 225))
        surf.blit(overlay, (0, HEIGHT//2 - 70))
        
        color = TEAM1_BLUE if self.scoring_team == 1 else TEAM2_RED
        pygame.draw.line(surf, color, (0, HEIGHT//2 - 70), (WIDTH, HEIGHT//2 - 70), 3)
        pygame.draw.line(surf, color, (0, HEIGHT//2 + 70), (WIDTH, HEIGHT//2 + 70), 3)
        pygame.draw.line(surf, GOLD_SEPIA, (0, HEIGHT//2 - 66), (WIDTH, HEIGHT//2 - 66), 1)
        pygame.draw.line(surf, GOLD_SEPIA, (0, HEIGHT//2 + 66), (WIDTH, HEIGHT//2 + 66), 1)
        
        team_str = "BLUE LOCK" if self.scoring_team == 1 else "ANTI-BLUE LOCK"
        goal_text = self.font_overlay.render("GOAL!!!", True, GOLD_SEPIA)
        team_text = self.font_subtitle_bold.render(f"{team_str} CONVERTS THE SCORE!", True, WHITE)
        
        surf.blit(goal_text, (WIDTH//2 - goal_text.get_width()//2, HEIGHT//2 - 55))
        surf.blit(team_text, (WIDTH//2 - team_text.get_width()//2, HEIGHT//2 + 20))

    def draw_game_over(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 22, 15, 235))
        surf.blit(overlay, (0, 0))
        
        if self.score_team1 > self.score_team2:
            win_str = "BLUE LOCK WINS THE MATCH!"
            color = TEAM1_BLUE
        elif self.score_team2 > self.score_team1:
            win_str = "ANTI-BLUE LOCK WINS THE MATCH!"
            color = TEAM2_RED
        else:
            win_str = "MATCH ENDED IN A DRAW!"
            color = GOLD_SEPIA
            
        win_text = self.font_overlay.render(win_str, True, color)
        surf.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 110))
        
        score_text = self.font_subtitle_bold.render(f"Final score:  {self.score_team1} - {self.score_team2}", True, WHITE)
        surf.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        
        restart = self.font_subtitle_bold.render("Press ENTER to play again", True, GOLD_SEPIA)
        exit_p = self.font_subtitle.render("Press ESCAPE for Main Menu", True, LIGHT_TAN)
        
        surf.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 60))
        surf.blit(exit_p, (WIDTH//2 - exit_p.get_width()//2, HEIGHT//2 + 110))

if __name__ == '__main__':
    game = GameEngine()
    game.run()

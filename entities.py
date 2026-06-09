import pygame
import math
from collections import deque

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0.0
        
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        
        self.radius = 8.0
        self.friction = 0.982
        self.air_resistance = 0.990
        self.gravity = 0.26
        
        self.owner = None
        self.kick_cooldowns = {}
        
        # Trail (much subtler and dust-like for vintage style)
        self.trail = deque(maxlen=8)
        
        self.angle = 0.0
        self.spin_speed = 0.0
        self.weather = 'SUNNY'

    def set_weather(self, weather):
        self.weather = weather
        if weather == 'RAINING':
            self.friction = 0.994 # Wet grass: skids and slides much further!
            self.air_resistance = 0.992
        else:
            self.friction = 0.982
            self.air_resistance = 0.990

    def kick(self, vx, vy, vz, kicker):
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.owner = None
        self.kick_cooldowns[kicker] = 25
        self.spin_speed = math.hypot(vx, vy) * 1.2

    def update(self, pitch_width, pitch_height):
        for p in list(self.kick_cooldowns.keys()):
            if self.kick_cooldowns[p] > 0:
                self.kick_cooldowns[p] -= 1
            else:
                del self.kick_cooldowns[p]

        if self.owner:
            dribble_dist = 11.0
            angle = self.owner.angle
            self.x = self.owner.x + math.cos(angle) * dribble_dist
            self.y = self.owner.y + math.sin(angle) * dribble_dist
            self.z = 0.0
            self.vx = self.owner.vx
            self.vy = self.owner.vy
            self.vz = 0.0
            self.trail.clear()
            self.angle += math.hypot(self.vx, self.vy) * 0.3
        else:
            self.x += self.vx
            self.y += self.vy
            self.z += self.vz
            
            if self.z > 0:
                self.vx *= self.air_resistance
                self.vy *= self.air_resistance
                self.vz -= self.gravity
                self.spin_speed *= 0.99
            else:
                self.z = 0.0
                self.vz = 0.0
                self.vx *= self.friction
                self.vy *= self.friction
                self.spin_speed *= 0.93
                
                # Check bounce
                if abs(self.vz) > 0.4:
                    self.vz = -self.vz * 0.42
                
            self.angle += self.spin_speed
            
            # Subtler vintage dust trail
            if math.hypot(self.vx, self.vy) > 3.0:
                self.trail.append((self.x, self.y, self.z))
            else:
                if len(self.trail) > 0:
                    self.trail.popleft()

    def draw_shadow(self, screen):
        # Draw dynamic shadows depending on weather mode
        shadow_r = max(3.0, self.radius - self.z * 0.08)
        
        if self.weather == 'SUNNY':
            # Crisp, dark, direct shadow
            s_surf = pygame.Surface((int(shadow_r*2), int(shadow_r*2)), pygame.SRCALPHA)
            pygame.draw.circle(s_surf, (0, 0, 0, 110), (shadow_r, shadow_r), shadow_r)
            screen.blit(s_surf, (self.x - shadow_r, self.y - shadow_r / 2 + 3))
            
        elif self.weather == 'EVENING':
            # Long, stretched, orange-tinted dark shadow towards bottom-right
            stretch_w = int(shadow_r * 2.5)
            stretch_h = int(shadow_r * 1.5)
            s_surf = pygame.Surface((stretch_w, stretch_h), pygame.SRCALPHA)
            # Draw ellipse shadow
            pygame.draw.ellipse(s_surf, (5, 3, 0, 85), (0, 0, stretch_w, stretch_h))
            # Offset based on height z
            ox = 12.0 + self.z * 0.4
            oy = 6.0 + self.z * 0.2
            screen.blit(s_surf, (self.x - shadow_r + ox, self.y - shadow_r/2 + oy))
            
        elif self.weather == 'RAINING':
            # Faint, highly dispersed shadow due to overcast clouds
            s_surf = pygame.Surface((int(shadow_r*2), int(shadow_r*2)), pygame.SRCALPHA)
            pygame.draw.circle(s_surf, (0, 0, 0, 45), (shadow_r, shadow_r), shadow_r)
            screen.blit(s_surf, (self.x - shadow_r, self.y - shadow_r / 2 + 1))
            
        elif self.weather == 'NIGHT':
            # Quad-shadow from 4 stadium floodlights
            # Faint shadows pointing in 4 diagonal directions away from the ball
            opacity = max(10, int(45 - self.z * 0.5))
            offsets = [(-8, -5), (8, -5), (-8, 5), (8, 5)]
            for dx, dy in offsets:
                # Shadows stretch outwards based on ball height
                sox = dx * (1.0 + self.z * 0.08)
                soy = dy * (1.0 + self.z * 0.08)
                s_surf = pygame.Surface((int(shadow_r*2), int(shadow_r*2)), pygame.SRCALPHA)
                pygame.draw.circle(s_surf, (0, 0, 0, opacity), (shadow_r, shadow_r), shadow_r)
                screen.blit(s_surf, (self.x - shadow_r + sox, self.y - shadow_r / 2 + soy))

    def draw(self, screen):
        # Draw vintage trail
        for i, (tx, ty, tz) in enumerate(self.trail):
            alpha = int(140 * (i / len(self.trail)) * 0.25)
            trail_r = self.radius + tz * 0.06
            trail_surf = pygame.Surface((int(trail_r * 2), int(trail_r * 2)), pygame.SRCALPHA)
            # Warm beige dust trail
            pygame.draw.circle(trail_surf, (220, 205, 180, alpha), (trail_r, trail_r), trail_r)
            screen.blit(trail_surf, (tx - trail_r, ty - tz - trail_r))

        bx = int(self.x)
        by = int(self.y - self.z)
        render_r = self.radius + self.z * 0.08
        
        # Classic 1970s Leather Football style (Brown/Tanned Hexagonal panels)
        # Base leather color: Vintage Tan (196, 148, 100)
        pygame.draw.circle(screen, (139, 90, 43), (bx, by), int(render_r))
        pygame.draw.circle(screen, (196, 148, 100), (bx, by), int(render_r - 1.5))
        
        # Draw classic curved leather seams instead of neon lines
        for offset_angle in [0, 90, 180, 270]:
            rad = math.radians(self.angle + offset_angle)
            rad_inner = math.radians(self.angle + offset_angle + 45)
            
            # Outer stitch anchors
            lx1 = bx + math.cos(rad) * (render_r - 2)
            ly1 = by + math.sin(rad) * (render_r - 2)
            
            # Curved inner seam lines (Laced football look)
            lx2 = bx + math.cos(rad_inner) * (render_r * 0.3)
            ly2 = by + math.sin(rad_inner) * (render_r * 0.3)
            
            pygame.draw.line(screen, (80, 50, 20), (lx2, ly2), (lx1, ly1), 1)

class Player:
    def __init__(self, x, y, team, role, number, team_color):
        self.x = x
        self.y = y
        self.team = team # 1 (Red) or 2 (Blue)
        self.role = role # 'GK', 'DEF', 'MID', 'ATT'
        self.number = number
        self.team_color = team_color # Vintage Crimson or Royal Blue
        
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.0
        
        self.radius = 13.5
        self.accel = 0.34
        self.decel = 0.84
        self.max_speed = 3.4
        self.sprint_speed = 4.8
        
        self.stamina = 100.0
        self.is_sprinting = False
        self.controlled = False
        
        # AI target coordinates
        self.target_x = x
        self.target_y = y
        
        self.trail = deque(maxlen=6)
        self.weather = 'SUNNY'

    def set_weather(self, weather):
        self.weather = weather
        if weather == 'RAINING':
            # Wet mud slows down acceleration and increases slip (slower deceleration)
            self.decel = 0.91 # Slippery slide!
            self.accel = 0.26 # Harder to get grip
            self.max_speed = 3.0
            self.sprint_speed = 4.1
        else:
            self.decel = 0.84
            self.accel = 0.34
            self.max_speed = 3.4
            self.sprint_speed = 4.8

    def move(self, dx, dy, sprint_requested):
        current_max = self.max_speed
        self.is_sprinting = False
        
        if sprint_requested and self.stamina > 10.0 and (dx != 0 or dy != 0):
            current_max = self.sprint_speed
            self.stamina = max(0.0, self.stamina - 0.45)
            self.is_sprinting = True
        else:
            self.stamina = min(100.0, self.stamina + 0.16)

        length = math.hypot(dx, dy)
        if length > 0:
            dx_norm = dx / length
            dy_norm = dy / length
            
            self.vx += dx_norm * self.accel
            self.vy += dy_norm * self.accel
            self.angle = math.atan2(dy_norm, dx_norm)
        else:
            self.vx *= self.decel
            self.vy *= self.decel

        speed = math.hypot(self.vx, self.vy)
        if speed > current_max:
            self.vx = (self.vx / speed) * current_max
            self.vy = (self.vy / speed) * current_max

        self.x += self.vx
        self.y += self.vy
        
        # Vintage motion ghosting
        if self.is_sprinting and speed > 2.8:
            self.trail.append((self.x, self.y))
        else:
            if len(self.trail) > 0:
                self.trail.popleft()

    def update_bounds(self, width, height, margin_x=50, margin_y=30):
        left_limit = margin_x
        right_limit = width - margin_x
        top_limit = margin_y
        bottom_limit = height - margin_y
        
        if self.x - self.radius < left_limit:
            self.x = left_limit + self.radius
            self.vx = 0
        elif self.x + self.radius > right_limit:
            self.x = right_limit - self.radius
            self.vx = 0
            
        if self.y - self.radius < top_limit:
            self.y = top_limit + self.radius
            self.vy = 0
        elif self.y + self.radius > bottom_limit:
            self.y = bottom_limit - self.radius
            self.vy = 0

    def draw_shadow(self, screen):
        # Draw player shadows based on weather mode
        if self.weather == 'SUNNY':
            s_surf = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(s_surf, (0, 0, 0, 95), (self.radius, self.radius), self.radius)
            screen.blit(s_surf, (self.x - self.radius, self.y - self.radius / 2 + 5))
            
        elif self.weather == 'EVENING':
            stretch_w = int(self.radius * 2.4)
            stretch_h = int(self.radius * 1.3)
            s_surf = pygame.Surface((stretch_w, stretch_h), pygame.SRCALPHA)
            pygame.draw.ellipse(s_surf, (5, 3, 0, 75), (0, 0, stretch_w, stretch_h))
            screen.blit(s_surf, (self.x - self.radius + 14, self.y - self.radius/2 + 8))
            
        elif self.weather == 'RAINING':
            s_surf = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(s_surf, (0, 0, 0, 40), (self.radius, self.radius), self.radius)
            screen.blit(s_surf, (self.x - self.radius, self.y - self.radius / 2 + 2))
            
        elif self.weather == 'NIGHT':
            # Quad shadow for player (floodlights)
            opacity = 35
            offsets = [(-6, -4), (6, -4), (-6, 4), (6, 4)]
            for dx, dy in offsets:
                s_surf = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
                pygame.draw.circle(s_surf, (0, 0, 0, opacity), (self.radius, self.radius), self.radius)
                screen.blit(s_surf, (self.x - self.radius + dx, self.y - self.radius/2 + dy))

    def draw(self, screen, font):
        # Sprint ghost trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(100 * (i / len(self.trail)) * 0.3)
            trail_surf = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (self.team_color[0], self.team_color[1], self.team_color[2], alpha), (self.radius, self.radius), self.radius)
            screen.blit(trail_surf, (tx - self.radius, ty - self.radius))

        px, py = int(self.x), int(self.y)
        
        # Vintage jersey styling: Solid jersey color with classic dark wood/leather borders
        pygame.draw.circle(screen, (60, 40, 25), (px, py), int(self.radius)) # Leather border
        pygame.draw.circle(screen, self.team_color, (px, py), int(self.radius - 1.5)) # Jersey body
        
        # Classic White collar/V-neck detail
        rad_facing = self.angle
        v_left = rad_facing + math.radians(135)
        v_right = rad_facing - math.radians(135)
        cx1 = px + math.cos(v_left) * (self.radius - 3)
        cy1 = py + math.sin(v_left) * (self.radius - 3)
        cx2 = px + math.cos(v_right) * (self.radius - 3)
        cy2 = py + math.sin(v_right) * (self.radius - 3)
        pygame.draw.line(screen, (245, 240, 230), (cx1, cy1), (px, py), 1)
        pygame.draw.line(screen, (245, 240, 230), (cx2, cy2), (px, py), 1)
        
        # Facing line (nose)
        nose_x = px + math.cos(self.angle) * (self.radius - 2.5)
        nose_y = py + math.sin(self.angle) * (self.radius - 2.5)
        pygame.draw.line(screen, (245, 240, 230), (px, py), (nose_x, nose_y), 2)

        # Vintage Jersey number
        num_color = (255, 255, 255) if self.team == 1 else (240, 210, 110)
        num_text = font.render(str(self.number), True, num_color)
        num_rect = num_text.get_rect(center=(px, py + 1.5)) # Offset down slightly for typography
        screen.blit(num_text, num_rect)
        
        # Stamina indicator (vintage styled: brown border, gold/amber bar)
        if self.stamina < 95.0:
            bar_w = 18
            bar_h = 3
            bx = px - bar_w // 2
            by = py + int(self.radius) + 4
            pygame.draw.rect(screen, (70, 50, 35), (bx - 1, by - 1, bar_w + 2, bar_h + 2))
            pygame.draw.rect(screen, (90, 80, 70), (bx, by, bar_w, bar_h))
            
            color = (130, 200, 100) # Muted green
            if self.stamina < 30:
                color = (190, 80, 70) # Muted red
            elif self.stamina < 70:
                color = (210, 180, 80) # Muted gold
                
            fill_w = int(bar_w * (self.stamina / 100.0))
            pygame.draw.rect(screen, color, (bx, by, fill_w, bar_h))

        # Active player indicator (vintage pointing triangle)
        if self.controlled:
            t_y = py - int(self.radius) - 8
            # Floating hover offset using ticks
            bounce = math.sin(pygame.time.get_ticks() * 0.01) * 3
            t_y += bounce
            t_points = [
                (px - 5, t_y - 6),
                (px + 5, t_y - 6),
                (px, t_y)
            ]
            pygame.draw.polygon(screen, (245, 240, 230), t_points)
            pygame.draw.polygon(screen, (60, 40, 25), t_points, 1)

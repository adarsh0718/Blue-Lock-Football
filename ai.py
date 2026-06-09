import math
import random

class FootballAI:
    def __init__(self, team_id, pitch_width, pitch_height, goal_y1, goal_y2, margin_x, margin_y):
        self.team_id = team_id # 1 (Left to Right) or 2 (Right to Left)
        self.width = pitch_width
        self.height = pitch_height
        self.goal_y1 = goal_y1
        self.goal_y2 = goal_y2
        self.margin_x = margin_x
        self.margin_y = margin_y
        
        if team_id == 1:
            self.opp_goal_x = pitch_width - margin_x
            self.own_goal_x = margin_x
        else:
            self.opp_goal_x = margin_x
            self.own_goal_x = pitch_width - margin_x
            
        self.opp_goal_center_y = (goal_y1 + goal_y2) / 2.0

    def update_ai_player(self, player, ball, teammates, opponents):
        if player.role == 'GK':
            self.update_goalkeeper(player, ball, teammates)
            return

        # Outfield player coordination
        ball_owner = ball.owner
        
        # 1. If this player is holding the ball
        if ball_owner == player:
            self.handle_offense_ball_carrier(player, ball, teammates, opponents)
        elif ball_owner in teammates:
            # A teammate has the ball
            self.handle_offense_support(player, ball, teammates)
        else:
            # Opponent has the ball, or it is loose
            self.handle_defense_or_loose(player, ball, teammates, opponents)

    def update_goalkeeper(self, gk, ball, teammates):
        target_x = self.own_goal_x
        
        # Offset slightly in front of goal
        if self.team_id == 1:
            target_x += 18.0
        else:
            target_x -= 18.0
            
        # Track ball Y, clamped to goal mouth area
        target_y = max(self.goal_y1 - 4, min(self.goal_y2 + 4, ball.y))
        
        # Rush out to collect ball if ball is close and free
        dist_to_ball = math.hypot(ball.x - gk.x, ball.y - gk.y)
        if dist_to_ball < 70.0 and ball.z < 18.0 and (ball.owner is None or ball.owner.team != self.team_id):
            target_x = ball.x
            target_y = ball.y
            
        # If goalie catches ball
        if ball.owner == gk:
            # Find a teammate to pass to (prefer midfielders or defenders further up)
            best_target = None
            max_dist = -1.0
            for tm in teammates:
                if tm != gk:
                    dist = abs(tm.x - self.own_goal_x)
                    if dist > max_dist:
                        max_dist = dist
                        best_target = tm
            
            if best_target:
                dx = best_target.x - gk.x
                dy = best_target.y - gk.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    vx = (dx / dist) * 7.2
                    vy = (dy / dist) * 7.2
                    ball.kick(vx, vy, 1.4, gk)
            else:
                kx = 7.5 if self.team_id == 1 else -7.5
                ball.kick(kx, random.uniform(-1.5, 1.5), 1.8, gk)
            return

        # Goalkeeper movements are conservative (no sprinting)
        dx = target_x - gk.x
        dy = target_y - gk.y
        gk.move(dx, dy, sprint_requested=False)

    def handle_offense_ball_carrier(self, player, ball, teammates, opponents):
        goal_dx = self.opp_goal_x - player.x
        goal_dy = self.opp_goal_center_y - player.y
        dist_to_goal = math.hypot(goal_dx, goal_dy)
        
        # 1. Shoot range check (< 230px)
        if dist_to_goal < 230.0:
            target_y = self.opp_goal_center_y + random.uniform(-35, 35)
            dx = self.opp_goal_x - player.x
            dy = target_y - player.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                power = 8.5 + random.uniform(0.5, 2.0)
                vx = (dx / dist) * power
                vy = (dy / dist) * power
                # Lofted shot chance (40% if defenders block lane)
                vz = random.uniform(2.0, 4.2) if random.random() < 0.4 else 0.0
                ball.kick(vx, vy, vz, player)
            return

        # 2. Look for open passing options further up field
        for tm in teammates:
            if tm != player and tm.role != 'GK':
                # teammate is further forward
                if (self.team_id == 1 and tm.x > player.x + 60) or (self.team_id == 2 and tm.x < player.x - 60):
                    lane_clear = True
                    for opp in opponents:
                        opp_dist = self.distance_point_to_segment((opp.x, opp.y), (player.x, player.y), (tm.x, tm.y))
                        if opp_dist < 35.0:
                            lane_clear = False
                            break
                    
                    if lane_clear and random.random() < 0.4:
                        dx = tm.x - player.x
                        dy = tm.y - player.y
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            power = max(6.0, dist * 0.05)
                            vx = (dx / dist) * power
                            vy = (dy / dist) * power
                            # Randomly loft cross pass if far away
                            vz = 3.0 if dist > 180.0 and random.random() < 0.5 else 0.0
                            ball.kick(vx, vy, vz, player)
                        return

        # 3. Dribble forward
        dodge_y = 0.0
        for opp in opponents:
            opp_dx = opp.x - player.x
            opp_dy = opp.y - player.y
            opp_dist = math.hypot(opp_dx, opp_dy)
            if opp_dist < 55.0 and ((self.team_id == 1 and opp_dx > 0) or (self.team_id == 2 and opp_dx < 0)):
                # Dodge vertically away
                dodge_y = -35.0 if opp_dy > 0 else 35.0
                break
                
        sprint = dist_to_goal > 120.0 and random.random() < 0.75
        player.move(goal_dx, goal_dy + dodge_y, sprint_requested=sprint)

    def handle_offense_support(self, player, ball, teammates):
        carrier = ball.owner
        
        # Position targeting based on player roles
        if player.role == 'ATT':
            # Attacker pushes far forward, shifting towards center
            offset_x = 130.0 if self.team_id == 1 else -130.0
            offset_y = (self.opp_goal_center_y - carrier.y) * 0.4
        elif player.role == 'MID':
            # Midfielder tags slightly behind/above/below carrier
            offset_x = 60.0 if self.team_id == 1 else -60.0
            offset_y = 60.0 if carrier.y < self.height/2 else -60.0
        else: # DEF1 / DEF2
            # Defenders stay behind carrier to absorb counters
            offset_x = -90.0 if self.team_id == 1 else 90.0
            offset_y = -50.0 if player.number in [2, 7] else 50.0 # Spread defender layout

        target_x = carrier.x + offset_x
        target_y = carrier.y + offset_y
        
        # Bounds clamps
        target_x = max(self.margin_x + 50, min(self.width - self.margin_x - 50, target_x))
        target_y = max(self.margin_y + 35, min(self.height - self.margin_y - 35, target_y))
        
        dx = target_x - player.x
        dy = target_y - player.y
        player.move(dx, dy, sprint_requested=False)

    def handle_defense_or_loose(self, player, ball, teammates, opponents):
        # Determine closest outfielder teammate to chase loose ball/carrier
        outfield_teammates = [t for t in teammates if t.role != 'GK']
        closest_teammate = min(outfield_teammates, key=lambda t: math.hypot(ball.x - t.x, ball.y - t.y))
        
        if player == closest_teammate:
            # Press the ball!
            dx = ball.x - player.x
            dy = ball.y - player.y
            dist = math.hypot(dx, dy)
            player.move(dx, dy, sprint_requested=(dist > 70.0))
        else:
            # Mark space or fall back
            if player.role == 'DEF':
                # Defenders retreat to protect penalty box
                target_x = self.own_goal_x + (150.0 if self.team_id == 1 else -150.0)
                # Spread Y
                target_y = self.height * 0.35 if player.number in [2, 7] else self.height * 0.65
                # Align slightly to follow ball height
                target_y += (ball.y - self.height/2) * 0.3
            elif player.role == 'MID':
                # Midfielder stays between ball and center-pitch
                target_x = ball.x - (100.0 if self.team_id == 1 else -100.0)
                target_y = ball.y
            else: # ATT
                # Attacker stands high, ready for counter
                target_x = self.width * 0.55 if self.team_id == 1 else self.width * 0.45
                target_y = self.height * 0.5
                
            dx = target_x - player.x
            dy = target_y - player.y
            player.move(dx, dy, sprint_requested=False)

    def distance_point_to_segment(self, pt, s1, s2):
        px, py = pt
        x1, y1 = s1
        x2, y2 = s2
        
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
            
        t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)
        t = max(0.0, min(1.0, t))
        
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        return math.hypot(px - closest_x, py - closest_y)

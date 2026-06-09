import pygame
import math
import random

class NetNode:
    def __init__(self, x, y):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.mass = 1.0

    def update(self, stiffness=0.15, damping=0.85):
        # Spring force pulling back to original position
        fx = -stiffness * (self.x - self.original_x)
        fy = -stiffness * (self.y - self.original_y)
        
        # Acceleration
        ax = fx / self.mass
        ay = fy / self.mass
        
        # Update velocity & position
        self.vx = (self.vx + ax) * damping
        self.vy = (self.vy + ay) * damping
        self.x += self.vx
        self.y += self.vy

class GoalNetPhysics:
    def __init__(self, post1_y, post2_y, goal_x, net_depth_x, is_left=True):
        self.is_left = is_left
        self.post1_y = post1_y
        self.post2_y = post2_y
        self.goal_x = goal_x
        self.net_depth_x = net_depth_x
        
        # Create nodes along the back of the net
        self.nodes = []
        num_nodes = 8
        step = (post2_y - post1_y) / (num_nodes - 1)
        for i in range(num_nodes):
            ny = post1_y + i * step
            self.nodes.append(NetNode(net_depth_x, ny))

    def update(self):
        for node in self.nodes:
            node.update()
            
        # Structural springs pulling adjacent nodes together
        stiffness = 0.08
        for i in range(len(self.nodes) - 1):
            n1 = self.nodes[i]
            n2 = self.nodes[i+1]
            dx = n2.x - n1.x
            dy = n2.y - n1.y
            dist = math.hypot(dx, dy)
            target = (self.post2_y - self.post1_y) / (len(self.nodes) - 1)
            if dist > 0:
                diff = (dist - target) / dist
                offset_x = dx * 0.5 * diff * stiffness
                offset_y = dy * 0.5 * diff * stiffness
                n1.x += offset_x
                n1.y += offset_y
                n2.x -= offset_x
                n2.y -= offset_y

    def check_ball_collision(self, ball, ball_radius=10):
        # Check if inside Y range of the goal
        in_y_range = self.post1_y <= ball.y <= self.post2_y
        
        if not in_y_range:
            return

        # Collision with back of the net
        if self.is_left:
            if ball.x - ball_radius <= self.net_depth_x + 10 and ball.x > self.net_depth_x - 20:
                nearest_node = min(self.nodes, key=lambda n: abs(n.y - ball.y))
                force = abs(ball.vx) * 0.5 + 2.0
                nearest_node.vx -= force
                ball.x = self.net_depth_x + 10 + ball_radius
                ball.vx = -ball.vx * 0.22 # Vintage dead ball damp
                ball.vy = ball.vy * 0.8
        else:
            if ball.x + ball_radius >= self.net_depth_x - 10 and ball.x < self.net_depth_x + 20:
                nearest_node = min(self.nodes, key=lambda n: abs(n.y - ball.y))
                force = abs(ball.vx) * 0.5 + 2.0
                nearest_node.vx += force
                ball.x = self.net_depth_x - 10 - ball_radius
                ball.vx = -ball.vx * 0.22
                ball.vy = ball.vy * 0.8

        # Collision with top/bottom walls of the net
        if self.is_left:
            if ball.x < self.goal_x:
                if abs(ball.y - self.post1_y) < ball_radius:
                    ball.y = self.post1_y + ball_radius
                    ball.vy = -ball.vy * 0.3
                elif abs(ball.y - self.post2_y) < ball_radius:
                    ball.y = self.post2_y - ball_radius
                    ball.vy = -ball.vy * 0.3
        else:
            if ball.x > self.goal_x:
                if abs(ball.y - self.post1_y) < ball_radius:
                    ball.y = self.post1_y + ball_radius
                    ball.vy = -ball.vy * 0.3
                elif abs(ball.y - self.post2_y) < ball_radius:
                    ball.y = self.post2_y - ball_radius
                    ball.vy = -ball.vy * 0.3

    def draw(self, screen, color=(220, 210, 195, 120)):
        # Draw vintage mesh ropes
        post1 = (self.goal_x, self.post1_y)
        post2 = (self.goal_x, self.post2_y)
        points = [(node.x, node.y) for node in self.nodes]
        net_lines = [post1] + points + [post2]
        
        # Main thick support rope
        pygame.draw.lines(screen, color, False, net_lines, 2)
        
        # Draw net mesh squares (classic brown/cream color)
        for node in self.nodes:
            # Horizontal rope
            pygame.draw.line(screen, (color[0], color[1], color[2], 60), (node.x, node.y), (self.goal_x, node.y), 1)

def handle_ball_pitch_bounds(ball, width, height, margin_x=50, margin_y=30, goal_y1=240, goal_y2=360):
    left_x = margin_x
    right_x = width - margin_x
    top_y = margin_y
    bottom_y = height - margin_y
    
    ball_radius = 8
    
    # Check top/bottom boundaries
    if ball.y - ball_radius < top_y:
        ball.y = top_y + ball_radius
        ball.vy = -ball.vy * 0.5
        ball.vx *= 0.88
    elif ball.y + ball_radius > bottom_y:
        ball.y = bottom_y - ball_radius
        ball.vy = -ball.vy * 0.5
        ball.vx *= 0.88

    in_goal_y = goal_y1 <= ball.y <= goal_y2
    
    if in_goal_y:
        # Check post bounces (wooden post style!)
        for post_x, post_y in [(left_x, goal_y1), (left_x, goal_y2), (right_x, goal_y1), (right_x, goal_y2)]:
            dx = ball.x - post_x
            dy = ball.y - post_y
            dist = math.hypot(dx, dy)
            if dist < ball_radius + 6:
                if dist > 0:
                    nx = dx / dist
                    ny = dy / dist
                    dot = ball.vx * nx + ball.vy * ny
                    # Classic wooden post: high restitution (bouncy) but heavy damp
                    ball.vx = (ball.vx - 2 * dot * nx) * 0.65
                    ball.vy = (ball.vy - 2 * dot * ny) * 0.65
                    ball.x = post_x + nx * (ball_radius + 6.5)
                    ball.y = post_y + ny * (ball_radius + 6.5)
    else:
        # Normal sideline bounce
        if ball.x - ball_radius < left_x:
            ball.x = left_x + ball_radius
            ball.vx = -ball.vx * 0.5
            ball.vy *= 0.88
        elif ball.x + ball_radius > right_x:
            ball.x = right_x - ball_radius
            ball.vx = -ball.vx * 0.5
            ball.vy *= 0.88

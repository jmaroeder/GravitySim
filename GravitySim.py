from scene import *
from random import random, uniform

EDGE_BUFFER = 200

STATS_UPDATE_INTERVAL = 10

SIM_DT = 0.01 # 100 fps simulation

MAX_FRAME_TIME = 0.25

PURE = Color(1,1,1,1)




class Ptoid (object):
	def __init__(self, pos = Point(0,0), vel = Point(0,0), acc = Point(0,0),
	             radius = 10, mass = 10, color = Color(1,1,1)):
		self.pos = pos
		self.vel = vel
		self.acc = acc
		self.radius = radius
		self.mass = mass
		self.color = color
		
	def intersects(self, other):
		pos1 = self.pos
		pos2 = other.pos
		radius1 = self.radius
		radius2 = other.radius
		dx = pos2.x - pos1.x
		dy = pos2.y - pos1.y
		radii = radius1 + radius2
		if (dx * dx) + (dy * dy) < (radii * radius):
			return True
		else:
			return False
			
	def update(self):
		self.pos.x += self.vel.x
		self.pos.y += self.vel.y
		
		self.vel.x += self.acc.x
		self.vel.y += self.acc.y
		
	
	def draw(self):
		tint(*self.color)
		image('White_Circle', self.pos.x - self.radius,
		      self.pos.y - self.radius,
		      self.radius * 2, self.radius * 2)


class GravSim (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		self.ptoids = set()
		self.show_stats = True
		self.framecount = 0
		self.statsimg = None
		self.lastbounds = None
		self.diebounds = None
		
		self.accumulator = 0.0
		self.simtime = 0.0
	
	def update(self):
		'Updates the physics'
		dead = set()
		
		if self.lastbounds != self.bounds:
			self.lastbounds = self.bounds
			self.diebounds = Rect(self.bounds.x - EDGE_BUFFER,
			                      self.bounds.y - EDGE_BUFFER,
			                      self.bounds.w + EDGE_BUFFER * 2,
			                      self.bounds.h + EDGE_BUFFER * 2)
		
		for p in self.ptoids:
			p.update()
			if not p.pos in self.diebounds:
				dead.add(p)
		
		self.ptoids -= dead

	
	def render(self):
		for p in self.ptoids:
			p.draw()
				
		if self.framecount % STATS_UPDATE_INTERVAL == 0:
			self.statsimg, sz = render_text("Ptoids: {}\nFPS: {}".format(len(self.ptoids), 1.0 / self.dt))
		
		if self.show_stats:
			tint(*PURE)
			image(self.statsimg, 5, 5)
					
	
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		
		# Fixed time step from http://gafferongames.com/game-physics/fix-your-timestep/
		frame_time = min(self.dt, MAX_FRAME_TIME) # prevent death spiral
		
		self.accumulator += frame_time
		
		while self.accumulator >= SIM_DT:
			self.update()
			self.simtime += SIM_DT
			self.accumulator -= SIM_DT
		
		
		self.render()		
		
		self.framecount += 1
	
	def touch_began(self, touch):
		density = uniform(0.5, 3.0)
		radius = uniform(5, 50)
		mass = density * radius * radius
		p = Ptoid(pos = touch.location,
		          vel = Point(uniform(-2, 2), uniform(-2, 2)),
		          radius = radius,
		          mass = mass,
		          color = Color(random(), random(), random(), random()))
		self.ptoids.add(p)
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

run(GravSim())

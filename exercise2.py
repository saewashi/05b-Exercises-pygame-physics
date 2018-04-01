#!/usr/bin/env python
'''

For every line in the collide method (lines 58-91), please add a comment describing what it does. 

Try to describe each line within the context of the program as a whole, rather than just mechanically

Feel free to alter the parameters to see how things change. That can be a great way to be able to intuit what is supposed to be happening

I will do a few lines for you as an example


'''
import sys, logging, math, pygame, random as r
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

screen_size = (WIDTH,HEIGHT) = (600,600)
FPS = 60
black = (0,0,0)

class Ball(pygame.sprite.Sprite):
	def __init__(self, label, size, mass, color, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.label = label
		self.size = size
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect()
		pygame.draw.ellipse(self.image, color, self.rect)
		self.image.set_colorkey((0,0,0))
		(self.rect.x,self.rect.y) = position
		self.direction = direction
		self.mass = mass
		self.collided = False

	def update(self):
		(dx,dy) = self.direction
		self.rect.x += dx
		self.rect.y += dy
		
		(WIDTH,HEIGHT) = screen_size
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
			dx *= -1
		if self.rect.left < 0:
			self.rect.left = 0
			dx *= -1
		if self.rect.top < 0:
			self.rect.top = 0 # Setting rect.top = 0
			dy *= -1 # Setting the vertical and multplying/equalizing it to -1.
		if self.rect.bottom > HEIGHT: # If statement for making rect.bottom greater than height.
			self.rect.bottom = HEIGHT # Setting rect.bottom equal to height.
			dy *= -1 # Same as line 52.
		self.direction = (dx,dy) # Setting the direction equal to the horizontal and vertical.
	
	def collide(self, other_object): # Defining a collision between another object.
		'''
		
		Checks to see if the object has collided with another object. Assumes that each collision will be calculated pairwise.
		If there has been a collision, and the objects are still moving toward each other, the direction attribute of both objects is updated
		
		
		'''
		(dx,dy) = self.direction				# the x and y components of the direction
		(odx,ody) = other_object.direction		# the x and y components of the other object's direction
		(cx,cy) = self.rect.center # setting cx and cy to the center?
		(ocx,ocy) = other_object.rect.center # Having the other objects collide with the center object?
		radius = self.rect.width/2 # setting the radius and dividing the rect.width by 2.
		oradius = other_object.rect.width/2 # setting the oradius to the other object and dividing the width by 2.
		#find the hypotenuse
		distance = math.sqrt(abs(cx-ocx)**2 + abs(cy-ocy)**2) # Setting the distance with the square root of bouncing objects, times 2
		if distance <= 0: # If statement for distance less-than or equal to 0
			distance = 0.1 # distance is equal to 0.1
		combined_distance = (radius+oradius) # Combining the distance with the radius and oradius.
		if distance <= combined_distance:	#collision
			normal = ((cx-ocx)/distance,(cy-ocy)/distance)	# a vector tangent to the plane of collision
			velocity_delta = ((odx-dx),(ody-dy))	#the relative difference between the speed of the two objects
			(nx,ny) = normal # making nx and ny equal to normal
			(vdx,vdy) = velocity_delta # setting the components to equal the velocity_delta.
			dot_product = nx*vdx + ny*vdy # setting the dot_
			if dot_product >= 0:	#check if the objects are moving toward each other
				impulse_strength = dot_product * (self.mass / other_object.mass) # setting the impulse strength to equal the dot product and multiplying it times mass and the other objects mass.
				impulse = (ix,iy) = (impulse_strength * nx, impulse_strength * ny) # impulse equal to the componments and the multiplying the impulse strength by the components.
				dx += ix * (other_object.mass/self.mass) # taking the componments and += to the other object mass and dividing by the main mass.
				dy += iy * (other_object.mass/self.mass) # same as above, just this time with iy.
				self.direction = (dx,dy) # Setting the direction the componments of the vertical and horizontal.
				odx -= ix * (self.mass/other_object.mass) # Taking the odx componment and making it less equal to ix times the mass and other object mass.
				ody -= iy * (self.mass/other_object.mass) # Same as above, just with the ody and iy.
				other_object.direction = (odx,ody) # Setting the other object direction to the odx and ody componments.

	def draw(self,screen):
		self.image.blit(screen,(0,0),self.rect)

	def get_energy(self):
		(dx,dy) = self.direction
		return math.sqrt(abs(dx)**2 + abs(dy)**2)/self.mass

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()

	balls = []
	colors = [(255,212,59),(34,139,230),(240,62,62),(174,62,201),(253,126,20),(64,192,87),(194,37,92),(73,80,87)]
	positions = [(260,180),(180,100),(260,100),(340,100),(220,60),(220,140),(300,140),(300,60)]
	size = (50,50)
	mass = 30
	initial_velocity = (0,0)
	for c in range(len(colors)):
		initial_position = positions[c]
		ball = Ball('{0}'.format(c+1),size,mass,colors[c],initial_position,initial_velocity)
		balls.append(ball)
	ball = Ball('Cue',size,mass,(255,255,255),(260,500),(0,-20))
	balls.append(ball)

	ball_group = pygame.sprite.Group()
	for b in balls:
		ball_group.add(b)

	
	while True:
		clock.tick(FPS)
		screen.fill(black)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

		for b in balls:
			for c in balls:
				if b.label != c.label:
					b.collide(c)
		ball_group.update()
		ball_group.draw(screen)
		pygame.display.flip()

if __name__ == '__main__':
	main()
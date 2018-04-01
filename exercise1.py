#!/usr/bin/env python
'''

Choose values for gravity, friction, and air_resistance (lines 25–27). Try to find a combination that seems realistic

For every line in the update method (lines 41-66), please add a comment describing what it does. 

Try to describe each line within the context of the program as a whole, rather than just mechanically

Feel free to alter the parameters to see how things change. That can be a great way to be able to intuit what is supposed to be happening

I will do a few lines for you as an example


'''
import sys, logging, random, pygame
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

screen_size = (600,600)
FPS = 60
black = (0,0,0)
gravity = 0.5
friction = 0.1
air_resistance = 0.1

class Ball(pygame.sprite.Sprite):
	def __init__(self, i, size, color, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect()
		pygame.draw.ellipse(self.image, color, self.rect)
		self.image.set_colorkey((0,0,0))
		(self.rect.x,self.rect.y) = position
		self.direction = direction
		self.id = i

	def update(self): # This is to update the program with any changes made.
		(dx,dy) = self.direction	# get the current velocity
		self.rect.x += dx		# move the sprite horizontally
		self.rect.y += dy   # Moves the sprite vertically

		dy = dy + gravity # this is adding the horizontal and vertical movements to gravity.
		dx *= (1.0-air_resistance) # this is taking the horizontal movement and multiplying with the air resistence.
		dy *= (1.0-air_resistance) # this is taking the veritcal movement and mulptying it with the air resistence.
		
		(WIDTH,HEIGHT) = screen_size # this is setting the width and height to the screen size.
		if self.rect.right >= WIDTH: # this is an if statement if the sprite is greater than or equal to the width,
			self.rect.right = WIDTH # Same as above, just the sprite is equal to the width.
			dx = dx * -1 * (1.0-friction) # taking the horizontal,  and taking it and multipying to the friction.
		if self.rect.left <= 0: # If statement for rect.left less than or equal to 0.
			self.rect.left = 0 # Setting rect.left to 0.
			dx = dx * -1 * (1.0-friction) # Same as line 53
		if self.rect.top <= 0: # If statement for rect.top less than or equal 0.
			self.rect.top = 0 # setting rect.top equal to 0.
			dy = dy * -1 * (1.0-friction) # Setting the vertical and multiplying it with -1, and the friction.
		if self.rect.bottom >= HEIGHT: # If statement for rect.bottom to greater than or equal to height.
			self.rect.bottom = HEIGHT # setting the rect.bottom equal to height.
			dx = dx * -1 * (1.0-friction) # setting the horizontal and multiplying it by -1 and friction.
			dy = dy * -1 * (1.0-friction) # setting the vertical and multiplying by -1 and the friction.
			if abs(dy) < 1:			# a hack to keep it from bouncing forever
				dy = 0 # setting the vertical equal to 0.
		self.direction = (dx,dy) # Setting the direction to the vertical and horizontal movements.


def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()

	balls = pygame.sprite.Group()
	for i in range(random.randrange(10,50)):
		size = random.randrange(10,50)
		color = (random.randrange(255),random.randrange(255),random.randrange(255))
		initial_position = (random.randrange(25,screen_size[0]-25),random.randrange(25,screen_size[1]-25))
		initial_velocity = (random.randrange(-10,10),0)
		ball = Ball(i,(size,size),color,initial_position,initial_velocity)
		balls.add(ball)

	while True:
		clock.tick(FPS)
		screen.fill(black)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

		balls.update()
		balls.draw(screen)
		pygame.display.flip()

if __name__ == '__main__':
	main()
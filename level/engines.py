# -*- coding: utf-8 -*-
import pygame, random, sys, string
from helpers import Stop_Watch, Trial_Data
from helpers.log import Trial_Logger
from helpers.debug import Debugger
from pygame.locals import *

class Engine:

	def __init__(self, surface, bg, syllables, syllable_sounds, syllable_images, random_order, order, neo=True):
		self.frames = 40
		self.surface = surface
		self.bg = bg
		self.random_order = random_order
		self.order = order
		self.mainClock = pygame.time.Clock()
		self.curser_unvisible = False

		self.syllable_images = syllable_images
		self.syllables_allowed = syllables
		self.syllable_sounds = syllable_sounds
		self.syllables_called = {}

		if syllables != None:
			self.n_syllables = len(syllables)
			self.syllables = syllables.keys()
			for syllable in self.syllables:
				self.syllables_called[syllable] = 0

		if neo:
			self.left = u'xvlcwuiaeoüöäpzXVLCWUIAEOÜÖÄPZ'
			self.right = u'khgfqßsnrtdybm,.jKHGFQẞSNRTDYBM–•J'
		else:
			self.left = u'qwertasdfgyxcvbQWERTASDFGYXCVB'
			self.right = u'zuiopühjklöänmm,.-ZUIOPÜHJKLÖÄNM'


	def toggle_fullscreen(self):

		pygame.display.toggle_fullscreen()
		self.curser_unvisible = pygame.mouse.set_visible(self.curser_unvisible)


	def standart_event(self,event):

		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_F10:
				self.toggle_fullscreen()


	def get_miss(self): return self.miss
	
	def get_frams(self): return self.frames

	
	def set_frames(self,frames):
		self.frames = frames


	def move(self,start,stop,time,position):

		speed = (stop - stop) / time
		#have to find a way to get the frame rate, so i can evolve the actuel pixels to move at a frame
		return int(position + speed/40.)


	def draw_sprite(self,sprite):
		self.surface.blit(sprite,(self.position_center_width(sprite),self.surface.get_size()[1]-sprite.get_size()[1]))


	def enter_sprite(self,sprite,direction,time=1):
		if direction == 0:
			start = -1*sprite.get_size()[0]
		else:
			start = self.surface.get_size()[0]

		stop = self.position_center_width(sprite)
		move = float(stop - start)/float(time*40)

		p = start
		for i in range(time*40):
			self.surface.blit(self.bg,(0,0))
			p += move
			self.surface.blit(sprite,(p,self.surface.get_size()[1]-sprite.get_size()[1]))
			pygame.display.update()
			self.mainClock.tick(40)
		
		self.surface.blit(self.bg,(0,0))
		self.draw_sprite(sprite)
		pygame.display.update()


	def exit_sprite(self,sprite,direction,time=1):

		if direction == 0:
			stop = self.surface.get_size()[0]
		else:
			stop = -1*sprite.get_size()[0]

		start = self.position_center_width(sprite)
		move = float(stop - start)/float(time*40)
		
		p = start
		for i in range(time*40):
			self.surface.blit(self.bg,(0,0))
			p += move
			self.surface.blit(sprite,(p,self.surface.get_size()[1]-sprite.get_size()[1]))
			pygame.display.update()
			self.mainClock.tick(40)

		self.surface.blit(self.bg,(0,0))
		pygame.display.update()


	def sprite_fly_in(self,s_l,s_r,time=1):

		y_l = self.position_center_height(s_l)
		y_r = self.position_center_height(s_r)
		p_l = -1*s_l.get_size()[0]
		p_r = self.surface.get_size()[0]
		m = float(p_r/2.2)/float(time*40)

		for i in range(time*40):
			self.surface.blit(self.bg,(0,0))
			p_l += m
			p_r -= m
			self.surface.blit(s_l,(p_l,y_l))
			self.surface.blit(s_r,(p_r,y_r))
			pygame.display.update()
			self.mainClock.tick(40)

		return (int(p_l),y_l),(int(p_r),y_r)


	def draw_syllable_left(self,syllable):

		self.surface.blit(syllable,(150,300))


	def draw_syllable_right(self,syllable):

		self.surface.blit(syllable,(self.surface.get_size()[0]-syllable.get_size()[0]-150,300))


	def choose_two(self,source):

		out1 = random.randint(0,source-1)
		out2 = random.randint(0,source-2)

		if out1 <= out2:
			out2 = out2 + 1

		return (out1,out2)

	def check_correct_syllable(self,syllable):

		if self.syllables_called[syllable] < self.syllables_allowed[syllable]:
			self.syllables_called[syllable] += 1
			return True
		else:
			return False


	def position_center_width(self,item):

		return self.surface.get_size()[0]/2 - item.get_size()[0]/2


	def position_center_height(self,item):

		return self.surface.get_size()[1]/2 - item.get_size()[1]/2

	def reset_syllables_called(self):
		
		for syllable in self.syllables:
			self.syllables_called[syllable] = 0

#	Class used to give easy tools to move sprites

	class Sprite:

		def __init__(self,surface,sprite,(x,y)):
			self.surface = surface
			self.pic = sprite
			self.position = (x,y)

		def move(self,dx,dy):
			self.position = (self.position[0]+dx,self.position[1]+dy)

		def draw(self):
			self.surface.blit(self.pic,self.position)

		def get_position(self):
			return self.position

		def set_position(self,x,y):
			self.position = (x,y)

		def get_sprite(self):
			return self.pic


#	Engine used in modules A and U
#	in:
#		log: Log file for this module. type Trial_Logger
#		surface: the surface of which the graphics of the game should be drawn. type pygame.Surface
#		bg: the background image of the module. type pygame.Surface
#		sprites: a list of all sprites used in this module
#		syllables: a list of all syllables

class OneOutOfTwo(Engine):

	def __init__(self, log, surface, bg, sprites, syllables, syllable_images, syllable_sounds, random_order=True, order=None, neo=True):
		Engine.__init__(self,surface,bg,syllables,syllable_sounds,syllable_images,random_order,order,neo)
		self.log = log
		self.sprites = sprites
		self.n_sprites = len(self.sprites)


	def start(self,n=10):

		miss = 0
		sw = Stop_Watch()
		self.reset_syllables_called()
		self.log.set_top('trial_nr\tsyllable_l\tsyllable_r\tsound\tkey_pressed\tresponse\tresponsetime\tsprite')

		if not self.random_order:
			trials = Trial_Data(self.order)
			n = trials.get_n_trials()
			site = []

		for i in range(n):
			size = self.surface.get_size()
			self.bg = pygame.transform.scale(self.bg,size)
			self.surface.blit(self.bg,(0,0))

			if self.random_order:
				correct = random.randint(0,1)
				direction = random.randint(0,1)
				if direction == 0:
					direction_str = 'l'
				else:
					direction_str = 'r'

				sprite_str = self.sprites.keys()[random.randint(0,self.n_sprites-1)]

				check = True
				i = 0
				while check:
					i += 1
					syllable = self.choose_two(self.n_syllables)
					if i < 20:
						check = not self.check_correct_syllable(self.syllables[syllable[correct]])
					else:
						check = False
				syllable_str = [self.syllables[syllable[0]],self.syllables[syllable[1]]]

			else:
				accept = False
				while not accept:
					
					trial_index,trial = trials.get_trial()
					syllable_correct = trial[2]
					syllable_left = string.lower(trial[3])
					syllable_right = string.lower(trial[4])
					syllable_str = [syllable_left,syllable_right]
					if syllable_correct == syllable_left:
						correct = 0
					else:
						correct = 1
					if len(site) == 0 or trials.get_n_trials() <= 1 or i > 20:
						site.append(correct)
						accept = True
					else:
						if site[len(site)-1] != correct:
							site = [correct]
							accept = True
						else:
							if len(site) < 2:
								site.append(correct)
								accept = True

				trials.accept(trial_index)
				sprite = trial[1]
				sprite_str = sprite[:-2]
				direction_str = string.lower(sprite[-1:])
				if direction_str == 'l':
					direction = 0
				else:
					direction = 1

			sprite = self.sprites[sprite_str][direction_str]
			self.enter_sprite(sprite,direction)
			pygame.event.clear()
			self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
			self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
			pygame.display.update()

			self.syllable_sounds[syllable_str[correct]][str(random.randint(1,3))].play()
			sw.start()

			key_pressed = False
			press = 0

			while True:

				for event in pygame.event.get():
					self.standart_event(event)
					if event.type == KEYDOWN:
						try:
							if self.left.find(unichr(event.key))>= 0:
								sw.stop()
								press = 0
								key_pressed = True
							if self.right.find(unichr(event.key)) >=0:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				
				if press == correct and key_pressed:
					log_line = [trial[0],syllable_str[0],syllable_str[1],syllable_str[correct],press,int(press==correct),sw.get_time(),sprite_str]
#					print(log_line)
					self.log.add(log_line)
					self.syllable_sounds[syllable_str[correct]]['pos'+str(random.randint(1,4))].play()
					self.surface.blit(self.bg,(0,0))
					self.draw_sprite(sprite)
					if correct == 0:
						self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
					else:
						self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
					pygame.display.update()
					pygame.time.wait(3700)
					pygame.event.clear()
					break

				if press != correct and key_pressed:
					log_line = [i,syllable_str[0],syllable_str[1],syllable_str[correct],press,int(press==correct),sw.get_time(),sprite_str]
					self.log.add(log_line)
					key_pressed = False
					self.syllable_sounds[syllable_str[correct]]['neg'+str(random.randint(1,2))].play() 
					self.surface.blit(self.bg,(0,0))
					self.draw_sprite(sprite)
					if correct == 0:
						self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
					else:
						self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
					pygame.display.update()
					pygame.time.wait(4500)
					miss += 1
					
					if correct == 0:
						self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
					else:
						self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
					pygame.display.update()
					self.syllable_sounds[syllable_str[correct]][str(random.randint(1,3))].play()
					sw.start()
					pygame.event.clear()

				self.mainClock.tick(40)
			self.exit_sprite(sprite,direction)

		return miss

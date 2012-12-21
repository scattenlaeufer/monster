# -*- coding: utf-8 -*-

#	{{{ import
import pygame, sys, random, time, os
from pygame.locals import *
#from engines import OneOutOfTwo, Space_Engine, Balloon_Engine, CatchMeIfYouCan, OneOutOfThree
from helpers.log import Log_Handler, Trial_Logger
from helpers import Stop_Watch
#	}}}

#	{{{ class Stage
#generic form of a stage. all actual stages should inherit from this

class Stage:

#	{{{ __init__
	def __init__(self,bla=True,neo=False):
		
		self.path = __file__[:-10]
		self.miss = 0
		self.instr = None
		self.mainClock = pygame.time.Clock()

		# init pygame
		pygame.init()

		# set window
		self.windowwidth = 1024
		self.windowheight = 768
		self.curser_unvisible = False
		self.surface = pygame.display.set_mode((self.windowwidth,self.windowheight),0,32)
		pygame.display.set_caption('Monster v0.1') 

#		self.bg_blank = (194,194,194)
		self.bg_blank = (255,255,255)
		self.surface.fill(self.bg_blank)
		self.font1 = pygame.font.Font(None,70)

		if neo:
			self.left = u'xvlcwuiaeoüöäpzXVLCWUIAEOÜÖÄPZ'
			self.right = u'khgfqßsnrtdybm,.jKHGFQẞSNRTDYBM–•J'
		else:
			self.left = u'qwertasdfgyxcvbQWERTASDFGYXCVB'
			self.right = u'zuiopühjklöänmm,.-ZUIOPÜHJKLÖÄNM'
		if bla:
			self.text = self.font1.render('Willkommen zum Monsterspiel',True,(0,0,0))
			self.surface.blit(self.text,(self.position_center_width(self.text),100))
#	}}}

#	{{{ get_path
	def get_path(self,path):
		return os.path.join(self.path,path)
#	}}}

#	{{{ toggle_fullscreen
	def toggle_fullscreen(self):
		
		pygame.display.toggle_fullscreen()
		self.curser_unvisible = pygame.mouse.set_visible(self.curser_unvisible)
		
#		if self.curser_unvisible:
#			self.windowwidth = self.desktopwidth
#			self.windowheight = self.desktopheight
#		else:
#			self.windowwidth = 1024
#			self.windowheight = 768

#		self.surface = pygame.transform.scale(self.surface,(self.windowwidth,self.windowheight))
#		pygame.display.update()
#	}}}

#	{{{ start
	def start(self,modul):
	
		text = self.font1.render(modul,True,(0,0,0))
		self.surface.blit(text,(self.position_center_width(text),250))
		pygame.display.update()

		text = self.font1.render(u'bitte Enter-Taste drücken',True,(0,0,0))
		self.surface.blit(text,(self.position_center_width(text),400))
		pygame.display.update()

		bla = True

		while bla:
			for event in pygame.event.get():
				self.standart_event(event)
				if event.type == KEYDOWN:
					if event.key == K_RETURN:
						bla = False

			self.mainClock.tick(20)
#	}}}

#	{{{ stop
	def stop(self):
		
		self.surface.fill(self.bg_blank)
		text = self.font1.render('Bitte nehmen Sie Kontakt mit uns auf.',True,(0,0,0))
		self.surface.blit(text,(self.position_center_width(text),self.position_center_height(text)))
		pygame.display.update()

		pygame.event.clear()
		bla = True
		while bla:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						bla = False
			self.mainClock.tick(10)

		pygame.quit()
		sys.exit()
#	}}}

#	{{{ end
	def end(self):
		
		image = pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg'))
		self.surface.blit(image,(0,0))
		pygame.display.update()
		self.play_instruction('audio/final/final1.ogg',False)
		pygame.quit()
		sys.exit()
#	}}}

#	{{{ load_sound
	def load_sound(self,name):
		
		class NoneSound:
			def play(self): pass
		if not pygame.mixer:
			return NoneSound()
		try:
			sound = pygame.mixer.Sound(name)
		except pygame.error, message:
			print 'Cannot load sound:', ogg 
			raise SystemExit, message
		return sound
#	}}}

#	{{{ load_syllable_sound
	def load_syllable_sound(self,syllable):

		dic = {}
		
		dic['1'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'1.ogg'))
		dic['2'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'2.ogg'))
		dic['3'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'3.ogg'))
		
		dic['miss'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'miss.ogg'))
		
		dic['neg1'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'neg1.ogg'))
		dic['neg2'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'neg2.ogg'))
		
		dic['pos1'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos1.ogg'))
		dic['pos2'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos2.ogg'))
		dic['pos3'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos3.ogg'))
		dic['pos4'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos4.ogg'))
		
		return dic
#	}}}

#	{{{ play_instruction
	def play_instruction(self,instr,clean=True):
		
		self.instr = instr
		pygame.mixer.music.load(os.path.join(self.path,instr))
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.play()
		
		if clean:
			self.surface.fill(self.bg_blank)
			pygame.display.update()
				
		while True:
			for event in pygame.event.get():
				self.standart_event(event)

			if not pygame.mixer.music.get_busy():
				break
			
			self.mainClock.tick(20)
#	}}}

#	{{{ position_center_width
	def position_center_width(self,item):

		return self.windowwidth/2 - item.get_size()[0]/2
#	}}}

#	{{{ position_center_height
	def position_center_height(self,item):

		return self.windowheight/2 - item.get_size()[1]/2
#	}}}

#	{{{ draw
	def draw(self,image,dest=(0,0)):

		self.surface.blit(image,dest)
		pygame.display.update()
#	}}}

#	{{{ draw_left
	def draw_left(self,image):

		self.surface.blit(image,(self.windowwidth/12,self.position_center_height(image)))
#	}}}

#	{{{ draw_right
	def draw_right(self,image):

		self.surface.blit(image,(self.windowwidth*7/12,self.position_center_height(image)))
#	}}}

#	{{{ standart_event
	def standart_event(self,event):

		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_F10:
				self.toggle_fullsreen()
			if event.key == K_F12 and pygame.mixer.music.get_busy():
				pygame.mixer.music.stop()
#	}}}

#	{{{ watch_keypress
	def watch_keypress(self):

		for event in pygame.event.get():
			self.standart_event(event)
#	}}}

#	{{{ teach_monster
	def teach_monster(self,image,sound):
 
		self.surface.fill(self.bg_blank)

		sound.play()

		im = pygame.image.load(os.path.join(self.path,image))
		dimension = (self.windowwidth/3,self.transform_height(im,self.windowwidth/3))
		im = pygame.transform.scale(im,dimension)
		self.surface.blit(im,(self.position_center_width(im),self.position_center_height(im)))
		pygame.display.update()
		pygame.time.wait(3000)
		self.watch_keypress()
#	}}}

#	{{{ transform_height
	def transform_height(self,item,width):

		x = item.get_size()[0]
		y = item.get_size()[1]
		ratio = float(y)/float(x)
		return int(width * ratio)
#	}}}

#	{{{ test_monster
	def test_monster(self,monster,dic,log_title,response=True,n=8):

		miss = 0
		sw = Stop_Watch()
		log = Trial_Logger(log_title)
		log.set_top('trial_nr\tkey_pressed\tresponse\tresponse_time')
		m = 1
		side = []

		for i in range(n):
			self.surface.fill(self.bg_blank)
			a = True
			while a:
				correct = random.randint(0,1)
				if len(side) == 0:
					side.append(correct)
					a = False
				elif side[len(side)-1] == correct:
					if len(side) < 2:
						side.append(correct)
						a = False
				else:
					side = [correct]
					a = False
						

			image = pygame.image.load(os.path.join(self.path,monster[correct]))

			self.draw(image,(self.position_center_width(image),self.position_center_height(image)))

			pygame.display.update()
			
			sound = random.randint(0,1)
			dic[sound]['bla'][random.randint(0,4)].play()
			sw.start()

			key_pressed = False
			press = 0

			while True:
				for event in pygame.event.get():
					self.standart_event(event)

					if event.type == KEYDOWN:
						try:
							if self.left.find(unichr(event.key)) >= 0:
								sw.stop()
								press = 0
								key_pressed = True
							if self.right.find(unichr(event.key)) >= 0:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				if press == (correct == sound) and key_pressed:
					log.add([m,press,int(press==correct),sw.get_time()])
					if response:
						dic[correct]['pos'][random.randint(0,2)].play()
						pygame.time.wait(3700)
					else:
						pygame.time.wait(250)
					pygame.event.clear()

					self.surface.fill(self.bg_blank)
					pygame.display.update()
					pygame.time.wait(250)
					break
				if press != (correct == sound) and key_pressed:
					log.add([m,press,int(press==correct),sw.get_time()])
					miss += 1
					if response:
						dic[correct]['neg'][random.randint(0,2)].play()
						pygame.time.wait(4500)
						dic[sound]['bla'][random.randint(0,4)].play()
						key_pressed = False
						sw.start()
					else:
						pygame.time.wait(250)
						self.surface.fill(self.bg_blank)
						pygame.display.update()
						pygame.time.wait(250)
						break
					pygame.event.clear()
				
				self.mainClock.tick(40)

			pygame.time.wait(500)
			m += 1

		log.save()
		return miss
#	}}}

#	{{{ feedback
	def feedback(self,miss,x,outstanding=True):
		
		pygame.time.wait(1000)
		if miss == 0 and outstanding:
			self.draw(pygame.image.load(os.path.join(self.path,'images/feedback/feedback3.gif')))
			self.play_instruction('audio/feedback/feedback3.ogg',False)
		elif miss <= x:
			self.draw(pygame.image.load(os.path.join(self.path,'images/feedback/feedback2.gif')))
			self.play_instruction('audio/feedback/feedback2.ogg',False)
		else:
			self.draw(pygame.image.load(os.path.join(self.path,'images/feedback/feedback1.gif')))
			self.play_instruction('audio/feedback/feedback1.ogg',False)
		pygame.time.wait(1000)
#	}}}
#	}}}


class Monster1(Stage):

	def __init__(self):
		Stage.__init__(self,True,True)
		self.start('Teil 1')
#		self.play_instruction('audio/intro_begin.ogg')
		monster = ['images/monster1.jpg','images/monster2.jpg']
		
		sound_dic = {}
		sound_dic[0] = {}
		sound_dic[0]['bla'] = []
		sound_dic[0]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M11.ogg')))
		sound_dic[0]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M12.ogg')))
		sound_dic[0]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M13.ogg')))
		sound_dic[0]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M14.ogg')))
		sound_dic[0]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M15.ogg')))
		sound_dic[0]['pos'] = []
		sound_dic[0]['pos'].append(self.load_sound(os.path.join(self.path,'audio/pos_resp_M1_1.ogg')))
		sound_dic[0]['pos'].append(self.load_sound(os.path.join(self.path,'audio/pos_resp_M1_2.ogg')))
		sound_dic[0]['pos'].append(self.load_sound(os.path.join(self.path,'audio/pos_resp_M1_3.ogg')))
		sound_dic[0]['neg'] = []
		sound_dic[0]['neg'].append(self.load_sound(os.path.join(self.path,'audio/neg_resp_M1_1.ogg')))
		sound_dic[0]['neg'].append(self.load_sound(os.path.join(self.path,'audio/neg_resp_M1_2.ogg')))
		sound_dic[0]['neg'].append(self.load_sound(os.path.join(self.path,'audio/neg_resp_M1_1.ogg')))
		sound_dic[1] = {}
		sound_dic[1]['bla'] = []
		sound_dic[1]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M21.ogg')))
		sound_dic[1]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M22.ogg')))
		sound_dic[1]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M23.ogg')))
		sound_dic[1]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M24.ogg')))
		sound_dic[1]['bla'].append(self.load_sound(os.path.join(self.path,'audio/M25.ogg')))
		sound_dic[1]['pos'] = []
		sound_dic[1]['pos'].append(self.load_sound(os.path.join(self.path,'audio/pos_resp_M2_1.ogg')))
		sound_dic[1]['pos'].append(self.load_sound(os.path.join(self.path,'audio/pos_resp_M2_2.ogg')))
		sound_dic[1]['pos'].append(self.load_sound(os.path.join(self.path,'audio/pos_resp_M2_3.ogg')))
		sound_dic[1]['neg'] = []
		sound_dic[1]['neg'].append(self.load_sound(os.path.join(self.path,'audio/neg_resp_M2_1.ogg')))
		sound_dic[1]['neg'].append(self.load_sound(os.path.join(self.path,'audio/neg_resp_M2_2.ogg')))
		sound_dic[1]['neg'].append(self.load_sound(os.path.join(self.path,'audio/neg_resp_M2_1.ogg')))


#		self.teach_monster(monster[0],self.load_sound(os.path.join(self.path,'audio/intro_pic_M1.ogg')))
#		self.teach_monster(monster[1],self.load_sound(os.path.join(self.path,'audio/intro_pic_M2.ogg')))
#		self.play_instruction('audio/instr1.ogg')

#		self.play_instruction('audio/intro_train.ogg')

#		self.test_monster(monster,sound_dic,'monster1_train',True)

#		self.play_instruction('audio/intro_test.ogg')

		self.test_monster(monster,sound_dic,'monster1_test',False)

#		self.play_instruction('audio/quit.ogg')
		

# -*- coding: utf-8 -*-

# TODO:
#	fix negeativ sound response in test_monster(...)
#	test new logger => at least partialy done

#	{{{ import
import pygame, sys, random, os
from PyQt4 import QtGui
from pygame.locals import *
from helpers.log import Monster_Logger2
from helpers.dialog import ProbCodeDialog
from helpers import Stop_Watch, Trial_Data

try:
	from config import *
except ImportError:
	print('######################################\n'+
			'# Create config.py from defaults.py! #\n'+
			'######################################')
	from defaults import *
#	}}}


class Stage(object):
	#generic form of a stage. all actual stages should inherit from this

	def __init__(self,bla=True,neo=False,title='Monster'):

#		self.ask_prob_code('monster1_learn')

		self.path = __file__[:-10]
		self.miss = 0
		self.instr = None
		self.mainClock = pygame.time.Clock()

		# init pygame
		pygame.init()

		# set window
		self.windowwidth = 1366
		self.windowheight = 768
		self.curser_unvisible = True
		self.surface = pygame.display.set_mode((self.windowwidth,self.windowheight),pygame.FULLSCREEN,32)
		pygame.display.set_caption(title+' v0.1') 
		#pygame.display.toggle_fullscreen()
		pygame.mouse.set_visible(False)
		#self.bg_blank = (194,194,194)
		self.bg_blank = (255,255,255)
		self.surface.fill(self.bg_blank)
		base_size = 70
		self.font1 = pygame.font.Font(None,base_size)
		self.font2 = pygame.font.Font(None,base_size*5)

		if neo:
			self.left = u'xvlcwuiaeoüöäpzXVLCWUIAEOÜÖÄPZ'
			self.right = u'khgfqßsnrtdybm,.jKHGFQẞSNRTDYBM–•J'
		else:
			self.left = u'qwertasdfgyxcvbQWERTASDFGYXCVB'
			self.right = u'zuiopühjklöänmm,.-ZUIOPÜHJKLÖÄNM'
		if bla:
			self.text = self.font1.render('Willkommen zum '+title+'spiel',True,(0,0,0))
			self.surface.blit(self.text,(self.position_center_width(self.text),100))

	def get_path(self,path):
		return os.path.join(self.path,path)

	def toggle_fullscreen(self):
		pass
	#	pygame.display.toggle_fullscreen()
	#	self.curser_unvisible = pygame.mouse.set_visible(self.curser_unvisible)
	#	
	#	#if self.curser_unvisible:
	#	#	self.windowwidth = self.desktopwidth
	#	#	self.windowheight = self.desktopheight
	 	#else:
	#	#	self.windowwidth = 1024
	#	#	self.windowheight = 768

		#self.surface = pygame.transform.scale(self.surface,(self.windowwidth,self.windowheight))
		#pygame.display.update()

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

	def draw_text_center(self,text,font=None):
		if not font:
			font = self.font1
		text_obj = font.render(text,True,(0,0,0))
		self.surface.blit(text_obj,(self.position_center_width(text_obj),self.position_center_height(text_obj)))
		pygame.display.update()

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

	def end(self):
		
		image = pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg'))
		self.surface.blit(image,(0,0))
		pygame.display.update()
		self.play_instruction('audio/final/final1.ogg',False)
		pygame.quit()
		sys.exit()

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

	def position_center_width(self,item):

		return self.windowwidth/2 - item.get_size()[0]/2

	def position_center_height(self,item):

		return self.windowheight/2 - item.get_size()[1]/2

	def draw(self,image,dest=(0,0)):

		self.surface.blit(image,dest)
		pygame.display.update()

	def draw_left(self,image):

		self.surface.blit(image,((self.windowwidth/2-image.get_width())/2,self.position_center_height(image)))

	def draw_right(self,image):

		self.surface.blit(image,(self.windowwidth/2 + (self.windowwidth/2-image.get_width())/2,self.position_center_height(image)))

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

	def watch_keypress(self):

		for event in pygame.event.get():
			self.standart_event(event)

	def teach_monster(self,image,sound,resize=True):
 
		self.surface.fill(self.bg_blank)

		sound.play()

		im = pygame.image.load(os.path.join(self.path,image))
		if resize:
			dimension = (self.windowwidth/3,self.transform_height(im,self.windowwidth/3))
			im = pygame.transform.scale(im,dimension)
		self.surface.blit(im,(self.position_center_width(im),self.position_center_height(im)))
		pygame.display.update()
		pygame.time.wait(3250)
		self.watch_keypress()
#	}}}

	def transform_height(self,item,width):

		x = item.get_size()[0]
		y = item.get_size()[1]
		ratio = float(y)/float(x)
		return int(width * ratio)

	def transform_width(self,item,height):

		x = item.get_size()[0]
		y = item.get_size()[1]
		ratio = float(x)/float(y)
		return int(height * ratio)

	def test_monster(self,monster,dic,data,log,response=True,n=8,break_when=False):

		miss = 0
		correct_resp = 0
		counter = 0
		sw = Stop_Watch()
		log.set_top('trial_nr\tkey_pressed\tresponse\tresponse_time')
		side = []
		print(data)

		for i in range(data.get_n_trials()):
			self.surface.fill(self.bg_blank)

			trial = data.get_trial()
			image = pygame.image.load(os.path.join(self.path,monster[trial[0]]))

			if trial[2] == '"congruent"':
				correct = 1
			else:
				correct = 0

			self.draw(image,(self.position_center_width(image),self.position_center_height(image)))

			pygame.display.update()
			
			sound = int(trial[1][2]) - 1
			dic[sound]['bla'][random.randint(0,4)].play()
			sw.start()

			key_pressed = False
			press = 0
			pygame.event.clear()

			while True:
				for event in pygame.event.get():
					self.standart_event(event)

					if event.type == MOUSEBUTTONDOWN:
						try:
							if event.button == 1:
								sw.stop()
								press = 0
								key_pressed = True
							if event.button == 3:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				if press == correct and key_pressed:
					log.add([i+1,press,int(press==correct),sw.get_time()])
					if response:
						if correct == 1:
							dic[sound]['pos'][random.randint(0,2)].play()
						else:
							dic[int(bin(sound+1)[-1])]['pos'][random.randint(0,2)].play()
						correct_resp += 1
						counter += 1
						pygame.time.wait(3700)
					else:
						pygame.time.wait(250)
					pygame.event.clear()

					self.surface.fill(self.bg_blank)
					pygame.display.update()
					pygame.time.wait(250)
					break
				if press != correct and key_pressed:
					log.add([i+1,press,int(press==correct),sw.get_time()])
					miss += 1
					counter += 1
					if response:
						if correct == 1:
							dic[sound]['neg'][random.randint(0,2)].play()
						else:
							dic[int(bin(sound+1)[-1:])]['neg'][random.randint(0,2)].play()
						correct_resp -= 1
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

			print('counter: '+str(counter)+' | correct: '+str(correct_resp))
			pygame.time.wait(500)
			if (correct_resp >= 10 or counter >= 30) and break_when:
				break


		return miss

	def blank(self):
		self.surface.fill(self.bg_blank)
		pygame.display.update()

	def draw_mouse_instruction(self,left,right,mouse,resize=True,highlight=None):
		self.blank()

		left = pygame.image.load(os.path.join(self.path,left))
		right = pygame.image.load(os.path.join(self.path,right))

		if highlight == 'l':
			l = 2.1
			r = 3
		elif highlight == 'r':
			l = 3
			r = 2.1
		else:
			l = 3
			r = 3

		if resize:
			left = pygame.transform.scale(left,(self.transform_width(left,int(self.windowheight/l)),int(self.windowheight/l)))
			right = pygame.transform.scale(right,(self.transform_width(right,int(self.windowheight/r)),int(self.windowheight/r)))

		self.surface.blit(left,(int((self.windowwidth/2-left.get_width())/2),int(self.windowheight/9)))
		self.surface.blit(right,(int((self.windowwidth/2-right.get_width())/2 + self.windowwidth/2),int(self.windowheight/9)))
		if mouse != None:
			mouse = pygame.image.load(os.path.join(self.path,mouse))
			mouse = pygame.transform.scale(mouse,(self.transform_width(mouse,int(self.windowheight/3)),int(self.windowheight/3)))
			self.surface.blit(mouse,(int((self.windowwidth-mouse.get_width())/2),int(self.windowheight/2+self.windowheight/9)))
		pygame.display.update()

	def redraw_mouse(self,mouse):
		mouse = pygame.image.load(os.path.join(self.path,mouse))
		mouse = pygame.transform.scale(mouse,(self.transform_width(mouse,int(self.windowheight/3)),int(self.windowheight/3)))
		self.surface.blit(mouse,(int((self.windowwidth-mouse.get_width())/2),int(self.windowheight/2+self.windowheight/9)))
		pygame.display.update()

	def draw_beginning(self,left,right,resize=True):
		l = pygame.image.load(os.path.join(self.path,left))
		r = pygame.image.load(os.path.join(self.path,right))

		if resize:
			l = pygame.transform.scale(l,(self.transform_width(l,int(self.windowheight/2)),int(self.windowheight/2)))
			r = pygame.transform.scale(r,(self.transform_width(r,int(self.windowheight/2)),int(self.windowheight/2)))

		self.blank()
		self.draw_left(l)
		self.draw_right(r)
		pygame.display.update()


class Morse1(Stage):

	def __init__(self,beep=False):
		self.log = Monster_Logger2('morse1')
		Stage.__init__(self,True,title='Morse',)
		self.start('Teil 1')

		self.surface.fill(self.bg_blank)
		pygame.display.update()

		self.load_sound(os.path.join(self.path,'audio/morse1/Instr1.ogg')).play()
		self.blank()
		pygame.time.wait(5000)
		image = pygame.image.load(os.path.join(self.path,'images/morse/dot.tif'))
		self.draw(image,(self.position_center_width(image),self.position_center_height(image)))
		pygame.display.update()
		pygame.time.wait(4300)
		image = pygame.image.load(os.path.join(self.path,'images/morse/dash.tif'))
		self.draw(image,(self.position_center_width(image),self.position_center_height(image)))
		pygame.display.update()
		pygame.time.wait(4200)

		self.play_instruction('audio/morse1/Instr2.ogg')

		self.draw_stuff('images/morse/dot.tif')
		self.stopwatch = Stop_Watch()
		self.stopwatch.start()
		self.play_instruction('audio/morse1/ta.ogg',False)
		pygame.time.wait(500)

		self.surface.fill(self.bg_blank)
		pygame.display.update()
		pygame.time.wait(500)

		self.draw_stuff('images/morse/dash.tif')
		self.play_instruction('audio/morse1/maa.ogg',False)
		pygame.time.wait(500)

		self.surface.fill(self.bg_blank)
		pygame.display.update()
		pygame.time.wait(500)
		self.play_instruction('audio/morse1/Instr3.ogg')

		self.log.add_new_log('learn1')
		self.stuff(Trial_Data('level/data/mor1/learn1.dat'))

		self.load_sound(os.path.join(self.path,'audio/morse1/Instr4.ogg')).play()
		self.blank()
		pygame.time.wait(2000)
		image = pygame.image.load(os.path.join(self.path,'images/morse/dot_dash.tif'))
		self.draw(image,(self.position_center_width(image),self.position_center_height(image)))
		pygame.display.update()
		pygame.time.wait(8500)
		self.draw(pygame.image.load(os.path.join(self.path,'images/morse/show_dot.jpg')))
		pygame.display.update()
		pygame.time.wait(3000)
		self.draw(pygame.image.load(os.path.join(self.path,'images/morse/show_dash.jpg')))
		pygame.display.update()
		pygame.time.wait(3500)
		self.blank()
		pygame.time.wait(500)
		
		self.play_instruction('audio/morse1/Instr5.ogg')

		self.log.add_new_log('learn2')
		self.stuff(Trial_Data('level/data/mor1/learn2.dat'))
		self.play_instruction('audio/morse1/intro_test.ogg')
		self.log.add_new_log('test')
		self.stuff(Trial_Data('level/data/mor1/test.dat'),True)
		self.play_instruction('audio/morse1/quit.ogg')

	def draw_stuff(self,path):
		image = pygame.image.load(os.path.join(self.path,path))
		self.surface.fill(self.bg_blank)
		self.surface.blit(image,(self.position_center_width(image),self.position_center_height(image)))
		pygame.display.update()

	def stuff(self,trialdata,test=False):

		correct = 0

		self.log.set_top('trial\timage\tcorrect\ttime')
		for i in range(trialdata.get_n_trials()):
			if not test and correct >= 10:
				break
			else:
				trial = trialdata.get_trial()
				image = trial[1][1:-1]
	#			self.play_instruction(self.noise)
				pygame.time.wait(500)
				#self.play_instruction('audio/beep.ogg')
				self.draw_stuff(os.path.join('images/morse/',image))
				self.stopwatch.stop()
				time = self.stopwatch.get_time()
				stop = False

				while not stop:
					for event in pygame.event.get():
						self.standart_event(event)
						if event.type == KEYDOWN:
							if event.key == K_RETURN:
								correct += 1
								self.log.add([trial[0],image,int(True),time])
								stop = True
								self.blank()
								pygame.time.wait(500)
							elif event.key == K_SPACE:
								self.log.add([trial[0],image,int(False),time])
								self.blank()
								pygame.time.wait(500)
								if not test:
	#								self.play_instruction(self.noise)
									pygame.time.wait(500)
									self.draw_stuff(os.path.join('images/morse',image))
									self.stopwatch.stop()
									time = self.stopwatch.get_time()
								else:
									stop = True

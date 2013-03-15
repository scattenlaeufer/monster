# -*- coding: utf-8 -*-

#	{{{ import
import pygame, sys, random, os
from PyQt4 import QtGui
from pygame.locals import *
from helpers.log import Monster_Logger, Log_Tester
from helpers.dialog import ProbCodeDialog
from helpers import Stop_Watch, Trial_Data
#	}}}

#	{{{ class Stage
#generic form of a stage. all actual stages should inherit from this

class Stage:

#	{{{ __init__
	def __init__(self,bla=True,neo=False):

#		self.ask_prob_code('monster1_learn')
		app = QtGui.QApplication(sys.argv)
		probDialog = ProbCodeDialog()
		self.prob_code = probDialog.ask()
#		log_tester = Log_Tester(self.prob_code,'monster1_learn')
		
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
		self.surface = pygame.display.set_mode((self.windowwidth,self.windowheight),0,32)
		pygame.display.set_caption('Monster v0.1') 
#		self.toggle_fullscreen()

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

#	{{{ transform_width
	def transform_width(self,item,height):

		x = item.get_size()[0]
		y = item.get_size()[1]
		ratio = float(x)/float(y)
		return int(height * ratio)
#	}}}

#	{{{ test_monster
	def test_monster(self,monster,dic,data,log,response=True,n=8):

		miss = 0
		correct_resp = 0
		sw = Stop_Watch()
		log.set_top('trial_nr\tkey_pressed\tresponse\tresponse_time')
		side = []

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

				if press == correct and key_pressed:
					log.add([i+1,press,int(press==correct),sw.get_time()])
					if response:
						if correct == 1:
							dic[sound]['pos'][random.randint(0,2)].play()
						else:
							dic[int(bin(sound+1)[-1])]['pos'][random.randint(0,2)].play()
						correct_resp += 1
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
					if response:
						dic[int(bin(sound+1)[-1])]['neg'][random.randint(0,2)].play()
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

			pygame.time.wait(500)
#			if correct_resp >= 5:
#				break

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

#	{{{ ask_prob_code
	def ask_prob_code(self,level):
		app = QtGui.QApplication(sys.argv)
		probDialog = ProbCodeDialog()
		self.prob_code = probDialog.ask()
		log_tester = Log_Tester(self.prob_code,level)
#	}}}

#	}}}

#	{{{ Monster1
class Monster1(Stage):

	def __init__(self, prob_code = 'test'):
		Stage.__init__(self,True,True)
#		self.ask_prob_code('monster1_learn')
		self.start('Teil 1')
#		self.play_instruction('audio/intro_begin.ogg')
		monster = {'"pic_M1.bmp"':'images/monster1.jpg','"pic_M2.bmp"':'images/monster2.jpg'}
		
		sound_dic = self.load_monster_sound()

#		self.teach_monster(monster[0],self.load_sound(os.path.join(self.path,'audio/intro_pic_M1.ogg')))
#		self.teach_monster(monster[1],self.load_sound(os.path.join(self.path,'audio/intro_pic_M2.ogg')))
#		self.play_instruction('audio/instr1.ogg')

#		self.play_instruction('audio/intro_train.ogg')

		log = Monster_Logger('monster1_learn',self.prob_code)
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon1/learn.dat'),log,True,10)

		self.play_instruction('audio/intro_test.ogg')

		log = Monster_Logger('monster1_test',self.prob_code)
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon1/test.dat'),log,False,20)

		self.play_instruction('audio/quit.ogg')
		
	def load_monster_sound(self):

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

		return sound_dic
#	}}}

#	{{{ Monster2
class Monster2(Monster1):

	def __init__(self, prob_code = 'test'):
		self.prob_code = prob_code
		Stage.__init__(self,True,True)
		self.start('Teil 2')

		sound_dic = self.load_monster_sound()

		monster = {'"Φ"':'images/li.png','"Ψ"':'images/ka.png'}
#		self.teach_monster(monster[0],self.load_sound(os.path.join(self.path,'audio/intro_sym_M1.ogg')))
#		self.teach_monster(monster[1],self.load_sound(os.path.join(self.path,'audio/intro_sym_M2.ogg')))

#		self.play_instruction('audio/intro_train.ogg')
		log = Monster_Logger('monster2_learn',self.prob_code)
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon2/learn.dat'),log,True,10)

#		self.play_instruction('audio/intro_test.ogg')
		log = Monster_Logger('monster2_test',self.prob_code)
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon2/test.dat'),log,False,20)
		
		self.play_instruction('audio/quit.ogg')
#	}}}

#	{{{ Monster 3

class Monster3(Monster1):

#	{{{ __init__

	def __init__(self,prob_code = 'test'):
		self.prob_code = prob_code
		Stage.__init__(self,True,True)
		self.start('Teil 3')

		log = Monster_Logger('monster3_cookies',self.prob_code)
		cookies = {'"cookie_M1.tif"':self.load_sprite('images/li_cookie.png'),'"cookie_M2.tif"':self.load_sprite('images/ka_cookie.png')}

		top = {'r':self.load_sprite('images/li_g.png'),'l':self.load_sprite('images/ka_r.png')}
		#self.cookie_test(cookies,top,Trial_Data('level/data/mon3/run_1.dat'),log)

		log = Monster_Logger('monster3_monster',self.prob_code)
		monster = {'"pic_M1.tif"':self.load_sprite('images/monster1.jpg'),'"pic_M2.tif"':self.load_sprite('images/monster2.jpg')}
		top = {'r':self.load_sprite('images/li_cookie_g.png'),'l':self.load_sprite('images/ka_cookie_r.png')}
		self.cookie_test(monster,top,Trial_Data('level/data/mon3/run_2.dat'),log)

#	}}}

#	{{{ load_sprite

	def load_sprite(self,path):

		image = pygame.image.load(os.path.join(self.path,path))
		image = pygame.transform.scale(image,(self.transform_width(image,int(self.windowheight/3)),int(self.windowheight/3)))
		return image

#	}}}

#	{{{ cookie_test

	def cookie_test(self,target,top,data,log):
		
		miss = 0
		correct_resp = 0
		sw = Stop_Watch()
		log.set_top('trial_nr\tkey_pressed\tcorrect\tresponse_time')

		for i in range(data.get_n_trials()):

			self.surface.fill(self.bg_blank)
			trial = data.get_trial()
			sprite = target[trial[1]]

			if trial[2] == '"2"':
				correct = 0
			else:
				correct = 1

			self.surface.blit(top['l'],(int((self.windowwidth/2-top['l'].get_width())/2),int(self.windowheight/9)))
			self.surface.blit(top['r'],(int((self.windowwidth/2-top['r'].get_width())/2 + self.windowwidth/2),int(self.windowheight/9)))
			self.surface.blit(sprite,(int((self.windowwidth-sprite.get_width())/2),int(self.windowheight/2+self.windowheight/9)))
			pygame.display.update()
			sw.start()

			key_pressed = False
			press = -1

			while(True):
				for event in pygame.event.get():
					self.standart_event(event)

					if event.type == KEYDOWN:
						try:
							if self.left.find(unichr(event.key)) >= 0:
								sw.stop()
								press = 0
								key_pressed = True
							elif self.right.find(unichr(event.key)) >= 0:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				if key_pressed:
					log.add([i,press,press==correct,sw.get_time()])
					self.surface.fill(self.bg_blank)
					pygame.display.update()
					pygame.time.wait(500)
					break

				self.mainClock.tick(40)

#	}}}

#	}}}

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
	print('Create config.py from defaults.py!')
	from defaults import *
#	}}}


class Stage:
	#generic form of a stage. all actual stages should inherit from this

	def __init__(self,bla=True,neo=False,title='Monster'):

#		self.ask_prob_code('monster1_learn')
		print(RESOLUTION)

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
		self.font1 = pygame.font.Font(None,70)

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

	#	#self.surface = pygame.transform.scale(self.surface,(self.windowwidth,self.windowheight))
	#	#pygame.display.update()

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
		pygame.time.wait(3000)
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


class Monster1(Stage):

	def __init__(self):
		log = Monster_Logger2('monster1')
		Stage.__init__(self,True)
		self.start('Teil 1')
		monster = {'"pic_M1.bmp"':'images/monster1.jpg','"pic_M2.bmp"':'images/monster2.jpg'}
		self.draw_beginning(monster['"pic_M1.bmp"'],monster['"pic_M2.bmp"'])
		self.play_instruction('audio/intro_begin.ogg',False)
		
		sound_dic = self.load_monster_sound()

		self.teach_monster(monster['"pic_M1.bmp"'],self.load_sound(os.path.join(self.path,'audio/intro_pic_M1.ogg')))
		pygame.time.wait(500)
		self.teach_monster(monster['"pic_M2.bmp"'],self.load_sound(os.path.join(self.path,'audio/intro_pic_M2.ogg')))
		pygame.time.wait(500)
		self.teach_monster(monster['"pic_M1.bmp"'],self.load_sound(os.path.join(self.path,'audio/introA_pic_M1.ogg')))
		pygame.time.wait(500)
		self.teach_monster(monster['"pic_M2.bmp"'],self.load_sound(os.path.join(self.path,'audio/introA_pic_M2.ogg')))
		pygame.time.wait(500)
		self.load_sound(os.path.join(self.path,'audio/instr1.ogg')).play()
		self.draw_mouse_instruction(monster['"pic_M1.bmp"'],monster['"pic_M2.bmp"'],None)
		pygame.time.wait(7000)
		self.redraw_mouse('images/maus_g.jpg')
		pygame.time.wait(8000)
		self.redraw_mouse('images/maus_r.jpg')
		pygame.time.wait(8000)
		self.blank()
		pygame.time.wait(3000)

		self.show_monster('images/monster1.jpg',sound_dic[0]['bla'][0],True)
		pygame.time.wait(750)
		self.show_monster('images/monster1.jpg',sound_dic[1]['bla'][0],False)
		pygame.time.wait(750)
		self.show_monster('images/monster2.jpg',sound_dic[1]['bla'][0],True)
		pygame.time.wait(750)
		self.show_monster('images/monster2.jpg',sound_dic[0]['bla'][0],False)
		pygame.time.wait(750)

		self.play_instruction('audio/intro_train.ogg')

		log.add_new_log('learn')
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon1/learn.dat'),log,True,10,break_when=True)

		self.play_instruction('audio/intro_test.ogg')

		log.add_new_log('test')
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon1/test.dat'),log,False,20)

		self.play_instruction('audio/quit.ogg')

	def show_monster(self,monster,sound,green,resize=True):

		self.surface.fill(self.bg_blank)

		monster = pygame.image.load(os.path.join(self.path,monster))
		if resize:
			monster = pygame.transform.scale(monster,(self.transform_width(monster,int(self.windowheight/2)),int(self.windowheight/2)))
		self.draw_left(monster)

		mouse = pygame.image.load(os.path.join(self.path,'images/Maus.jpg'))
		mouse = pygame.transform.scale(mouse,(self.transform_width(mouse,int(self.windowheight/2)),int(self.windowheight/2)))
		self.draw_right(mouse)
		pygame.display.update()
		
		pygame.time.wait(200)
		sound.play()
		pygame.time.wait(700)
		
		if green:
			arrow = pygame.image.load(os.path.join(self.path,'images/arrow_g.png'))
			self.draw(arrow,(970,320))
		else:
			arrow = pygame.image.load(os.path.join(self.path,'images/arrow_r.png'))
			self.draw(arrow,(870,320))
		pygame.time.wait(2000)

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


class Monster2(Monster1):

	def __init__(self):
		log = Monster_Logger2('monster2')
		Stage.__init__(self,True)
		self.start('Teil 2')

		sound_dic = self.load_monster_sound()

		monster = {'"Φ"':'images/li.png','"Ψ"':'images/ka.png'}
		self.teach_monster(monster['"Φ"'],self.load_sound(os.path.join(self.path,'audio/intro_sym_M1.ogg')),False)
		pygame.time.wait(1000)
		self.teach_monster(monster['"Ψ"'],self.load_sound(os.path.join(self.path,'audio/intro_sym_M2.ogg')),False)
		pygame.time.wait(1000)

		self.blank()
		pygame.time.wait(2000)

		self.teach_monster(monster['"Φ"'],self.load_sound(os.path.join(self.path,'audio/introA_sym_M1.ogg')),False)
		pygame.time.wait(1000)
		self.teach_monster(monster['"Ψ"'],self.load_sound(os.path.join(self.path,'audio/introA_sym_M2.ogg')),False)
		pygame.time.wait(500)

		self.load_sound(os.path.join(self.path,'audio/m2/instr2.ogg')).play()
		self.draw_mouse_instruction(monster['"Φ"'],monster['"Ψ"'],None,False)
		pygame.time.wait(7000)
		self.redraw_mouse('images/maus_g.jpg')
		pygame.time.wait(12000)
		self.redraw_mouse('images/maus_r.jpg')
		pygame.time.wait(4000)
		self.blank()
		pygame.time.wait(3000)
		
		self.show_monster('images/li.png',sound_dic[0]['bla'][0],True,False)
		pygame.time.wait(750)
		self.show_monster('images/li.png',sound_dic[1]['bla'][0],False,False)
		pygame.time.wait(750)
		self.show_monster('images/ka.png',sound_dic[1]['bla'][0],True,False)
		pygame.time.wait(750)
		self.show_monster('images/ka.png',sound_dic[0]['bla'][0],False,False)
		pygame.time.wait(750)

		self.play_instruction('audio/intro_train.ogg')
		log.add_new_log('learn')
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon2/learn.dat'),log,True,10,break_when=True)

		self.play_instruction('audio/intro_test.ogg')
		log.add_new_log('test')
		self.test_monster(monster,sound_dic,Trial_Data('level/data/mon2/test.dat'),log,False,20)
		
		self.play_instruction('audio/quit.ogg')


class Monster3(Monster1):

	def __init__(self):
		log = Monster_Logger2('monster3')
		Stage.__init__(self,True)
		self.start('Teil 3')

		self.surface.fill(self.bg_blank)
		self.load_sound(os.path.join(self.path,'audio/m3/instr3.ogg')).play()
		self.draw(pygame.image.load(os.path.join(self.path,'images/m3_1.jpg')))
		pygame.time.wait(10000)
		self.draw(pygame.image.load(os.path.join(self.path,'images/m3_2.jpg')))
		pygame.time.wait(5000)
		self.draw(pygame.image.load(os.path.join(self.path,'images/m3_3.jpg')))
		pygame.time.wait(9500)

		self.surface.fill(self.bg_blank)

		log.add_new_log('cookies')
		cookies = {'"cookie_M1.tif"':self.load_sprite('images/li_cookie.png'),'"cookie_M2.tif"':self.load_sprite('images/ka_cookie.png')}
		top = {'r':self.load_sprite('images/li_g.png'),'l':self.load_sprite('images/ka_r.png')}


		self.load_sound(os.path.join(self.path,'audio/m3/instr4.ogg')).play()
		self.draw_mouse_instruction('images/ka_r.png','images/li_g.png',None,highlight=None)
		pygame.time.wait(2000)
		self.draw_mouse_instruction('images/ka_r.png','images/li_g.png',None,highlight='l')
		pygame.time.wait(2500)
		self.surface.fill(self.bg_blank)
		self.draw_mouse_instruction('images/ka_r.png','images/li_g.png',None,highlight='r')
		pygame.time.wait(5000)
#		self.draw_mouse_instruction('images/ka_r.png','images/li_g.png',None,highlight=None)
#		pygame.time.wait(500)
		self.draw_mouse_instruction('images/ka_r.png','images/li_g.png','images/maus_r.jpg',highlight='l')
		pygame.time.wait(3500)
		self.draw_mouse_instruction('images/ka_r.png','images/li_g.png','images/maus_g.jpg',highlight='r')
		pygame.time.wait(3500)

		self.blank()
		pygame.time.wait(500)

		self.cookie_test(cookies,top,Trial_Data('level/data/mon3/run_1.dat'),log)

		self.load_sound(os.path.join(self.path,'audio/m3/instr5.ogg')).play()
		self.blank()
		pygame.time.wait(3000)
		self.draw_mouse_instruction('images/ka_cookie_r.png','images/li_cookie_g.png','images/monster1.jpg',highlight=None)
		pygame.time.wait(14000)
		
		self.load_sound(os.path.join(self.path,'audio/m3/instr6.ogg')).play()
		self.draw_mouse_instruction('images/ka_cookie_r.png','images/li_cookie_g.png',None,highlight='l')
		pygame.time.wait(4500)
		self.draw_mouse_instruction('images/ka_cookie_r.png','images/li_cookie_g.png',None,highlight='r')
		pygame.time.wait(4500)
		self.draw_mouse_instruction('images/ka_cookie_r.png','images/li_cookie_g.png',None,highlight=None)
		pygame.time.wait(6000)
		self.draw_mouse_instruction('images/ka_cookie_r.png','images/li_cookie_g.png','images/maus_r.jpg',highlight='l')
		pygame.time.wait(2500)
		self.draw_mouse_instruction('images/ka_cookie_r.png','images/li_cookie_g.png','images/maus_g.jpg',highlight='r')
		pygame.time.wait(2500)

		self.blank()
		pygame.time.wait(500)

		self.surface.fill(self.bg_blank)

		log.add_new_log('monster')
		monster = {'"pic_M1.tif"':self.load_sprite('images/monster1.jpg'),'"pic_M2.tif"':self.load_sprite('images/monster2.jpg')}
		top = {'r':self.load_sprite('images/li_cookie_g.png'),'l':self.load_sprite('images/ka_cookie_r.png')}

		self.cookie_test(monster,top,Trial_Data('level/data/mon3/run_2.dat'),log)

		self.play_instruction('audio/m3/end.ogg')

	def load_sprite(self,path):

		image = pygame.image.load(os.path.join(self.path,path))
		image = pygame.transform.scale(image,(self.transform_width(image,int(self.windowheight/3)),int(self.windowheight/3)))
		return image

	def show_stuff(self,top,sprite):
		self.blank()
		self.draw_three_sprites(top,sprite)

		goon = True

		while goon:
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					goon = False

	def draw_three_sprites(self,top,sprite):
		self.surface.blit(top['l'],(int((self.windowwidth/2-top['l'].get_width())/2),int(self.windowheight/9)))
		self.surface.blit(top['r'],(int((self.windowwidth/2-top['r'].get_width())/2 + self.windowwidth/2),int(self.windowheight/9)))
		self.surface.blit(sprite,(int((self.windowwidth-sprite.get_width())/2),int(self.windowheight/2+self.windowheight/9)))
		pygame.display.update()

	def cookie_test(self,target,top,data,log):
		
		miss = 0
		correct_resp = 0
		sw = Stop_Watch()
		log.set_top('trial_nr\tkey_pressed\tresponse\tresponse_time')

		for i in range(data.get_n_trials()):

			self.surface.fill(self.bg_blank)
			trial = data.get_trial()
			sprite = target[trial[1]]

			if trial[2] == '"2"':
				correct = 0
			else:
				correct = 1

			self.draw_three_sprites(top,sprite)
			sw.start()

			key_pressed = False
			press = -1
			pygame.event.clear()

			while(True):
				for event in pygame.event.get():
					self.standart_event(event)

					if event.type == MOUSEBUTTONDOWN:
						try:
							if event.button == 1:
								sw.stop()
								press = 0
								key_pressed = True
							elif event.button == 3:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				if key_pressed:
					log.add([i,press,int(press==correct),sw.get_time()])
					self.surface.fill(self.bg_blank)
					pygame.display.update()
					break

				self.mainClock.tick(40)

			pygame.time.wait(500)


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


class Morse2(Stage):

	def __init__(self):
		self.log = Monster_Logger2('morse2')
		Stage.__init__(self,True,title='Morse')
		self.start('Teil 2')

		self.surface.fill(self.bg_blank)
		pygame.display.update()
		self.play_instruction('audio/morse2/instr1.ogg')

		pygame.time.wait(1000)

		self.play_instruction('audio/intro_train.ogg')

		self.log.add_new_log('learn1')
		self.log.set_top('trail\tcorrect')
		self.morse('ta')
		self.morse('ma')
		self.morse('ma')
		self.morse('ta')
		self.morse('ta')
		self.morse('ma')
		self.morse('ta')
		self.morse('ta')
		self.morse('ta')
		self.morse('ma')

		self.play_instruction('audio/morse2/instr2.ogg')

		self.log.add_new_log('learn2')
		self.log.set_top('trail\tcorrect')
		self.morse('u201')
		self.morse('u202')
		self.morse('u203')
		self.morse('u204')
		self.morse('u205')
		self.morse('u206')
		self.morse('u207')
		self.morse('u208')
		self.morse('u209')
		self.morse('u210')
		self.morse('u211')
		self.morse('u212')

		self.play_instruction('audio/morse2/instr3.ogg')

		self.log.add_new_log('test')
		self.log.set_top('trail\tcorrect')
		self.morse('t01',True)
		self.morse('t02',True)
		self.morse('t03',True)
		self.morse('t04',True)
		self.morse('t05',True)
		self.morse('t06',True)
		self.morse('t07',True)
		self.morse('t08',True)
		self.morse('t09',True)
		self.morse('t10',True)
		self.morse('t11',True)
		self.morse('t12',True)

		self.play_instruction('audio/morse1/quit.ogg')

	def morse(self,trail,test=False):
		goon = True
		self.play_instruction('audio/morse2/'+trail+'.ogg')
		while goon:
			for event in pygame.event.get():
				self.standart_event(event)
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						if not test:
							self.play_instruction('audio/morse2/'+trail+'.ogg')
						else:
							goon = False
						self.log.add([trail,str(False)])
					elif event.key == K_RETURN:
						goon = False
						self.log.add([trail,str(True)])
					elif event.key == K_BACKSPACE:
						self.play_instruction('audio/morse2/'+trail+'.ogg')
						self.log.add([trail,'repeat'])


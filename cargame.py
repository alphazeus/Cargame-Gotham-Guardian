import pygame
import random

pygame.init()

display = pygame.display.Info()
clock= pygame.time.Clock()
screen= pygame.display.set_mode((display.current_w,display.current_h),pygame.FULLSCREEN)

repeat=True
sc=0
def introduction():
	introflag=True
	font1=pygame.font.SysFont(None,100)
	font2=pygame.font.SysFont("comicsansms",60)
	instrfont=pygame.font.SysFont("arial",50)
	screen.fill((255,255,50))
	text1=font1.render("Gotham Guardian",True,(0,128,0))
	text2=font2.render("Story of the fallen Joker",True,(0,128,128))
	text3=font2.render("and his ambulance",True,(0,128,128))
	instr=instrfont.render("Press [SPACE] to proceed to game",True,(0,0,0))
	screen.blit(text1,(display.current_w/8,display.current_h/3))
	screen.blit(text2,(display.current_w/3,display.current_h/2))
	screen.blit(text3,(display.current_w/3,display.current_h/2+70))
	screen.blit(instr,(display.current_w*0.35,display.current_h*0.75))
	pygame.display.flip()
	pygame.time.delay(1000)

	intro=pygame.mixer.Sound('intro.wav')
	intro.play()
	while introflag==True:
		pygame.event.get()
		press=pygame.key.get_pressed()
		if press[pygame.K_SPACE]:
			intro.stop()
			introflag=False

def ending():
	global c
	global repeat
	endflag=True
	font3=pygame.font.SysFont("arial",100)
	font4=pygame.font.SysFont("arial",50)
	font5=pygame.font.SysFont("arial",150)
	screen.fill((255,255,50))
	text4=font3.render("GAME OVER",True,(255,0,0))
	text5=font4.render("Press [SPACE] to retry and 'Esc' to exit",True,(0,0,255))
	text6=font5.render(str(sc),True,(255,0,0))
	screen.blit(text4,(display.current_w/4,display.current_h/3))
	screen.blit(text5,(display.current_w/4,display.current_h/2))
	screen.blit(text6,(display.current_w*0.4,display.current_h*0.6))

	pygame.display.flip()
	ending=pygame.mixer.Sound('gameover.wav')
	ending.play()

	while endflag==True:
		pygame.event.get()
		press=pygame.key.get_pressed()
		if press[pygame.K_SPACE]:
			repeat=True
			endflag=False
		if press[pygame.K_ESCAPE]:
			repeat=False
			endflag=False
	return repeat
def main():
	global sc
	sc=0
	c=0
	car1x=carrandx()
	car1y=0
	gameover=False
	carx = display.current_w/2
	cary = display.current_h*0.70

	crash=pygame.mixer.Sound('crash.wav')
	pygame.mixer.music.load('ambulancesound.mp3')
	pygame.mixer.music.play(-1)

	ambulance=pygame.image.load('ambulance.jpg')
	ambulance=pygame.transform.scale(ambulance,(int(display.current_w*0.05),int(display.current_h*0.2)))
	car1=pygame.image.load('object.jpg')
	car1=pygame.transform.scale(car1,(int(display.current_w*0.05),int(display.current_h*0.2)))
	car2=pygame.image.load('object1.jpg')
	car2=pygame.transform.scale(car2,(int(display.current_w*0.05),int(display.current_h*0.2)))
	car3=pygame.image.load('object2.jpg')
	car3=pygame.transform.scale(car3,(int(display.current_w*0.05),int(display.current_h*0.2)))
	car4=pygame.image.load('object3.jpg')
	car4=pygame.transform.scale(car4,(int(display.current_w*0.05),int(display.current_h*0.2)))
	car5=pygame.image.load('object4.jpg')
	car5=pygame.transform.scale(car5,(int(display.current_w*0.05),int(display.current_h*0.2)))

	while not gameover:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				gameover=True

		press=pygame.key.get_pressed()
		if press[pygame.K_UP]: cary -=5
		if press[pygame.K_DOWN]: cary +=5
		if press[pygame.K_LEFT]: carx -=5
		if press[pygame.K_RIGHT]: carx +=5

		if press[pygame.K_ESCAPE]:gameover=True

		carselect={1:car1,2:car2,3:car3,4:car4,5:car5}.get(int(sc/50)+1,car5)

		screen.fill((255,255,255))
		car1y+=3*int(sc/50+1)
		if(car1y>=display.current_h):
			car1y=0
			car1x=carrandx()

		screen.blit(carselect,(car1x,car1y))	
		pygame.draw.rect(screen,(255,0,0),pygame.Rect(0,0,display.current_w*.15,display.current_h))
		pygame.draw.rect(screen,(255,0,0),pygame.Rect(display.current_w*0.85,0,display.current_w*.15,display.current_h))
		pygame.draw.rect(screen,(255,0,0),pygame.Rect(0,0,display.current_w,display.current_h*0.05))
		pygame.draw.rect(screen,(255,0,0),pygame.Rect(0,display.current_h*0.95,display.current_w,display.current_h*0.05))
		screen.blit(ambulance,(carx,cary))
		showscores(sc)

		c+=1
		if c>=10:
			sc+=1
			c=0
		pygame.display.flip()
		gameover=testcrash(carx,cary,int(display.current_w*0.05),int(display.current_h*0.2),car1x,car1y,int(display.current_w*0.05),int(display.current_h*0.2))

		if carx<=display.current_w*.15 or cary<=display.current_h*0.05:
			crash.play()
			pygame.time.delay(400)
			gameover=True
		
		if carx>=(display.current_w*.80) or cary>=display.current_h*0.75:
			crash.play()
			pygame.time.delay(400)
			gameover=True

		if gameover==True:
			pygame.mixer.music.stop()
		clock.tick(60)


def complete():
	pygame.quit()
	quit()	

def showscores(c):
	scorefont=pygame.font.SysFont("arial",40)
	scorehead=scorefont.render("Score",True,(255,255,255))
	score = scorefont.render(str(c),True,(255,255,255))
	level=scorefont.render("LEVEL",True,(255,255,255))
	levelno=scorefont.render(str(int(c/50)+1),True,(255,255,255))
	screen.blit(scorehead,(display.current_w*0.03,display.current_h*0.1))
	screen.blit(score,(display.current_w*0.03,display.current_h*0.2))
	screen.blit(level,(display.current_w*0.9,display.current_h*0.1))
	screen.blit(levelno,(display.current_w*0.9,display.current_h*0.2))

def carrandx():
	return random.randint(int(display.current_w*0.15),int(display.current_w*0.85))

def testcrash(carx,cary,carw,carh,car1x,car1y,car1w,car1h):
	if cary<car1y+car1h and cary>car1y or cary+carh<car1y+car1h and cary+carh>car1y:
		if carx>car1x and carx<car1x+car1w or carx+carw>car1x and carx+carw<car1x+car1w:
			return True
	

	return False
while True:
	if repeat==True:
		introduction()
		main()
		repeat=ending()
	else:
		complete()


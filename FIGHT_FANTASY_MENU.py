import sys,pygame
from pygame.locals import QUIT,KEYDOWN,K_UP,K_DOWN,K_RETURN,MOUSEBUTTONDOWN
pygame.init()
pygame.display.set_caption('FIGHT FANTASY - Menu')
WIDTH,HEIGHT=626,511
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
FPS=60
CLOCK=pygame.time.Clock()
SKY=pygame.Color('#87CEEB')
GRASS=pygame.Color('#4CAF50')
TREE_TRUNK=pygame.Color('#5D4037')
TREE_LEAF=pygame.Color('#2E7D32')
TREE_HIGHLIGHT=pygame.Color('#4CAF50')
BUSH_DARK=pygame.Color('#1B5E20')
BUSH_LIGHT=pygame.Color('#2E7D32')
WHITE=pygame.Color('#FFFFFF')
BLACK=pygame.Color('#000000')
GRAY=pygame.Color('#4B5563')
PURPLE=pygame.Color('#7C3AED')
OVERLAY=0,0,0,180
PIXEL=8
TITLE_FONT=pygame.font.SysFont('Arial',72,bold=True)
BUTTON_FONT=pygame.font.SysFont('Arial',32,bold=True)
SECTION_FONT=pygame.font.SysFont('Arial',28,bold=True)
TEXT_FONT=pygame.font.SysFont('Arial',20)
FOOTER_FONT=pygame.font.SysFont('Arial',18)
buttons=[{'label':'PLAY GAME','rect':None},{'label':'HOW TO PLAY','rect':None},{'label':'QUIT','rect':None}]
selected_index=0
def draw_tree(surface,x,y):
	def rect(px,py,w,h,color):surface.fill(color,pygame.Rect(int(px),int(py),int(w),int(h)))
	rect(x-PIXEL,y,PIXEL*2,PIXEL*6,TREE_TRUNK);rect(x-PIXEL*3,y-PIXEL*2,PIXEL*6,PIXEL*2,TREE_LEAF);rect(x-PIXEL*4,y-PIXEL*4,PIXEL*8,PIXEL*2,TREE_LEAF);rect(x-PIXEL*3,y-PIXEL*6,PIXEL*6,PIXEL*2,TREE_LEAF);rect(x-PIXEL*2,y-PIXEL*5,PIXEL*2,PIXEL,TREE_HIGHLIGHT);rect(x+PIXEL,y-PIXEL*3,PIXEL,PIXEL,TREE_HIGHLIGHT)
def draw_bush(surface,x,y):
	def rect(px,py,w,h,color):surface.fill(color,pygame.Rect(int(px),int(py),int(w),int(h)))
	rect(x-PIXEL*2,y,PIXEL*4,PIXEL*2,BUSH_DARK);rect(x-PIXEL,y-PIXEL,PIXEL*2,PIXEL,BUSH_LIGHT)
def draw_cloud(surface,x,y):
	def rect(px,py,w,h,color):surface.fill(color,pygame.Rect(int(px),int(py),int(w),int(h)))
	rect(x,y,PIXEL*3,PIXEL,WHITE);rect(x-PIXEL,y+PIXEL,PIXEL*5,PIXEL,WHITE);rect(x,y+PIXEL*2,PIXEL*3,PIXEL,WHITE)
def create_background_surface():surf=pygame.Surface((WIDTH,HEIGHT));surf.fill(SKY);grass_height=int(HEIGHT*.4);surf.fill(GRASS,rect=pygame.Rect(0,int(HEIGHT*.6),WIDTH,grass_height));ground=int(HEIGHT*.6);draw_tree(surf,WIDTH*.15,ground-PIXEL*6);draw_tree(surf,WIDTH*.35,ground-PIXEL*5);draw_tree(surf,WIDTH*.65,ground-PIXEL*7);draw_tree(surf,WIDTH*.85,ground-PIXEL*6);draw_bush(surf,WIDTH*.25,ground);draw_bush(surf,WIDTH*.55,ground);draw_bush(surf,WIDTH*.75,ground);draw_cloud(surf,WIDTH*.2,HEIGHT*.15);draw_cloud(surf,WIDTH*.6,HEIGHT*.25);draw_cloud(surf,WIDTH*.8,HEIGHT*.1);return surf
BACKGROUND=create_background_surface()
def how_to_play_screen():
	running=True
	while running:
		SCREEN.blit(BACKGROUND,(0,0));overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA);overlay.fill((0,0,0,180));SCREEN.blit(overlay,(0,0));y=10;sections=[(' Controls:',['Click on the hero to attack the selected enemy','Click enemies to attack in battle','select A to attack','select H to heal']),(' Combat:',['Turn-based combat system','Each character has unique abilities','Strategic positioning matters']),(' Objective:',['Defeat all enemies to win','Protect your team from defeat','Use tactics to survive'])]
		for(title,lines)in sections:
			section_surf=SECTION_FONT.render(title,True,WHITE);SCREEN.blit(section_surf,(40,y));y+=40
			for line in lines:line_surf=TEXT_FONT.render(line,True,WHITE);SCREEN.blit(line_surf,(60,y));y+=30
			y+=20
		back_rect=pygame.Rect(WIDTH-180,HEIGHT-70,140,45);pygame.draw.rect(SCREEN,PURPLE,back_rect,border_radius=10);back_text=BUTTON_FONT.render('Back',True,WHITE);text_rect=back_text.get_rect(center=back_rect.center);SCREEN.blit(back_text,text_rect);pygame.display.flip()
		for event in pygame.event.get():
			if event.type==QUIT:pygame.quit();sys.exit()
			elif event.type==MOUSEBUTTONDOWN:
				if back_rect.collidepoint(event.pos):running=False
			elif event.type==KEYDOWN:
				if event.key==K_RETURN:running=False
def run_menu(start_game_callback=None):
	global selected_index;BUTTON_WIDTH=300;BUTTON_HEIGHT=60;BUTTON_GAP=20
	def layout_buttons():
		menu_center_x=WIDTH//2;menu_top_y=int(HEIGHT*.3);current_y=menu_top_y+70
		for button in buttons:button['rect']=pygame.Rect(menu_center_x-BUTTON_WIDTH//2,current_y,BUTTON_WIDTH,BUTTON_HEIGHT);current_y+=BUTTON_HEIGHT+BUTTON_GAP
	while True:
		layout_buttons();SCREEN.blit(BACKGROUND,(0,0));title_surface=TITLE_FONT.render('FIGHT FANTASY',True,WHITE);title_x=WIDTH//2-title_surface.get_width()//2;SCREEN.blit(title_surface,(title_x,30))
		for(i,button)in enumerate(buttons):color=PURPLE if i==selected_index else GRAY;pygame.draw.rect(SCREEN,color,button['rect'],border_radius=12);text_surface=BUTTON_FONT.render(button['label'],True,WHITE);text_x=button['rect'].x+(BUTTON_WIDTH-text_surface.get_width())//2;text_y=button['rect'].y+(BUTTON_HEIGHT-text_surface.get_height())//2;SCREEN.blit(text_surface,(text_x,text_y))
		footer_surface=FOOTER_FONT.render('v1.0.0 | © 2025',True,WHITE);SCREEN.blit(footer_surface,(WIDTH//2-footer_surface.get_width()//2,HEIGHT-30));pygame.display.flip()
		for event in pygame.event.get():
			if event.type==QUIT:return False
			elif event.type==KEYDOWN:
				if event.key==K_UP:selected_index=(selected_index-1)%len(buttons)
				elif event.key==K_DOWN:selected_index=(selected_index+1)%len(buttons)
				elif event.key==K_RETURN:
					if buttons[selected_index]['label']=='PLAY GAME':
						if start_game_callback:
							result=start_game_callback()
							if not result:return False
					elif buttons[selected_index]['label']=='HOW TO PLAY':how_to_play_screen()
					elif buttons[selected_index]['label']=='QUIT':return False
			elif event.type==MOUSEBUTTONDOWN:
				for(i,button)in enumerate(buttons):
					if button['rect'].collidepoint(event.pos):
						if button['label']=='PLAY GAME':
							if start_game_callback:
								result=start_game_callback()
								if not result:return False
						elif button['label']=='HOW TO PLAY':how_to_play_screen()
						elif button['label']=='QUIT':return False
		CLOCK.tick(FPS)
if __name__=='__main__':run_menu()





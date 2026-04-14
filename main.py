import sys,random,os,pygame
from movement import load_animations
pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_PATH = os.path.join(BASE_DIR, 'assets', 'Sound effects and music')
PUNCH_SFX=pygame.mixer.Sound(os.path.join(SOUND_PATH,'player_punch.wav'))
ZOMBIE_PUNCH_SFX=pygame.mixer.Sound(os.path.join(SOUND_PATH,'zombie_punch.wav'))
DYING_GIRL_SFX=pygame.mixer.Sound(os.path.join(SOUND_PATH,'dying_girl.wav'))
DYING_GUY_SFX=pygame.mixer.Sound(os.path.join(SOUND_PATH,'dying_guy.wav'))
DYING_ROBOT_SFX=pygame.mixer.Sound(os.path.join(SOUND_PATH,'dying_robot.wav'))
DYING_ZOMBIE_SFX=pygame.mixer.Sound(os.path.join(SOUND_PATH,'dying_zombie.wav'))
DYING_ZOMBIE_SFX.set_volume(.5)
BG_MUSIC_FILE=os.path.join(SOUND_PATH,'Music.wav')
pygame.mixer.music.load(BG_MUSIC_FILE)
pygame.mixer.init()
WIDTH,HEIGHT=626,511
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Fight Fantasy')
CLOCK=pygame.time.Clock()
FONT=pygame.font.SysFont('arial',20)
BIG_FONT=pygame.font.SysFont('arial',28,bold=True)
WHITE=255,255,255
BLACK=0,0,0
GREY=80,80,80
RED=200,60,60
GREEN=60,200,100
BLUE=60,120,200
YELLOW=240,210,60
ASSET_DIR=os.path.join(BASE_DIR, 'assets')
#ASSET_DIR='assets' #use for mac/linux
animations=load_animations(ASSET_DIR)
BG_IMAGE=pygame.image.load(os.path.join(ASSET_DIR,'bg.png'))
def draw_background(surface):surface.blit(BG_IMAGE,(0,0))
class Unit:
	def __init__(self,name,team,center_pos,color,profession,animation_key,move_speed=3.,hero_index=None):
		self.name=name;self.team=team;self.center_pos=center_pos;self.home_pos=center_pos;self.color=color;self.profession=profession;self.animation=animations[animation_key];self.move_speed=move_speed;self.radius=36;self.anim_state='stand';self.anim_start_ms=0;self.move_target=None;self.hero_index=hero_index
		if profession=='Warrior':self.max_hp=100;self.hp=self.max_hp;self.attack_damage=30,40;self.defense=random.randint(3,5)
		elif profession=='Tank':self.max_hp=100;self.hp=self.max_hp;self.attack_damage=30,40;self.defense=random.randint(5,10)
	@property
	def alive(self):return self.hp>0
	def rect(self):x,y=self.center_pos;return pygame.Rect(x-self.radius,y-self.radius,self.radius*2,self.radius*2)
	def play_animation(self,state,now_ms):
		if self.anim_state!=state:self.anim_state=state;self.anim_start_ms=now_ms
	def start_move_to(self,target_pos,now_ms):self.move_target=target_pos;self.play_animation('run',now_ms)
	def update_movement(self,now_ms):
		if self.move_target is None:return False
		dx=self.move_target[0]-self.center_pos[0];dy=self.move_target[1]-self.center_pos[1];dist=(dx*dx+dy*dy)**.5
		if dist<self.move_speed:self.center_pos=self.move_target;self.move_target=None;self.play_animation('stand',now_ms);return True
		self.center_pos=self.center_pos[0]+dx/dist*self.move_speed,self.center_pos[1]+dy/dist*self.move_speed;return False
	def draw(self,surface,is_active=False):
		x,y=self.center_pos;now_ms=pygame.time.get_ticks();image=self.animation.get_frame(self.anim_state,now_ms-self.anim_start_ms);img_rect=image.get_rect(center=(x,y));surface.blit(image,img_rect)
		if self.alive:bar_w,bar_h=80,10;bar_x,bar_y=x-bar_w//2,y-self.radius-18;pygame.draw.rect(surface,BLACK,(bar_x-1,bar_y-1,bar_w+2,bar_h+2));hp_ratio=max(.0,self.hp/self.max_hp);hp_color=GREEN if hp_ratio>.5 else YELLOW if hp_ratio>.25 else RED;pygame.draw.rect(surface,hp_color,(bar_x,bar_y,int(bar_w*hp_ratio),bar_h));hp_text=f"{self.hp}/{self.max_hp}";hp_surf=FONT.render(hp_text,True,WHITE);hp_rect=hp_surf.get_rect(midtop=(x,bar_y+bar_h+2));surface.blit(hp_surf,hp_rect);name_surf=FONT.render(self.name,True,WHITE);name_rect=name_surf.get_rect(center=(x,y+self.radius+16));surface.blit(name_surf,name_rect)
	def take_damage(self,damage):
		if isinstance(damage,tuple):actual_damage=random.randint(damage[0],damage[1])
		else:actual_damage=damage
		self.hp=max(0,self.hp-actual_damage)
		if self.hp==0:
			if self.hero_index==1:DYING_GIRL_SFX.play(maxtime = 2000)
			elif self.hero_index==2:DYING_GUY_SFX.play()
			elif self.hero_index==3:DYING_ROBOT_SFX.play()
			else:DYING_ZOMBIE_SFX.play()
	def heal(self,heal_amount=10):self.hp=min(self.max_hp,self.hp+heal_amount);self.play_animation('stand',pygame.time.get_ticks())
class SpriteManager:
	def __init__(self,root_dir,scale_to=(100,100)):self.root_dir=root_dir;self.scale_to=scale_to;self.idle_frames=self._load_numbered_frames(os.path.join(root_dir,'Walking','Separate Sp'),'walk',1,1);self.walk_frames=self._load_numbered_frames(os.path.join(root_dir,'Walking','Separate Sp'),'walk',1,10);self.attack_frames=self._load_numbered_frames(os.path.join(root_dir,'Attack 1','Separate Sp'),'attack',1,10);self.dead_frames=self._load_numbered_frames(os.path.join(root_dir,'Dead','Separate Sp'),'dead',1,9)
	def _load_numbered_frames(self,folder_path,prefix,start,end):
		frames=[]
		for i in range(start,end+1):
			fname=f"{prefix} ({i}).png";fpath=os.path.join(folder_path,fname)
			if os.path.exists(fpath):frames.append(self._load_image(fpath))
		return frames if frames else[]
	def _load_image(self,path):
		img=pygame.image.load(path).convert_alpha()
		if self.scale_to:img=pygame.transform.smoothscale(img,self.scale_to)
		return img
	def get_image(self,state,elapsed_ms):
		frames=[];frame_duration=80;loop=True
		if state=='dead':frames=self.dead_frames;loop=False
		elif state=='attack':frames=self.attack_frames;loop=False
		elif state=='walk':frames=self.walk_frames
		else:frames=self.idle_frames
		if not frames:surf=pygame.Surface(self.scale_to,pygame.SRCALPHA);return surf,False
		frame_count=len(frames);idx=elapsed_ms//frame_duration%frame_count;finished=False
		if not loop:
			total_frames=elapsed_ms//frame_duration
			if total_frames>=frame_count:idx=frame_count-1;finished=True
			else:idx=total_frames
		return frames[int(idx)],finished
class Battle:
	def __init__(self):self.state='playing';self.turn_index=0;self.turn_order=[];self.ai_action_due_ms=None;self.message='Player turn: press A to attack or H to heal';self.player_team=[];self.ai_team=[];self.action_state=None;self.action_attacker=None;self.action_target=None;self.action_type=None;self.selected_unit=None;self.init_teams()
	def init_teams(self):
		self.player_team=form_player_team_in_game();self.ai_team=form_ai_team();pygame.mixer.music.play(-1);self.turn_order=[]
		for(p,a) in zip(self.player_team,self.ai_team):self.turn_order.append(p);self.turn_order.append(a)
		self.turn_index=0;self.state='playing';self.ai_action_due_ms=None;self.message='Player turn: press A to attack or H to heal'
	def current_unit(self):
		if not self.turn_order:return
		start=self.turn_index
		for _ in range(len(self.turn_order)):
			unit=self.turn_order[self.turn_index%len(self.turn_order)]
			if unit.alive:return unit
			self.turn_index+=1
	def next_turn(self):
		self.turn_index=(self.turn_index+1)%len(self.turn_order);self.ai_action_due_ms=None;self.player_team=[u for u in self.player_team if u.alive];self.ai_team=[u for u in self.ai_team if u.alive];self.turn_order=[u for u in self.turn_order if u.alive]
		if not self.ai_team:self.state='victory';self.message='Victory! Press R to restart';pygame.mixer.music.stop();return
		if not self.player_team:self.state='defeat';self.message='Defeat! Press R to restart';pygame.mixer.music.stop();return
		unit=self.current_unit()
		if unit is None:return
		if unit.team=='player':self.message='Player turn: press A to attack or H to heal'
		else:self.message='AI turn...'
	def get_enemies(self,unit):return self.ai_team if unit.team=='player'else self.player_team
	def start_attack_action(self,attacker,target):
		if attacker is None or target is None or not attacker.alive or not target.alive:return
		now_ms=pygame.time.get_ticks();dx=target.center_pos[0]-attacker.center_pos[0];distance=80
		if dx>0:attack_pos=target.center_pos[0]-distance,target.center_pos[1]
		else:attack_pos=target.center_pos[0]+distance,target.center_pos[1]
		self.action_state='moving';self.action_attacker=attacker;self.action_target=target;attacker.start_move_to(attack_pos,now_ms)
	def update_action(self,now_ms):
		if self.action_state is None:return
		if self.action_state=='moving':
			reached=self.action_attacker.update_movement(now_ms)
			if reached:self.action_state='attacking';self.action_attacker.play_animation('attack',now_ms)
		elif self.action_state=='attacking':
			elapsed=now_ms-self.action_attacker.anim_start_ms
			if self.action_attacker.team=='player':
				if elapsed in range(100,120)or elapsed in range(300,320)or elapsed in range(500,520):PUNCH_SFX.play()
			elif elapsed in range(200,220)or elapsed in range(400,420)or elapsed in range(600,620):ZOMBIE_PUNCH_SFX.play()
			if elapsed>800:
				base_damage=random.randint(*self.action_attacker.attack_damage);damage=base_damage-self.action_target.defense+random.randint(-5,10);damage=max(0,damage);self.action_target.take_damage(damage)
				if not self.action_target.alive:self.action_target.play_animation('dead',now_ms)
				self.action_state='returning';self.action_attacker.start_move_to(self.action_attacker.home_pos,now_ms)
		elif self.action_state=='returning':
			reached=self.action_attacker.update_movement(now_ms)
			if reached:self.action_attacker.play_animation('stand',now_ms);self.action_state=None;self.action_attacker=None;self.action_target=None;self.next_turn()
	def handle_player_action(self,action_type):
		if self.state!='playing'or self.action_state is not None:return
		if self.selected_unit is None or not self.selected_unit.alive:self.message='Select a character first!';return
		if self.selected_unit.team!='player':return
		if action_type=='heal':self.selected_unit.heal();self.selected_unit=None;self.next_turn()
		elif action_type=='attack':self.action_type='attack';self.message='Select target to attack'
	def handle_player_click(self,mouse_pos):
		if self.state!='playing'or self.action_state is not None:return
		for unit in self.player_team:
			if unit.alive and unit.rect().collidepoint(mouse_pos):self.selected_unit=unit;self.message='Press A to attack or H to heal';return
		if self.selected_unit and self.action_type=='attack':
			for enemy in self.get_enemies(self.selected_unit):
				if enemy.alive and enemy.rect().collidepoint(mouse_pos):self.start_attack_action(self.selected_unit,enemy);self.action_type=None;self.selected_unit=None;break
	def update_ai(self,now_ms):
		if self.state!='playing'or self.action_state is not None:return
		unit=self.current_unit()
		if unit is None or unit.team!='ai'or not unit.alive:return
		if self.ai_action_due_ms is None:self.ai_action_due_ms=now_ms+600;return
		if now_ms<self.ai_action_due_ms:return
		enemies=[e for e in self.get_enemies(unit)if e.alive]
		if not enemies:return
		target=min(enemies,key=lambda e:e.hp);self.start_attack_action(unit,target);self.ai_action_due_ms=None
	def draw(self,surface):
		draw_background(surface);active=self.current_unit();highlight_rects=[]
		if self.selected_unit and self.selected_unit.alive:pygame.draw.rect(surface,BLUE,self.selected_unit.rect(),2)
		if self.state=='playing'and self.selected_unit and self.action_type=='attack':highlight_rects=[e.rect()for e in self.get_enemies(self.selected_unit)if e.alive]
		for unit in self.player_team+self.ai_team:unit.draw(surface,unit==active)
		for rect in highlight_rects:pygame.draw.rect(surface,YELLOW,rect,2)
		if self.state in['victory','defeat']:message_surf=BIG_FONT.render(self.message,True,WHITE);message_rect=message_surf.get_rect(center=(WIDTH//2,HEIGHT//2));surface.blit(message_surf,message_rect)
def form_player_team_in_game():
	player_team=[];professions=['Warrior','Tank'];input_name='';selected_profession=0
	while len(player_team)<3:
		SCREEN.fill(BLACK);title_surf=BIG_FONT.render(f"Form Unit {len(player_team)+1}",True,WHITE);title_rect=title_surf.get_rect(center=(WIDTH//2,50));SCREEN.blit(title_surf,title_rect);name_surf=FONT.render(f"Name: {input_name}",True,WHITE);name_rect=name_surf.get_rect(center=(WIDTH//2,150));SCREEN.blit(name_surf,name_rect)
		for(i,profession)in enumerate(professions):color=GREEN if i==selected_profession else WHITE;prof_surf=FONT.render(profession,True,color);prof_rect=prof_surf.get_rect(center=(WIDTH//2,250+i*50));SCREEN.blit(prof_surf,prof_rect)
		instructions=['Type name and press ENTER to confirm.','Use UP/DOWN to select profession.','Press SPACE to confirm unit.']
		for(i,instruction)in enumerate(instructions):instr_surf=FONT.render(instruction,True,GREY);instr_rect=instr_surf.get_rect(center=(WIDTH//2,400+i*20));SCREEN.blit(instr_surf,instr_rect)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:pygame.quit();sys.exit()
			elif event.type==pygame.KEYDOWN:
				if event.key==pygame.K_RETURN:
					if input_name.strip():0
				elif event.key==pygame.K_BACKSPACE:input_name=input_name[:-1]
				elif event.key==pygame.K_UP:selected_profession=(selected_profession-1)%len(professions)
				elif event.key==pygame.K_DOWN:selected_profession=(selected_profession+1)%len(professions)
				elif event.key==pygame.K_SPACE:
					if input_name.strip():profession=professions[selected_profession];unit=Unit(name=input_name.strip(),team='player',center_pos=(150,100+len(player_team)*120),color=BLUE,profession=profession,animation_key=f"hero{len(player_team)+1}",hero_index=len(player_team)+1);player_team.append(unit);input_name=''
				elif event.unicode.isprintable():input_name+=event.unicode
	return player_team
def form_ai_team():
	ai_team=[];professions=['Warrior','Tank'];ai_names=['Enemy1','Enemy2','Enemy3']
	for(i,name)in enumerate(ai_names):profession=random.choice(professions);unit=Unit(name=name,team='ai',center_pos=(WIDTH-150,100+i*120),color=RED,profession=profession,animation_key=f"enemy{i+1}");unit.attack_damage=25,35;ai_team.append(unit)
	return ai_team
def main():
	global SCREEN;SCREEN=pygame.display.set_mode((WIDTH,HEIGHT));pygame.display.set_caption('Fight Fantasy');battle=Battle();running=True
	while running:
		now_ms=pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:running=False;return False
			elif event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:return True
				elif event.key==pygame.K_r:battle.init_teams();battle.state='playing'
				elif event.key==pygame.K_h:battle.handle_player_action('heal')
				elif event.key==pygame.K_a:battle.handle_player_action('attack')
			elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:battle.handle_player_click(event.pos)
		battle.update_action(now_ms);battle.update_ai(now_ms);battle.draw(SCREEN);pygame.display.flip();CLOCK.tick(60)
	return True
if __name__=='__main__':
	from FIGHT_FANTASY_MENU import run_menu;running=True
	while running:
		result=run_menu(start_game_callback=main)
		if not result:running=False
	pygame.quit();sys.exit()
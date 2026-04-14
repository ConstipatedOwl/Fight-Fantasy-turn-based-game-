import os,pygame
class Animation:
	def __init__(self,folder_path,scale_to=(100,100)):self.folder_path=folder_path;self.scale_to=scale_to;self.animations={'stand':self._load_frames('stand'),'run':self._load_frames('run',3),'attack':self._load_frames('attack',3)};self.frame_duration=100
	def _load_frames(self,prefix,count=1):
		frames=[]
		for i in range(1,count+1):
			file_name=f"{prefix}{i}.png"if count>1 else f"{prefix}.png";file_path=os.path.join(self.folder_path,file_name)
			if os.path.exists(file_path):
				img=pygame.image.load(file_path).convert_alpha()
				if self.scale_to:img=pygame.transform.smoothscale(img,self.scale_to)
				frames.append(img)
		return frames
	def get_frame(self,state,elapsed_ms):
		frames=self.animations.get(state,[])
		if not frames:return pygame.Surface(self.scale_to,pygame.SRCALPHA)
		frame_count=len(frames);frame_index=elapsed_ms//self.frame_duration%frame_count;return frames[frame_index]
def load_animations(asset_dir):return{'hero1':Animation(os.path.join(asset_dir,'fa')),'hero2':Animation(os.path.join(asset_dir,'mp')),'hero3':Animation(os.path.join(asset_dir,'r')),'enemy1':Animation(os.path.join(asset_dir,'z')),'enemy2':Animation(os.path.join(asset_dir,'z')),'enemy3':Animation(os.path.join(asset_dir,'z'))}
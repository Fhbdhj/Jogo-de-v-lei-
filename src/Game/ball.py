# encoding : UTF-8

from pygame import Vector3
import pygame as pg

from Engine.Display import debug3D_utils
from Engine.Display.scalable_sprite import ScalableSprite
from Engine.Collisions import SphereCollider
from Settings.general_settings import *
import Engine


class Ball(ScalableSprite):
	def __init__(self, position=None, radius=0.5, sprite_groups=[]):
		ScalableSprite.__init__(self, 1.0, *sprite_groups)
		self.radius = radius
		self.acceleration = Vector3()
		self.velocity = Vector3()
		self._position = Vector3(position) if position is not None else Vector3()
		self.previous_position = Vector3(self._position)
		self.collider = SphereCollider(position, radius)
		
		self.is_colliding_ground = False
		self.is_colliding_net = False
		self.is_colliding_character = False
		
		self.will_be_served = False
		
		# sprite
		#	real sprite
		self.raw_rect = pg.Rect(0, 0, 0, 0)
		self.raw_image = pg.image.load("../assets/sprites/ball.png").convert_alpha()

		# 	debug
		self.dbg_rect_shadow = pg.Rect(0, 0, 0, 0)
		self.dbg_rect = pg.Rect(0, 0, 0, 0)
		
		# game rules
		self._current_team_touches = []

	def add_team_touch(self, character):
		team_id = character.team.id
		if len(self._current_team_touches) == 0 or self._current_team_touches[-1] != team_id:
			self._current_team_touches = [team_id]
		else:
			self._current_team_touches.append(team_id)
			if len(self._current_team_touches) > MAX_TOUCHES_NB:
				ge_ticks = Engine.GameEngine.get_instance().get_running_ticks()
				# TODO : create form in settings for dict to pass in post(Event)
				d = {"faulty_team": team_id, "rule_type": RuleType.TOUCHES_NB, "time_stamp": ge_ticks}
				pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))
				
	def manage_touch_ground_rule(self):
		if len(self._current_team_touches) == 0:
			faulty_team_id = None
		else:
			last_team_id = self._current_team_touches[-1]
			faulty_team_id = last_team_id
			
			# if ball pos in good area for last team --> last team wins
			game_engine = Engine.game_engine.GameEngine.get_instance()
			court = game_engine.court
			if (self.position.y < 0 and last_team_id == TeamId.RIGHT) or (self.position.y > 0 and last_team_id == TeamId.LEFT):
				if abs(self.position.x) < court.h / 2 and abs(self.position.y) < court.w / 2:
					faulty_team_id = TeamId.LEFT if last_team_id == TeamId.RIGHT else TeamId.RIGHT

		ge_ticks = Engine.GameEngine.get_instance().get_running_ticks()
		d = {"faulty_team": faulty_team_id, "rule_type": RuleType.GROUND, "time_stamp": ge_ticks}
		pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))
		
	def check_if_out_of_bounds(self):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		court = game_engine.court
		if abs(self.position.x) > 1.5 * court.h / 2 or abs(self.position.y) > 1.5 * court.w / 2:
			faulty_team_id = self._current_team_touches[-1] if len(self._current_team_touches) > 0 else None
			ge_ticks = Engine.GameEngine.get_instance().get_running_ticks()
			d = {"faulty_team": faulty_team_id, "rule_type": RuleType.OUT_OF_BOUNDS, "time_stamp": ge_ticks}
			pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))

	def check_if_under_net(self):
		game_engine = Engine.game_engine.GameEngine.get_instance()
		court = game_engine.court

		# check ball height
		if self.position.z + self.radius < court.net_z1:
			# check if ball crossed net plane
			if (self.previous_position.y < 0 and self.position.y > 0)\
					or (self.previous_position.y > 0 and self.position.y < 0):
				faulty_team_id = self._current_team_touches[-1] if len(self._current_team_touches) > 0 else None
				ge_ticks = game_engine.get_running_ticks()
				d = {"faulty_team": faulty_team_id, "rule_type": RuleType.UNDER_NET, "time_stamp": ge_ticks}
				pg.event.post(pg.event.Event(RULES_BREAK_EVENT, d))

	def reset_rules(self):
		self._current_team_touches = []

	def reset_colliding(self):
		self.is_colliding_ground = False
		self.is_colliding_net = False
		self.is_colliding_character = False

	def wait_to_be_served_by(self, character):
		self.reset_rules()
		self.reset_colliding()
		self.will_be_served = True
		self.previous_position = character.get_hands_position()
		self.position = character.get_hands_position()

	@property
	def position(self):
		return self._position
	
	@position.setter
	def position(self, value):
		self._position = value
		self.collider.center = self._position
	
	def draw_debug(self):
		prev_rect = self.dbg_rect
		prev_rect_shadow = self.dbg_rect_shadow
		
		self.dbg_rect = debug3D_utils.draw_horizontal_ellipse(Vector3(self.position[0], self.position[1], 0), self.radius)
		self.dbg_rect_shadow = self.collider.draw_debug()
		
		return [prev_rect.union(self.dbg_rect), prev_rect_shadow.union(self.dbg_rect_shadow)]
	
	def move_rel(self, dxyz):
		self.position += Vector3(dxyz)
	
	def move_at(self, new_pos):
		self.position = Vector3(new_pos)
	
	def set_velocity(self, new_vel):
		self.velocity = Vector3(new_vel)
	
	def add_velocity(self, d_vel):
		self.velocity += Vector3(d_vel)

	def update_rules(self):
		self.check_if_out_of_bounds()
		self.check_if_under_net()

		if self.is_colliding_ground:
			self.manage_touch_ground_rule()

	def update_physics(self, dt):
		self.previous_position = Vector3(self.position)
		if not self.will_be_served:
			self.add_velocity(Vector3(0, 0, -0.001 * dt * G))
			self.move_rel(0.001 * dt * self.velocity)
		else:
			self.velocity = Vector3()

	def update(self, new_scale_factor=None, raw_rects_to_redraw=None, raw_rects_to_erase=None):
		"""

		:param new_scale_factor:
		:param raw_rects_to_redraw:
		:param raw_rects_to_erase:
		:return:
		"""
		display_manager = Engine.Display.display_manager.DisplayManager.get_instance()
		camera = display_manager.camera

		top_left_px = camera.world_to_pixel_coords(self.position + Vector3(0, -self.radius, self.radius), NOMINAL_RESOLUTION)
		btm_right_px = camera.world_to_pixel_coords(self.position + Vector3(0, self.radius, -self.radius), NOMINAL_RESOLUTION)
		# TODO: process r_px for self.raw_rect; radius in pixel as for debug3D

		# self.set_raw_rect(pg.Rect(top_left_px[0], top_left_px[1],
		# 						  btm_right_px[0] - top_left_px[0], btm_right_px[1] - top_left_px[1]))

		# TODO: not dirty for each frame...
		self.dirty = 1
		if raw_rects_to_redraw is None:
			raw_rects_to_redraw = [self.raw_rect.copy()]
		self.raw_rects_to_redraw = raw_rects_to_redraw

		self.set_raw_rect(pg.Rect(top_left_px[0], top_left_px[1], 32, 32))

		f_scale = display_manager.f_scale
		ScalableSprite.update(self, f_scale, raw_rects_to_redraw=self.raw_rects_to_redraw)


# encoding : UTF-8

from pygame import *
from math import tan, radians


class Camera:
	def __init__(self, pos, focus_pt, w=800, h=640, fov_angle=60):
		self.w = w
		self.h = h
		self.position = Vector3(pos)
		self.focus_point = Vector3(focus_pt)
		
		self.fov_angle = fov_angle
		self.fov = tan(radians(self.fov_angle))
		
		self.surface = Surface((self.w, self.h))
		
	def world_to_cam_3d_coords(self, w_pt):
		# w vector in world ref
		fc = (self.position - self.focus_point).normalize()
		
		# translation
		t_pt = w_pt - self.position
		
		# rotation
		sin_a = fc[2]
		cos_a = fc[0]
		
		c_pt = Vector3(t_pt[1],
					   sin_a * t_pt[0] - cos_a * t_pt[2],
					   cos_a * t_pt[0] + sin_a * t_pt[2])
		
		return c_pt
		
	def world_to_pixel_coords(self, pt_3d):
		u, v = 0, 0
		
		pt_3c = self.world_to_cam_3d_coords(pt_3d)
		
		if pt_3c[2] != 0:
			u = int(-self.w / (2 * self.fov) * pt_3c[0] / pt_3c[2] + self.w / 2)
			v = int(-self.h / (2 * self.fov) * pt_3c[1] / pt_3c[2] + self.h / 2)
		return u, v
	
	def draw_sphere(self, pos, r):
		# m to pixel
		# TODO : r_px must be processed with a norm2 ?
		r_px = self.world_to_pixel_coords(pos + Vector3(0, r, 0))[0] - self.world_to_pixel_coords(pos)[0]
		draw.circle(self.surface, (255, 0, 0), self.world_to_pixel_coords(pos), r_px)

	def draw_horizontal_ellipse(self, pos, r):
		# TODO : draft, messy
		pts = [self.world_to_pixel_coords(Vector3(pos) + (0, -r, 0)),
		       self.world_to_pixel_coords(Vector3(pos) + (0, r, 0))]
		pts2 = [self.world_to_pixel_coords(Vector3(pos) + (-r, 0, 0)),
		       self.world_to_pixel_coords(Vector3(pos) + (r, 0, 0))]
		rect = Rect(pts[0], (abs(pts[1][0] - pts[0][0]), abs(pts2[1][1] - pts2[0][1])))
		draw.ellipse(self.surface, (20, 20, 20), rect)
		draw.rect(self.surface, (0, 255, 0), rect, 2)

	def draw_polygon(self, pts):
		draw.polygon(self.surface, (255, 255, 255), [(self.world_to_pixel_coords(pt)) for pt in pts])
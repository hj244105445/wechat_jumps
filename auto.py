#coding:gbk
__author__ = 'hejun 244105445@qq.com'

import math
import os
import time
import random
import sys
import cv2
import logging
from PIL import Image

logger = logging.getLogger('jumps')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler("jumps.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


press_velocity = 0.7


def get_profile():
	os.system('adb shell screencap -p /sdcard/jumps.jpg')
	os.system('adb pull /sdcard/jumps.jpg ./img/')


class WeChatJumps(object):

	def __init__(self,chess_img,bk_img,circle_img):
		self.img_chess = cv2.imread(chess_img,0)
		self.img_bk = cv2.imread(bk_img,0)
		self.img_circle = cv2.imread(circle_img,0)

	def __calc_target_pos(self,max_loc1):
		img_rgb = cv2.GaussianBlur(self.img_bk, (5, 5), 0)
		canny_img = cv2.Canny(img_rgb, 1, 10)
		H, W = canny_img.shape

		# ��ȥС���������Ա�Ե������ĸ���
		for k in range(max_loc1[1] - 10, max_loc1[1] + 202):
			for b in range(max_loc1[0] - 10, max_loc1[0] + 82):
				canny_img[k][b] = 0

		# cv2.namedWindow('img',cv2.WINDOW_NORMAL)
		# cv2.imshow('img',canny_img)
		# cv2.waitKey(0)

		y_top = 400
		x_top = 0
		for row in canny_img[400:]:#���ϰ벿��400���ؿ�ʼ����ÿ�м��������ֲ�Ϊ0�ĵ㣬���ҵ�����Ķ���
			if 0 != max(row):
				for index,value in enumerate(row):#��һ�еĵ�һ����Ϊ0�ĵ����x
					if 0 != value:
						x_top = index
				break
			y_top += 1

		y_bottom = y_top + 40#����ƫ��40���أ���֤��������״�ĵ㲻���
		for row in range(y_bottom,H):#�̶�x���꣬�����������ĵײ�����һ����Ϊ0�ĵ��������ĵײ�y����
			if 0 != canny_img[row,x_top]:
				y_bottom = row
				break

		return x_top,(y_top + y_bottom) / 2

	def __get_pos(self):
		res = cv2.matchTemplate(self.img_chess,self.img_bk,cv2.TM_CCOEFF_NORMED)
		min_val,max_val,min_pos,max_pos = cv2.minMaxLoc(res)
		height,width = self.img_chess.shape
		chess_x,chess_y = max_pos[0] + width // 2,max_pos[1] + height
		res = cv2.matchTemplate(self.img_circle,self.img_bk,cv2.TM_CCOEFF_NORMED)
		min_val1,max_val1,min_pos1,max_pos1 = cv2.minMaxLoc(res)
		if max_val1 > 0.75:
			print 'jump to circle...'
			height,width = self.img_circle.shape
			target_x,target_y = max_pos1[0] + width // 2,max_pos1[1] + height // 2
		else:
			target_x,target_y = self.__calc_target_pos(max_pos)
		if max_val < 0.85:
			print max_val
			pass
		return chess_x,chess_y,target_x,target_y

	def __get_press_position(self):#ÿ�ΰ�ѹλ��������࣬��ban
		screen_height,screen_width = self.img_bk.shape
		random_spawn = 10 * random.random()
		start_x = screen_width * 0.4 + random_spawn
		start_y = screen_height * 0.8 + random_spawn
		end_x = start_x + random_spawn
		end_y = start_y + random_spawn
		return int(start_x),int(start_y),int(end_x),int(end_y)

	def jump_once(self):
		original_x,original_y,target_x,target_y = self.__get_pos()
		print original_x,original_y,target_x,target_y
		distance = math.sqrt((target_x - original_x) ** 2 + (target_y - original_y) ** 2)
		press_time = distance / press_velocity
		press_time = max(press_time,200)
		print 'distance is %d,press time is %d' % (distance,press_time)
		logger.info('distance is %d,press time is %d' % (distance,press_time))
		start_x,start_y,end_x,end_y = self.__get_press_position()
		cmd = 'adb shell input swipe {} {} {} {} {}'.format(start_x,start_y,end_x,
															end_y,int(press_time))
		print cmd
		os.system(cmd)

if '__main__' == __name__:
	print 'jump begin...'
	while True:
		get_profile()
		wj = WeChatJumps('img/chess.jpg','img/jumps.jpg','img/circle.jpg')
		wj.jump_once()
		time.sleep(random.uniform(1.2,1.8))



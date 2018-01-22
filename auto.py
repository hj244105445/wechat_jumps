#coding:gbk
__author__ = 'hejun 244105445@qq.com'

import math
import os
import time
import random
import sys
import cv2

press_velocity = 0.7

def get_press_position():#每次按压位置少量差距，防ban
	screen_width = 1080
	screen_height = 1920
	random_spawn = 100 * random.random()
	start_x = screen_width * 0.3 + random_spawn
	start_y = screen_height * 0.7 + random_spawn
	end_x = start_x + random_spawn
	end_y = start_y + random_spawn
	return int(start_x),int(start_y),int(end_x),int(end_y)

def parse_input(info):
	return tuple([int(pos) for pos in info.split(' ')])

def get_profile():
	os.system('adb shell screencap -p /sdcard/jumps.jpg')
	os.system('adb pull /sdcard/jumps.jpg img/')

def ch_curdir():
	os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def get_reference_val(img_reference,img_tempale):#获取参照物的坐标
	res = cv2.matchTemplate(img_reference,img_tempale,cv2.TM_CCOEFF_NORMED)
	min_val,max_val,min_pos,max_pos = cv2.minMaxLoc(res)
	height,width = img_reference.shape
	return max_val,max_pos[0] + width,max_pos[1] + height

def get_board_pos(img_chess,img_board):
	res = cv2.matchTemplate(img_chess,img_board,cv2.TM_CCOEFF_NORMED)
	max_loc1 = cv2.minMaxLoc(res)[3]

	img_rgb = cv2.GaussianBlur(img_board, (5, 5), 0)
	canny_img = cv2.Canny(img_rgb, 1, 10)
	H, W = canny_img.shape


	# 消去小跳棋轮廓对边缘检测结果的干扰
	for k in range(max_loc1[1] - 10, max_loc1[1] + 202):
		for b in range(max_loc1[0] - 10, max_loc1[0] + 82):
			canny_img[k][b] = 0

	y_top = 400
	x_top = 0
	for row in canny_img[400:]:#从上半部分400像素开始向下每行检索，出现不为0的点，则找到跳板的顶点
		if 0 != max(row):
			for index,value in enumerate(row):#这一行的第一个不为0的点就是x
				if 0 != value:
					x_top = index
			break
		y_top += 1

	y_bottom = y_top + 50#向下偏移50像素，邻近点会出现255的值
	for row in range(y_bottom,H):#固定x坐标，纵向查找跳板的底部，第一个不为0的点就是跳板的底部y坐标
		if 0 != canny_img[row,x_top]:
			y_bottom = row
			break
	return x_top,(y_top + y_bottom) / 2


def jump(original_x,original_y,target_x,target_y):
	distance = math.sqrt((target_x - original_x) ** 2 + (target_y - original_y) ** 2)
	press_time = distance / press_velocity
	press_time = max(press_time,200)
	print 'distance is %d,press time is %d' % (distance,press_time)
	start_x,start_y,end_x,end_y = get_press_position()
	cmd = 'adb shell input swipe {} {} {} {} {}'.format(start_x,start_y,end_x,
														end_y,int(press_time))
	print cmd
	os.system(cmd)

if '__main__' == __name__:
	# confirm_info = raw_input('请确保打开微信跳一跳，手机打开USB调试选项，确认请输入y，尚未准备好请输入n: ')
	# if 'y' != confirm_info:
	# 	exit(0)
	ch_curdir()
	while True:
		get_profile()
		img_chess = cv2.imread('img/chess.jpg',0)
		img_bk = cv2.imread('img/jumps.jpg',0)
		img_circle = cv2.imread('img/circle.jpg',0)
		time.sleep(1)#等待截图完成
		max_val0,chess_x,chess_y = get_reference_val(img_chess,img_bk)
		chess_x -= 40
		target_x,target_y = get_board_pos(img_chess,img_bk)
		print max_val0,chess_x,chess_y,target_x,target_y
		jump(chess_x,chess_y,target_x,target_y)
		time.sleep(random.uniform(1.2,1.8))#等待跳跃完成，跳跃为随机值，防止被检测



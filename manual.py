#coding:gbk
__author__ = 'hejun 244105445@qq.com'

import math
import os
import time
import random

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
	os.system('adb shell screencap -p /sdcard/jumps.png')
	os.system('adb pull /sdcard/jumps.png')


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
	while True:
		get_profile()
		input_info = raw_input('请输入跳棋和目标位置的坐标，以空格区分：')
		chess_x,chess_y,target_x,target_y = parse_input(input_info)
		jump(chess_x,chess_y,target_x,target_y)
		time.sleep(2)




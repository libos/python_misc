import os

###### 必须加在urllib2之前
###### 还必须pip install PySocks
###### 这是全部的都用代理，应该把这部分加到download_image里的，第一次下载不用proxy，第二次之后用proxy
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 65531)
socket.socket = socks.socksocket
###### 
import urllib2
import httplib

import multiprocessing


def download_image(url, save_name,proxy = None):
	try:
		fp = urllib2.urlopen(url, timeout=20)
		data = fp.read()
		fp.close()

		print url + ' downloading...'
		fid = open(save_name, 'w+b')
		fid.write(data)
		flag = True 
		######### 此处应该判断文件的大小，如果有md5也需要校验md5
		flsize = os.path.getsize(save_name)
		if flsize < 10:
			flag = False
		######
	except Exception:
		print url + ' downloading io error...'
		flag = False
	return flag



def readList((list_path, save_path, log_path)):
	if not os.path.exists(save_path):
		os.mkdir(save_path)

	fid = open(list_path, 'r')
	fid_log = open(log_path, 'w')
	line = fid.readline()
	count = 1
	while line:
		tmp = line.split(' ')
		name = tmp[0]
		url = tmp[2]
		filename = save_path + name + '.jpg'

		# skip the existing images
		if os.path.exists(filename):
			print filename + ' is already downloaded..'
			continue

		flag = download_image(url, filename)
		#########  这里应该判断flag，如果有问题，那么重新下载，不然才记录
		retrytimes = 0
		while not flag:
			flag = download_image(url, filename)
			retrytimes = retrytimes + 1
			if retrytimes > 5:
				break
			
		if not flag:
			fid_log.write(line)
			#raw_input();
		line = fid.readline()

	fid.close();
	fid_log.close();


def readPath(list_dir, save_dir, log_dir):
	count = 0;
	tasks = []
	for root, dirs, files in os.walk(list_dir):
		for fn in files:
			folder = fn.replace('.txt', '')
			log_path = log_dir + folder + '_error.txt';
			save_path = save_dir + folder + '/'
			
			tasks.append((root + fn, save_path, log_path))
			#readList(root + fn, save_path, log_path)
	pool_size = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=2)
	pool.map(readList, tasks)
	pool.close()
	pool.join()
	


if __name__ == "__main__":
	readPath("/home/xiang.wu/project/code/python/files/", "/home/xiang.wu/data/vgg_face/image/", "/home/xiang.wu/data/vgg_face/log/")

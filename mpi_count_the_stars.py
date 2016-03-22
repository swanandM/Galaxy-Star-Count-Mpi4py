####################################################################################
#
#                  Image Processing example for 10 node MPI cluster
#                                Author :  Mohan Muppidi
#
#	This program requires image file to be downloaded. 
#	wget http://www.spacetelescope.org/static/archives/images/publicationtiff40k/heic1502a.tif
#                   
#
####################################################################################


import numpy as np
import time
from mpi4py import MPI
import cv2
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
	t1 = time.time()
	img = cv2.imread("heic1502a.tif",0)
	t2 = time.time()
	print " Time taken to open and read the image is : %r sec " %(t2-t1)
	# (12788, 40000) Size of the image so dividing it into 10 parts
	# Each part is of same size 6394 x 8000 
	# each of this part will be sent to the other nodes for processing
	print " sending the parts of image to different nodes "
	t1 = time.time()
	img_node1 = img[:6394,:8000]
	comm.send(img[6395:,:8000], dest=1, tag=11)
	comm.send(img[:6394,8001:16000], dest=2, tag=11)
	comm.send(img[6395:,8001:16000], dest=3, tag=11)
	comm.send(img[:6394,16001:24000], dest=4, tag=11)
	comm.send(img[6395:,16001:24000], dest=5, tag=11)
	comm.send(img[:6394,24001:32000], dest=6, tag=11)
	comm.send(img[6395:,24001:32000], dest=7, tag=11)
	comm.send(img[:6394,32001:], dest=8, tag=11)
	comm.send(img[6395:,32001:], dest=9, tag=11)
	


        img_node_thresh1 =  cv2.adaptiveThreshold(img_node1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0) 
	star_count = [0,1,2,3,4,5,6,7,8,9]
	star_count[0] = ((200 < img_node_thresh1)).sum()
	
	
	C_dict1 = {}
	C_dict2 = {}
	C_dict1[0] = img_node_thresh1
	
	# Receiving the count of the stars from all the nodes	
	star_count[1] = comm.recv(source=1, tag=15)
	print "Star count received from node 1"
	star_count[2] = comm.recv(source=2, tag=15)
	print "Star count received from node 2"
	star_count[3] = comm.recv(source=3, tag=15)
	print "Star count received from node 3"
	star_count[4] = comm.recv(source=4, tag=15)
	print "Star count received from node 4"
	star_count[5] = comm.recv(source=5, tag=15)
	print "Star count received from node 5"
	star_count[6] = comm.recv(source=6, tag=15)
	print "Star count received from node 6"
	star_count[7] = comm.recv(source=7, tag=15)
	print "Star count received from node 7"
	star_count[8] = comm.recv(source=8, tag=15)
	print "Star count received from node 8"
	star_count[9] = comm.recv(source=9, tag=15)
	print "Star count received from node 9"
	t2 = time.time()
	print " The total number of stars : %s " %(sum(star_count))
	print " Time taken to count the stars : %r sec " %(t2-t1)
	
	
	C_dict2[0] = comm.recv(source=1, tag=13)
	print "received result from 1"
	C_dict1[1] = comm.recv(source=2, tag=13)
	print "received result from 2"
	C_dict2[1] = comm.recv(source=3, tag=13)
	print "received result from 3"
	C_dict1[2] = comm.recv(source=4, tag=13)
	print "received result from 4"
	C_dict2[2] = comm.recv(source=5, tag=13)
	print "received result from 5"
	C_dict1[3] = comm.recv(source=6, tag=13)
	print "received result from 6"
	C_dict2[3] = comm.recv(source=7, tag=13)
	print "received result from 7"
	C_dict1[4] = comm.recv(source=8, tag=13)
	print "received result from 8"
	C_dict2[4] = comm.recv(source=9, tag=13)
	print "received result from 9"


	
	

 
	for i in range(5):
		if i > 0:
			img_proc_1 = np.hstack((img_proc_1,C_dict1[i]))
		else :
			img_proc_1 = C_dict1[i]	
        for i in range(5):
                if i > 0:
                        img_proc_2 = np.hstack((img_proc_2,C_dict2[i]))
                else :
                        img_proc_2 = C_dict2[i]
	img_proc = np.vstack((img_proc_1,img_proc_2))
	print " The size of the reconstructed image is  "
	print img_proc.shape
	
	#img_proc = cv2.resize(img_proc,(0,0), fx=0.1, fy=0.1) 
	#cv2.imwrite("/var/www/example.com/public_html/1.jpg",img_proc)
	t1 = time.time()
	img_node_thresh1 =  cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0) 
	all_star_count = ((200 < img_node_thresh1)).sum()
	t2 = time.time()
	print " Time taken to count the stars in single node : %r sec " %(t2-t1)
	print " The stars count when used serial algo is : %r " %(all_star_count)
	print "Yay counted the stars finally !!!"

else:
	B_local = comm.recv(source=0, tag=11)	
	print "at Node %r received matrix of shape %s " %(rank, B_local.shape )
        img_node_thresh =  cv2.adaptiveThreshold(B_local,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0)
	
        star_count_node = ((200 < img_node_thresh)).sum()
	comm.send(star_count_node,dest=0, tag=15)
	print "sent back the star count %s" %(rank)
	comm.send(img_node_thresh, dest=0, tag=13)
	
	

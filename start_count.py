##############################################################################################################
#                                       Author - Swanand Mhalagi                                             #
#                       This program requires image file to be downloaded.                                   #
#	wget http://www.spacetelescope.org/static/archives/images/publicationtiff40k/heic1502a.tif           #
################################################################################################################

import numpy as np
import Image
import cv2
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

c = np.array([0])
local_x = np.array([0])
a = np.array((12788,40000),dtype='uint8') # Image has 12788 rows and 40000 colums

if rank == 0:
        t1 = MPI.Wtime()
        img = cv2.imread("heic1502a.tif",0) #Read the image
        t2 = MPI.Wtime()
        print " Time taken to open and read the image is : %r sec " %(t2-t1)
        a = np.array(img)  #Convert to a Matrix

w1 = MPI.Wtime()
remender = 12788 % size  # devide image horizontally

if rank < remender:
        rowsize = 12788/size
        rowsize = rowsize + 1
else:
        rowsize = 12788/size

c = np.array((rowsize,40000)) # Part of image given to each process
comm.Bcast(c, root=0)
local_x = np.zeros(c,dtype='uint8')
comm.Bcast(local_x, root=0)
total = np.array([0])

comm.Scatterv(a,local_x,root=0) # scatter the image

#image processing
img_node_thresh =  cv2.adaptiveThreshold(local_x,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,59,0)
star_count_node = ((200 < img_node_thresh)).sum()
print " Star count at Rank", rank,"is ", star_count_node

comm.Reduce(star_count_node,total,op=MPI.SUM,root=0) # Reduce to zero process

if comm.rank == 0:
        w2 = MPI.Wtime()
        print " Total Stars ", total
        print " Total time taken", w2-w1 ,"sec"



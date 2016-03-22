Hello Guys,

Recently NASA uploaded an image of whole Galaxy having N number stars.

This program is written to count the number of stars using python for MPI and some image processing tools like openCV.

There are 2 programs in this folder 

1) mpi_count_the_stars.py is written by my friend Mr.Mohan Muppidi. This program uses 10 node MPI cluster using point to point communication.
   To run this program use following command---
	mpirun -n 10 python mpi_count_the_stars.py

2) star_count.py is written by me. My program is inspired from Mohan's program. This program uses collective communication which is next 
   step of point to point communication to inprove the performance. You can run this program with any number of nodes.
   To run this program use following command-
	mpirun -n NumberOfNodes python star_count.py
    e.g mpirun -n 15 python star_count.py  
   
Even before running above programs you to install OpenMPI/MPI4py and OpenCV on your linux/windows machine. You will also need some 
NumPy and SciPy libraries. 

Download below star image---
wget http://www.spacetelescope.org/static/archives/images/publicationtiff40k/heic1502a.tif

for further assistance contact---
swan1991m@gmail.com
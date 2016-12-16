#

# REQUIRES the handbrake video transcoder command line
#!/usr/bin/python
##
##"""
##USAGE of handbrake command line
##
##
##"C:\Program Files\Handbrake\handbrakecli" -i "C:\Users\kende\Desktop\101CANON\MVI_2854.MOV" -o "c:\temp\MVI_2854.mp4" --preset="High Profile" --encoder-preset="Slow" -X 960 -q 21
##
##-i input file
##-o output file
##--present="NAME OF PRESET"
##--encoder-present= SLOW VS FAST tradeoff
##-X is maximum width allowed (video Y will scale to this)
##-q  is quality on rthe RF slider  , realistic  range is 22 (well compressed - ) to 18 (little compression)  - but can go from 51 to 0
##    use 20 for vidoes with low res  21 or 22 for big
##"""






#import os
import datetime
import win32file
import pytz
import time
import subprocess


resolution_width ='-X 1280'
quality = '-q 23'   #somewhere between 22 (low qual and 18 high qual - can be wider range but effect is exponential

handbrakeclie_executable = "C:\\Program Files\\Handbrake\\handbrakecli"

# traverse root directory, and list directories as dirs and files as files
#os. walk returns at each step dirs (a list of dirs), files (a list of files in dir), root (string - relative pathname of each dir)
import os

#source_path = "C:\\Users\\kende\\Desktop\\minicam"
#destination_path = "C:\\Users\\kende\\Desktop\\video_out"

source_path = input('Source dir:')
destination_path = input('Destiation dir:')

if source_path == destination_path:
    print('Source and destination should not be the same folder')
    quit()



def winddows_touch(file_name,newtime): #os.utime does not work well in windows, changes modified time but not creation time
    """ All this  is needed because windows stores file creation time but linux does not
     so the other functions do not fix that (they only fix modified and last access date)"""
    newtime= datetime.datetime.fromtimestamp(newtime)
    if newtime.tzinfo is None:
        tz = pytz.timezone('UTC')
        newtime = tz.localize(newtime)
    ctime = newtime; atime = newtime; mtime = newtime;
    filehandle = win32file.CreateFile(file_name, win32file.GENERIC_WRITE,0, None, win32file.OPEN_EXISTING, 0, 0)
    win32file.SetFileTime(filehandle, ctime, atime, mtime)



print('\n\n******************************\n'
      'Attention - This is encoding at {0} width    \n******************* '.format(resolution_width))
time.sleep(2)

logfile = open(destination_path +'\\video_compress.csv','w+')
logfile.write('file, size_in, size_out, compression, time \n\n')

i= 0
for root, dirs, files in os.walk(source_path, topdown=False):
    for dir in dirs:
        #create the subtree structure in destination dir
        mirror_dir =  root+'\\'+dir
        mirror_dir = mirror_dir.replace(source_path,destination_path)

        if not os.path.exists(mirror_dir):
            os.makedirs(mirror_dir)


    for file in files:
        if os.path.splitext(file)[1].lower() in ['.mp4' ,'.m4v','.mov','.mpg','.avi']:
            i=i+1
            source_file = os.path.abspath(root)+'\\'+file
            size_in = os.path.getsize(source_file)
            start_time = time.time()



            st= os.stat(source_file)
            original_file_mtime= st.st_mtime


            destination_file = os.path.abspath(root)+'\\'+os.path.splitext(file)[0]+'.mp4'
            destination_file= destination_file.replace(source_path,destination_path)
            command_template ="""{handbrakecli} -i "{source_file}" -o "{outfile}" --preset="High Profile" --encoder-preset="Slower" {width} {quality}""".format(handbrakecli=handbrakeclie_executable,source_file=source_file,outfile=destination_file,width=resolution_width,quality= quality)
            #print(command_template)

            #Run handbrake
            return_code = subprocess.call(command_template)
            compression_time = time.time() - start_time
            size_out = os.path.getsize(destination_file)
            compression_factor =  (size_out/size_in)

            logfile.write(source_file+',')
            logfile.write(str(size_in)+',')
            logfile.write(str(size_out)+',')
            logfile.write(str(round(compression_factor,2))+',')
            logfile.write(str(round(compression_time,2))+ 'sec,')


            if return_code == 1:
                print('Cound not use handbrake on ',source_file)
                logfile.write('error \n')
            else:
                try:
                    winddows_touch(destination_file,original_file_mtime)
                    logfile.write('success \n')
                except Exception as e:
                    print('Failed to touch file',destination_file,e)
                    logfile.write('error \n')


    logfile.close()

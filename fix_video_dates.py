
# Compressing video files using handbrake sets the timestamp on the compressed files to the date of compression.
# Incorrect dates mess with programs that organise your albums according to date 
# Do this script gets file info for two different directories (old and new) and fixes the creation dates of "new" to match "original"
# filenames must be the same except for the extension


import os
import datetime
import win32file
import pytz




def winddows_touch(file_name,newtime): #utime does not work well in windows, changes modified time but not creation time
    """ All this is needed because windows stores file creation time but linux does not
     so the other functions do not fix that (they only fix modified and last access date)"""
    newtime= datetime.datetime.fromtimestamp(newtime)
    if newtime.tzinfo is None:
        tz = pytz.timezone('UTC')
        newtime = tz.localize(newtime)
    ctime = newtime; atime = newtime; mtime = newtime;
    filehandle = win32file.CreateFile(file_name, win32file.GENERIC_WRITE,0, None, win32file.OPEN_EXISTING, 0, 0)
    win32file.SetFileTime(filehandle, ctime, atime, mtime)



def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)




def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()




original_pth  = input('Source dir')
new_pth  = input('Source dir')

def main():

    original_files = {}
    new_files ={}

    #build dict for new files directory
    temp  = os.listdir( new_pth )
    for afile in temp:
        (filename, filext) = os.path.splitext(afile)
        full_path =  new_pth + '\\' + afile
        st= os.stat(full_path)
        lowercase_name = str(filename).lower()
        new_files[lowercase_name] = {}
        new_files[lowercase_name]['original_name']  =filename
        new_files[lowercase_name]['fileext'] =filext
        new_files[lowercase_name]['mtime'] = st.st_mtime
        new_files[lowercase_name]['ctime'] = st.st_ctime
        date_as_str = lowercase_name[:8]   # for filenames sthat start with the date ex: 20151131_video_name.mpg


    #build dict for ORIGINAL files directory
    # TODO this is almost a copy of the code for new files, make a function
    temp  = os.listdir( original_pth )
    for afile in temp:
        (filename, filext) = os.path.splitext(afile)
        full_path =  original_pth + '\\' + afile
        st= os.stat(full_path)
        lowercase_name = str(filename).lower()
        original_files[lowercase_name] = {}
        original_files[lowercase_name]['original_name']  =filename
        original_files[lowercase_name]['fileext'] =filext
        original_files[lowercase_name]['mtime'] = st.st_mtime
        original_files[lowercase_name]['ctime'] = st.st_ctime
        date_as_str = lowercase_name[:8]   # for filenames sthat start with the date ex: 20151131_video_name.mpg


        nice1  = datetime.datetime.fromtimestamp(original_files[lowercase_name]['ctime']).strftime('%Y-%m-%d %H:%M:%S')
        nice2  = datetime.datetime.fromtimestamp(original_files[lowercase_name]['mtime']).strftime('%Y-%m-%d %H:%M:%S')




    for filename in new_files:
        if (filename in original_files) and (new_files[filename]['fileext'] in ['.mp4','.jpg','.jpeg','.m4v','.mov','.mpg','.avi']):
            fullname  = filename+new_files[filename]['fileext']
            full_path =  new_pth + '\\' + fullname
            print('change ',fullname, 'from ',new_files[filename]['mtime'] , ' to ', original_files[filename]['mtime'], end =''  )
            #os.utime(full_path,(original_files[filename]['mtime'],original_files[filename]['mtime']))
            #touch(full_path,(original_files[filename]['mtime'],original_files[filename]['mtime']))
            winddows_touch(full_path,original_files[filename]['mtime'])
            print ('after change its: ', modification_date(full_path) )
        else:
            print('Did not touch' ,full_path)



if __name__ == '__main__':
    main()





#os.utime(f,(atime,new_mtime))
#os.rename(filename, filename[7:])


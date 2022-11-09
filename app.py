import datetime
import os
import random
import subprocess
import time
from os import listdir
from os.path import isfile, join

overlaying ='ffmpeg -i {} -i {} -filter_complex "[0]scale=300:-1 [overlay]; [1][overlay]  overlay=0:0" -map 0:a -c:a copy -preset ultrafast -y {}'
cutting = 'ffmpeg -i {} -c copy -map 0 -segment_time {} -f segment -reset_timestamps 1 output%03d.mp4'

def time_now():
    now = datetime.datetime.now()
    print (now.strftime("%H:%M:%S"), end = " - ")

def getLength(filename):
    from subprocess import check_output
    a = str(check_output('ffprobe -i  "'+filename+'" 2>&1 |findstr "Duration"',shell=True)) 
    a = a.split(",")[0].split("Duration:")[1].strip().split('.')[0]
    return str(a)

def creator():
    cut_command = 'ffmpeg -y -ss 00:00:00 -to {} -i {} -c:a copy -preset ultrafast {}'
    overlaying_command ='ffmpeg -i {} -i {} -filter_complex "[0]scale=300:-1 [overlay]; [1][overlay]  overlay=0:0" -map 0:a -c:a copy -preset ultrafast -y {}'
    cutting_segments = 'ffmpeg -i {} -c copy -map 0 -segment_time {} -f segment -reset_timestamps 1 segments/output%03d.mp4'
    bg_path = 'background_videos'
    ol_path = 'overlay_videos'
    res_path = 'results'
    seg_path = 'segments'
    bgs = [f for f in listdir(bg_path) if isfile(join(bg_path, f))]
    overlays_raw = [f for f in listdir(ol_path) if isfile(join(ol_path, f))]
    overlays = []
    for overlay in overlays_raw:
        if " " in overlay:
            os.rename(os.path.abspath(join(ol_path, overlay)), os.path.abspath(join(ol_path, overlay.replace(' ', ''))))
        overlays.append(overlay)
    for index, video in enumerate(overlays):
        print('=' * 20)
        index += 1
        time_now()
        print('overlay lenght: ', end = ' ')
        dur = getLength(os.path.abspath(os.path.join(ol_path, video)))
        print(dur)
        time_now()
        print('start cutting bg on segments')
        subprocess.run(cutting_segments.format(join(bg_path, bgs[0]), dur), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segments = [f for f in listdir(seg_path) if isfile(join(seg_path, f))]
        seg_db = []
        for segment in segments[2:-1]:
            seg_db.append(join(seg_path, segment))
        time_now()
        print('segments cutted. segments count: {}'.format(len(seg_db)))
        bg = random.choice(seg_db)
        time_now()
        print('video №{} ({}), start overlaying, bg: {}'.format(index, video, bg))
        # subprocess.run(overlaying_command.format(join(ol_path, video), bg, join('upload/video_{}'.format(index), 'video.mp4')), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(overlaying_command.format(join(ol_path, video), bg, join(res_path, "video_{}.mp4".format(index))), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time_now()
        print('ended overlaying video №{} ({})'.format(index, video))
        for segment in segments:
            os.remove(join(seg_path, segment))


creator()

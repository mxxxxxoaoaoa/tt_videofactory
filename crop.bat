ffmpeg -y -i raw.mp4 -vf "scale=(iw*sar)*max(720/(iw*sar)\,1280/ih):ih*max(720/(iw*sar)\,1280/ih), crop=720:1280" -c:v mpeg4 -vtag mp4v -q:v 4 -preset ultrafast background_videos/bg_cropped.mp4
pause
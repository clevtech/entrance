import vlc

player = vlc.MediaPlayer('rtsp://192.168.81.218:8554/live')

player.video_take_snapshot(0, 'snapshot.png', 0, 0)


import rtsp
# client = rtsp.Client(rtsp_server_uri='rtsp://192.168.81.218:8554/live')
# client.read().show()
# client.close()

with rtsp.Client('rtsp://192.168.81.218:8554/live') as client:
    client.read().rotate(270).save("face.png")

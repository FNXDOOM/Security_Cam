import cv2
import threading
from collections import deque

class VideoStream:
    """A class to read frames from a camera in a dedicated thread."""
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        if not self.stream.isOpened():
            print(f"Error: Could not open video source at {src}")
            raise IOError("Cannot open video source")
        
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.stream.set(cv2.CAP_PROP_FPS, 30)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)
            
        self.width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.stream.get(cv2.CAP_PROP_FPS) or 30.0

        print(f"Camera initialized: {self.width}x{self.height} @ {self.fps} FPS")

        self.deque = deque(maxlen=1)
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        self.thread.start()
        return self

    def update(self):
        while not self.stopped:
            ret, frame = self.stream.read()
            if ret:
                self.deque.append(frame)

    def read(self):
        try:
            return self.deque[0]
        except IndexError:
            return None

    def stop(self):
        self.stopped = True
        self.thread.join(timeout=1)
        self.stream.release()
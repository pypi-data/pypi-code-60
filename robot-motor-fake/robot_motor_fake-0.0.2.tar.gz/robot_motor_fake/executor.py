import cv2
from robot_core.executor.executor import Executor


class FakeMotorExecutor(Executor):
    # Start Capture
    cap = cv2.VideoCapture(0)

    # Get frame dimensions
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def execute(self, **kwargs):
        if kwargs["command"] == "forward":
            return self.forward()
        elif kwargs["command"] == "backward":
            return self.backward()
        elif kwargs["command"] == "right":
            return self.right()
        elif kwargs["command"] == "left":
            return self.left()

    def forward(self):
        img = cv2.imread('forward.png')
        img_height, img_width, _ = img.shape
        ret, frame = self.cap.read()
        frame_height, frame_width, _ = frame.shape
        x = (frame_width / 2) - (img_width / 2)
        y = 50
        frame[y:y + img_height, x:x + img_width] = img
        return frame

    def backward(self):
        img = cv2.imread('backward.png')
        img_height, img_width, _ = img.shape
        ret, frame = self.cap.read()
        frame_height, frame_width, _ = frame.shape
        x = (frame_width / 2) - (img_width / 2)
        y = frame_height - img_height - 10
        frame[y:y + img_height, x:x + img_width] = img
        return frame

    def right(self):
        img = cv2.imread('right.png')
        img_height, img_width, _ = img.shape
        ret, frame = self.cap.read()
        frame_height, frame_width, _ = frame.shape
        x = frame_width - img_width - 10
        y = (frame_height / 2) - (img_height /2 )
        frame[y:y + img_height, x:x + img_width] = img
        return frame

    def left(self):
        img = cv2.imread('left.png')
        img_height, img_width, _ = img.shape
        ret, frame = self.cap.read()
        frame_height, frame_width, _ = frame.shape
        x = 10
        y = (frame_height / 2) - (img_height / 2)
        frame[y:y + img_height, x:x + img_width] = img
        return frame


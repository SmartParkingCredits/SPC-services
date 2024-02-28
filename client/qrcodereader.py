import cv2
import sys
import os
import numpy as np
try:
    from picamera2 import Picamera2, Preview
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False

def qr_code_detected(data):
    """
    Callback function to be called when a QR code is detected.
    :param data: Decoded data from the QR code.
    """
    print(f"QR Code detected: {data}")

def init_picamera2():
    if PICAMERA2_AVAILABLE:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(
            main={"format": "XRGB8888", "size": (1920, 1080)},
            lores={"size": (480, 360), "format": "YUV420"}
        )
        picam2.configure(config)
        picam2.start()
        return picam2
    else:
        raise RuntimeError("Picamera2 is not available on this platform.")


def read_qr_codes(callback=qr_code_detected):
    video_device = os.environ.get("VIDEO_DEVICE", 0)

    if video_device == "picam" and PICAMERA2_AVAILABLE:
        # Initialize Picamera2
        picam2 = init_picamera2()
        detector = cv2.QRCodeDetector()

        while True:
            # Capture frame
            frame = picam2.capture_array("main")
            # Convert frame to BGR format for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            # Detect and decode the QR code in the frame
            try:
                data, bbox, _ = detector.detectAndDecode(frame)
                if bbox is not None and data:
                    callback(data)
            except Exception as e:
                print(f"Error: {e}")
                continue
    else:
        # Fallback to using OpenCV for capturing frames
        cap = cv2.VideoCapture(video_device)
        detector = cv2.QRCodeDetector()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Exiting...")
                break

            try:
                data, bbox, _ = detector.detectAndDecode(frame)
                if bbox is not None and data:
                    callback(data)
            except Exception as e:
                print(f"Error: {e}")
                continue

        cap.release()

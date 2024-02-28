import cv2
import sys
import os

def qr_code_detected(data):
    """
    Callback function to be called when a QR code is detected.
    :param data: Decoded data from the QR code.
    """
    print(f"QR Code detected: {data}")

def read_qr_codes(callback=qr_code_detected):
    video_device = os.environ.get("VIDEO_DEVICE", 0)
    # Initialize the camera
    cap = cv2.VideoCapture(video_device)
    # Initialize the QR Code detector
    detector = cv2.QRCodeDetector()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Detect and decode the QR code in the frame
        try:
            data, bbox, _ = detector.detectAndDecode(frame)
            # Check if there is a QR Code in the image
            if bbox is not None and data:
                callback(data)
        except Exception as e:
            print(f"Error: {e}")
            continue

    cap.release()

import serial
import json
import time

class Servo:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.connect()

    def connect(self):
        """Establishes serial connection with Arduino."""
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for connection to establish
            print("Connected to Arduino")
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino on port {self.port}: {e}")

    def move_servo(self, position):
        """Sends command to move servo to specified position."""
        if self.serial_connection and self.serial_connection.isOpen():
            data = json.dumps({"position": position})
            self.serial_connection.write(data.encode('utf-8'))
            self.serial_connection.write(b'\n')  # Ensure message is terminated with newline
            print(f"Sent to Arduino: {data}")
        else:
            print("Serial connection not established. Call connect() to establish connection.")

    def close(self):
        """Closes the serial connection."""
        if self.serial_connection:
            self.serial_connection.close()
            print("Serial connection closed.")

# Example usage
if __name__ == "__main__":
    # Replace '/dev/ttyACM0' with your Arduino's serial port
    arduino_servo = Servo('/dev/cu.usbmodem1431401')

    try:
        # Move the servo to 90 degrees
        arduino_servo.move_servo(90)
        time.sleep(2)  # Wait for the servo to move

        # Move the servo to 45 degrees
        arduino_servo.move_servo(45)
        time.sleep(2)  # Wait for the servo to move

    except KeyboardInterrupt:
        print("Program exited gracefully")
    finally:
        arduino_servo.close()

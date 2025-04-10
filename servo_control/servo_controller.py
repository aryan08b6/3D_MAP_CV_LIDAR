import serial
import time
import serial.tools.list_ports


class servo_controller:
    def __init__(self, port="", baudrate=115200):
        if port == "":
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if p.manufacturer and "Arduino" in p.manufacturer:
                    port = p.device
                    break
            else:
                raise Exception("No Arduino found")
            
        self.port = port
        self.baudrate = baudrate
            
        self.ser = serial.Serial(port, baudrate)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()    
    
    
    def send_pan_tilt(self, pan, tilt):
        command = f"PAN:{pan},TILT:{tilt}\n"
        self.ser.write(command.encode())
        print(f"> Sent: {command.strip()}")
        
        print("Waiting for response...")
        start = time.time()
        while True:
            print("Checking for response...")
            
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode().strip()
                if response:
                    print(f"Got response: < {response}")
                    return response
            elif time.time() - start > 5:
                print("Timeout: No response received.")
                return None

                
    
if __name__ == "__main__":
    servo_controller = servo_controller()
    servo_controller.send_pan_tilt(90, 90)
    
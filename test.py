
import serial
import struct
import time

# Set up the serial connection
ser = serial.Serial(port='COM4', baudrate=115200, timeout=1)

# Function to send a packet over serial
def send_packet(sync, command, mode, apw, vpw, a_amp, v_amp, a_sens, v_sens, arp, vrp, url, lrl, res_factor, rxn_time, rec_time, thresh):
    packet = struct.pack(  # Format the packet
        'BBBBBBBBBBBBBBBBB',
        sync, command, mode, apw, vpw, a_amp, v_amp, a_sens, v_sens, arp, vrp, url, lrl, res_factor, rxn_time, rec_time, thresh
    )
    ser.write(packet)  # Send the packet over serial

# Function to unpack the 32-byte raw data
def unpack_data(raw_data):
    if len(raw_data) != 32:  # Check if the received data is exactly 32 bytes
        print(f"Error: Expected 32 bytes, but got {len(raw_data)} bytes.")
        return None
    
    # Unpack bytes 1-16 as unsigned integers, bytes 17-24 and 25-32 as floats
    format_string = '16Bdd'  # 16 unsigned bytes (B) and 2 double-precision floats (d)
    unpacked_data = struct.unpack(format_string, raw_data)
    
    # Separate the unpacked data
    single_byte_vars = unpacked_data[:16]  # First 16 single-byte variables
    float_var_1 = unpacked_data[16]       # First float variable (bytes 17-24)
    float_var_2 = unpacked_data[17]       # Second float variable (bytes 25-32)

    # Print the unpacked values
    print("Single-byte variables (bytes 1-16):", single_byte_vars)
    print("Float variable 1 (bytes 17-24):", float_var_1)
    print("Float variable 2 (bytes 25-32):", float_var_2)
    
    return {
        "single_byte_vars": single_byte_vars,
        "float_var_1": float_var_1,
        "float_var_2": float_var_2
    }

# Function to receive data from the serial port and unpack it
def receive_data():
    raw_data = ser.read(32)  # Read exactly 32 bytes
    if len(raw_data) == 32:
        print(f"Raw received data: {raw_data}")
        unpacked = unpack_data(raw_data)  # Unpack the data
        if unpacked:
            print("\nUnpacked Data:", unpacked)
    else:
        print(f"Error: Incomplete data received ({len(raw_data)} bytes).")

def main():
    send_packet(1, 0, 8, 10, 10, 5, 5, 60, 60, 100, 150, 120, 60, 8, 30, 5, 120)  
    receive_data()
    while True:
        send_packet(1, 1, 8, 10, 10, 5, 5, 60, 60, 100, 150, 120, 60, 8, 30, 5, 120)  
        receive_data()

if __name__ == "__main__":
    main()
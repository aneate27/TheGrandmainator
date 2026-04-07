import argparse
import os
import re
import sys
import time

try:
    import pygame
    import serial
    from serial.tools import list_ports
except ImportError as exc:
    print("Missing required package:", exc)
    print("Install with: pip install pyserial pygame")
    sys.exit(1)

TOUCH_EVENT_RE = re.compile(r"TOUCH([0-2])_(START|END)")
MODE_NAMES = ["BASE", "ALT"]


def list_serial_ports():
    ports = list_ports.comports()
    return [port.device for port in ports]


def parse_line(line: str):
    if not line:
        return None
    match = TOUCH_EVENT_RE.match(line.strip())
    if not match:
        return None
    index = int(match.group(1))
    event_type = match.group(2)
    return index, event_type


def load_sound(path: str):
    if not os.path.isfile(path):
        print(f"Sound file not found: {path}")
        sys.exit(1)
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as exc:
        print(f"Failed to load sound '{path}': {exc}")
        sys.exit(1)


def play_sound(sounds, index: int):
    sounds[index].play()


def build_sound_sets(args):
    base_files = [args.touch0_base, args.touch1_base, args.touch2_base]
    alt_files = [args.touch0_alt, args.touch1_alt, args.touch2_alt]

    base_sounds = [load_sound(path) for path in base_files]
    alt_sounds = [load_sound(path) for path in alt_files]
    return [base_sounds, alt_sounds]

#TODO: parse
def main():
    parser = argparse.ArgumentParser(
        description="Read ESP32 touch events from serial and play m4a files for each touch input."
    )
    parser.add_argument("--port", help="Serial port for the ESP32 (e.g. /dev/ttyUSB0 or /dev/tty.SLAB_USBtoUART)")
    parser.add_argument("--baud", type=int, default=115200, help="Serial baud rate")
    parser.add_argument("--touch0-base", default="audio files/Golden_Girls.m4a", help="m4a file for touch 0 in base mode")
    parser.add_argument("--touch1-base", default="audio files/Lillian_Dronaik_Boyfriend.m4a", help="m4a file for touch 1 in base mode")
    parser.add_argument("--touch2-base", default="audio files/Lillian_Dronaik_Gravestone.m4a", help="m4a file for touch 2 in base mode")
    parser.add_argument("--touch0-alt", default="audio files/Kim_you're_doing_amazing_sweetie.m4a", help="m4a file for touch 0 in alternate mode")
    parser.add_argument("--touch1-alt", default="audio files/Kim_you're_doing_amazing_sweetie.m4a", help="m4a file for touch 1 in alternate mode")
    parser.add_argument("--touch2-alt", default="audio files/Kim_you're_doing_amazing_sweetie.m4a", help="m4a file for touch 2 in alternate mode")
    args = parser.parse_args()

    if not args.port:
        available_ports = list_serial_ports()
        if not available_ports:
            print("No serial ports found. Connect your ESP32 and run again.")
            sys.exit(1)
        print("Available serial ports:")
        for i, port in enumerate(available_ports, start=1):
            print(f"  {i}: {port}")
        choice = input("Select port number: ").strip()
        try:
            idx = int(choice) - 1
            args.port = available_ports[idx]
        except Exception:
            print("Invalid port selection.")
            sys.exit(1)

    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.5)
    except serial.SerialException as exc:
        print(f"Failed to open serial port {args.port}: {exc}")
        sys.exit(1)

    pygame.mixer.init(frequency=44100, size=-16, channels=2)
    sounds = build_sound_sets(args)

    print(f"Listening on {args.port} at {args.baud} baud...")
    print("Touch event format: TOUCH0_START, TOUCH1_START, TOUCH2_END, etc.")
    print("Base mode files:")
    print(f"  0: {args.touch0_base}")
    print(f"  1: {args.touch1_base}")
    print(f"  2: {args.touch2_base}")
    print("Alternate mode files:")
    print(f"  0: {args.touch0_alt}")
    print(f"  1: {args.touch1_alt}")
    print(f"  2: {args.touch2_alt}")

    touch_state = [False, False, False]
    mode = 0
    all_three_active = False

    try:
        while True:
            raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw_line:
                continue

            parsed = parse_line(raw_line)
            if parsed is None:
                continue

            index, event_type = parsed
            if event_type == "START":
                touch_state[index] = True
                if all(touch_state) and not all_three_active:
                    mode ^= 1
                    all_three_active = True
                    print(f"All three touched: switching to mode {mode} ({MODE_NAMES[mode]})")
                play_sound(sounds[mode], index)
                print(f"Touch {index} START -> mode={mode} ({MODE_NAMES[mode]})")
            elif event_type == "END":
                touch_state[index] = False
                if all_three_active and not all(touch_state):
                    all_three_active = False
                    print("All-three touch released")
                print(f"Touch {index} END")

            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()

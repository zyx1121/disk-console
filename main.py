import os
import subprocess

from rich.console import Console


class DiskConsole:
    def __init__(self, device_path, block_index=0):
        self.device_path = device_path
        self.block_index = block_index

        self.console = Console()
        self.console.clear()

        self.open_disk()


    def open_disk(self):
        try:
            self.disk = open(self.device_path, 'rb')
        except FileNotFoundError:
            self.console.print(f'[bold red]Device path {self.device_path} does not exist. Please update the script with the correct device path.[/bold red]')
            return


    def show_block(self):
        self.console.clear()

        self.disk.seek(self.block_index * 512)
        data = self.disk.read(512)
        hex_data = data.hex(' ')

        # Get the console width
        console_width = self.console.width

        # Determine the display width based on the console width
        if console_width >= 96:
            display_width = 96
        elif console_width >= 48:
            display_width = 48
        elif console_width >= 24:
            display_width = 24
        else:
            display_width = 12

        # Format the output to fit the display width
        formatted_data = '\n'.join([hex_data[i:i+display_width] for i in range(0, len(hex_data), display_width)])

        self.console.print(f'[bold cyan]{formatted_data}[/bold cyan]\n')


    def getch(self):
        if os.name == 'nt':
            import msvcrt
            return msvcrt.getch().decode('utf-8')

        else:
            import sys
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


    def wait_input(self):
        while True:
            input = self.getch()

            if input == 'q':
                self.disk.close()
                self.console.clear()
                exit(0)

            elif input == 'l':
                self.block_index += 1
                break

            elif input == 'h':
                if self.block_index > 0:
                    self.block_index -= 1
                break


    def run(self):
        with self.console.status(f'[bold green]{self.device_path} {self.block_index}', spinner='arc') as status:
            while True:
                self.show_block()
                self.wait_input()
                status.update(f'[bold green]{self.device_path} {self.block_index}')


def select_device():
    result = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    disk_devices = [line.split()[0] for line in lines if '/dev/disk' in line]
    for i, disk_device in enumerate(disk_devices):
        print(f'{i}: {disk_device}')
    selected_index = int(input('Select a device: '))
    return disk_devices[selected_index]


def main():
    device_path = select_device()
    disk_console = DiskConsole(device_path, 0)
    disk_console.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)

import os
import subprocess

from rich.console import Console


BLOCK_SIZE = 512
DISPLAY_WIDTHS = [96, 48, 24, 12]


class DiskConsole:
    def __init__(self, device_path, block_index=0):
        self.device_path = device_path
        self.block_index = block_index

        self.console = Console()
        self.console.clear()

        self.open_disk()


    def open_disk(self):
        try:
            if os.name == 'nt':
                # Windows requires the device path to be in the format '\\.\DeviceName'
                self.device_path = r'\\.\\' + self.device_path
            self.disk = open(self.device_path, 'rb')
        except FileNotFoundError:
            self.console.print(f'[bold red]Device path {self.device_path} does not exist. Please update the script with the correct device path.[/bold red]')
            return
        except PermissionError:
            self.console.print(f'[bold red]Permission denied for device path {self.device_path}. Please run the script with the necessary permissions.[/bold red]')
            return


    def show_block(self):
        self.console.clear()

        self.disk.seek(self.block_index * BLOCK_SIZE)
        data = self.disk.read(BLOCK_SIZE)
        hex_data = data.hex(' ')

        # Get the console width
        console_width = self.console.width

        # Determine the display width based on the console width
        for width in DISPLAY_WIDTHS:
            if console_width >= width:
                display_width = width
            break
        else:
            display_width = DISPLAY_WIDTHS[-1]

        # Format the output to fit the display width
        formatted_data = '\n'.join([hex_data[i:i+display_width] for i in range(0, len(hex_data), display_width)])

        self.console.print(f'[bold cyan]{formatted_data}[/bold cyan]\n')


    def wait_cmd(self):
        while True:
            input = getch()

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
                self.wait_cmd()
                status.update(f'[bold green]{self.device_path} {self.block_index}')


def getch():
    if os.name == 'nt':
        import msvcrt
        try:
            return msvcrt.getch().decode('utf-8')
        except UnicodeDecodeError:
            return ''
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


def select_device():
    if os.name == 'nt':
        result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'], capture_output=True, text=True)
        lines = result.stdout.split('\n')[1:-1]
        disk_devices = [line.split()[0] for line in lines if len(line) > 0]
    else:
        result = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        disk_devices = [line.split()[0] for line in lines if '/dev/disk' in line]

    for i, disk_device in enumerate(disk_devices):
        print(f'{i}: {disk_device}')

    while True:
        try:
            selected_index = int(input('Select a device: '))
            if 0 <= selected_index < len(disk_devices):
                return disk_devices[selected_index]
            else:
                print(f'Invalid selection. Please select a number between 0 and {len(disk_devices) - 1}.')
        except ValueError:
            print('Invalid input. Please enter a number.')


def main():
    device_path = select_device()
    DiskConsole(device_path, 0).run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)

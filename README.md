# Disk Monitor

###### Disk HEX Data Monitor

<img width="794" alt="image" src="https://github.com/zyx1121/disk-monitor/assets/98001197/26aaad35-321b-4134-a3ce-ee0241346841">

## Features

- Current Features
  
  - **View Disk Block/Sector HEX Data**: Users can inspect the hexadecimal data of any disk block or sector.
    
- Planned Features
  
  - **Edit Disk HEX Data**: Ability to directly modify the hexadecimal data on the disk.
    
  - **Jump to Index Block/Sector**: Quick navigation to specific blocks or sectors.
    
  - **Clear All Data**: Option to erase all data from the disk view.
    
  - **Fill All Data**: Tool to populate all fields with a specific hex value for testing or initialization purposes.

## Roadmap

- [x] View disk Block/Sector HEX data
- [ ] Edit disk HEX data
- [ ] Jump index Block/Sector
- [ ] Clear all data
- [ ] Fill all data
- [ ] Load script to decode HEX data

## Installation

- **Install from PyPI**
  
  You can install Disk Monitor directly from the Python Package Index using the pip package manager. Open your terminal and run the following command:

  ```bash
  pip install disk-monitor
  ```
 
- **Manual Installation**

  If you prefer to install manually from the source code, first clone or download the repository:

  ```bash
  git clone https://github.com/zyx1121/disk-monitor
  cd disk-monitor
  ```

  Then run the following command in the project root directory:

  ```bash
  pip install .
  ```

  This will install the package and its required dependencies.

## Usage

Once installed, you can start Disk Monitor by entering the following command:

```bash
disk-monitor
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

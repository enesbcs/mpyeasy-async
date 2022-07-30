[![Release downloads](https://img.shields.io/github/downloads/enesbcs/mpyeasy-async/total.svg)]() [![Code size](https://img.shields.io/github/languages/code-size/enesbcs/mpyeasy-async)]() [![Last commit](https://img.shields.io/github/last-commit/enesbcs/mpyeasy-async)]()

# To support the development you can:
- Be a patron at [Patreon](https://www.patreon.com/enesbcs)
- Buy a [coffee](https://ko-fi.com/I3I5UT4H)
- Donate by [PayPal](https://www.paypal.me/rpieasy)
- Adding Python code by [Pull Request](https://github.com/enesbcs/mpyeasy-async/pulls)

# mPyEasy-Async

microPythonEasy IoT firmware for [W5100S-EVB-Pico](https://www.wiznet.io/product-item/w5100s-evb-pico/), [Pico-W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w), ESP32-WROOM and ESP32-WROVER (with SPIRAM)

Based on MicroPython this project tries to mimic the magnificent [ESPEasy](https://www.letscontrolit.com/wiki/index.php/ESPEasy) project functions. Python code is heavily based on RPIEasy, partially rewritten from mPyEasy dropping threading and implementing AsyncIO with a very basic Web framework with minimal memory footprint.
Main goal is to create a multisensor device, that can be install and setup quickly.

:warning:THIS IS A BETA TEST VERSION!:warning:

Expect major changes in later versions that may cause incompatibility with earlier versions!

# ESP32 Installation

1/ Recommended method to write the firmware binary to the flash directly. It will run on either WROOM or WROVER variants.

  Download image from: https://github.com/enesbcs/mpyeasy-async/releases/

- Erase flash at first time on ESP32:

  `esptool.py --port /dev/ttyUSB0 erase_flash`
- Write firmware:

  `esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 firmware.bin`

Or you can simply use [Thonny](https://thonny.org/) to install firmware!

2/ MicroPython source code from the src directory can be copied to the flash onto a WROVER module with 4MB PSRAM! 
Without PSRAM it may run out of memory, i warned you!

https://github.com/enesbcs/mpyeasy-async/tree/main/src

# RP2 (Pico) Installation

- Download image from: https://github.com/enesbcs/mpyeasy-async/releases/
- Press the Bootsel button on Pico when connecting to USB, it will open a new Drive.
- Copy the .uf2 image to this drive (suitable for your device)

# Setup (WiFi modells)

- Connect to mpyEasy WIFI AP with configesp password.
- Setup your own wifi data at http://192.168.4.1/config
- Search it on your own network and configure at the obtained dhcp IP with a web browser.

# Setup (LAN modells)

- Connect to a router with LAN cable, it will request a DHCP address
- Search it on your own network and configure at the obtained dhcp IP with a web browser.

# Update

OTA is not supported yet on ESP32, and never will be on RP2

# Compiling

To create firmware image from python sources, follow instructions for compiling standard MicroPython and add mPyEasy source to micropython/ports/esp32/modules subdirectory before "make" command.

https://github.com/micropython/micropython/tree/master/ports/esp32

https://blog.horan.hk/micropythonesp32.html

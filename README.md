# Python nRF52 OTA DFU Controller

This is my fork of mdxs's fork of astronomer80's fork of foldedtoad's Python OTA DFU utility. 
The goal of this fork is to achieve:

* Python3 support
* Work with the secure bootloader of nRF SDK15+

## What does it do?

This is a Python program that uses `gatttool` (provided with the Linux BlueZ driver) to achieve Over The Air (OTA) Device Firmware Updates (DFU) to a Nordic Semiconductor nRF52 device via Bluetooth Low Energy (BLE).

### Main features:

* Perform OTA DFU to an nRF5 peripheral without an external USB BLE dongle.
* Ability to detect if the peripheral is running in application mode or bootloader, and automatically switch if needed (buttonless).
* Support for Secure bootloader.

## Prerequisites

* BlueZ 5.4 or above
* Python 3 (tested with 3.9)
* Python `pexpect` module (available via pip)
* Python `intelhex` module (available via pip)

## Usage

Generate your DFU package using `nrfutil` and run the dfu script.

## Usage Examples

    $ python3 dfu.py -z firmware.zip -a CD:E3:4A:47:1C:E4

You can use the `hcitool lescan` to figure out the address of a DFU target, for example:

    $ sudo hcitool -i hci0 lescan
    LE Scan ...
    CD:E3:4A:47:1C:E4 <TARGET_NAME>
    CD:E3:4A:47:1C:E4 (unknown)


## Example Output

    $ python3 dfu.py -z firmware.zip -a CD:E3:4A:47:1C:E4 --secure

    ================================
    ==                            ==
    ==         DFU Server         ==
    ==         Jurpp Fork         ==
    ==                            ==
    ================================

    Sending file firmware.bin to CD:E3:4A:47:1C:E4
    Binary imge size: 177280
    Binary CRC32: 2822816268
    Connecting to CD:E3:4A:47:1C:E4
    Checking DFU State...
    Init packet successfully transfered
    Max object size: 4096, num objects: 44, offset: 0, total size: 177280
    Progress: |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 100.0% Complete (177280 of 177280 bytes)

    Upload complete in 2 minutes and 42 seconds
    DFU Server done

## TODO:

* Fix switching to bootloader using buttonless DFU
* Remove unused legacy mode


## Info & References

* [Nordic Legacy DFU Service](http://infocenter.nordicsemi.com/topic/com.nordic.infocenter.sdk5.v11.0.0/bledfu_transport_bleservice.html?cp=4_0_3_4_3_1_4_1)
* [Nordic Legacy DFU sequence diagrams](http://infocenter.nordicsemi.com/topic/com.nordic.infocenter.sdk5.v11.0.0/bledfu_transport_bleprofile.html?cp=4_0_3_4_3_1_4_0_1_6#ota_profile_pkt_rcpt_notif)
* [Nordic Secure DFU bootloader](http://infocenter.nordicsemi.com/topic/com.nordic.infocenter.sdk5.v12.2.0/lib_dfu_transport_ble.html?cp=4_0_1_3_5_2_2)
* [nrfutil](https://github.com/NordicSemiconductor/pc-nrfutil)

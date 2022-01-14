#!/usr/bin/env python3
"""
------------------------------------------------------------------------------
 DFU Server for Nordic nRF52 based systems.
 Conforms to nRF51_SDK 15.3 BLE_DFU requirements.
------------------------------------------------------------------------------
"""
import os, re
import sys
import argparse
import time
import math
import traceback

from unpacker import Unpacker

from ble_secure_dfu_controller import BleDfuControllerSecure

def main():

    init_msg =  """
    ================================
    ==                            ==
    ==         DFU Server         ==
    ==         Jurpp Fork         ==
    ==                            ==
    ================================
    """

    unpacker = None
    hexfile  = None
    datfile  = None

    print(init_msg)

    parser = argparse.ArgumentParser(usage='dfu.py <zip_file> <dfu_target_address>\n\nExample:\n\tdfu.py ./firmware.zip cd:e3:4a:47:1c:e4')

    parser.add_argument('zipfile')
    parser.add_argument('address')
    args = parser.parse_args()

    try:
        unpacker = Unpacker()

        try:
            hexfile, datfile = unpacker.unpack_zipfile(args.zipfile)	
        except Exception as e:
            print("[-]")
            print(e)
            pass


        ble_dfu = BleDfuControllerSecure(args.address.upper(), hexfile, datfile)

        # Initialize inputs
        ble_dfu.input_setup()

        # Connect to peer device. Assume application mode.
        if ble_dfu.scan_and_connect():
            if not ble_dfu.check_DFU_mode():
                print("[i] Target needs to switch to DFU mode")
                success = ble_dfu.switch_to_dfu_mode()
                if not success:
                    print("[-] Couldn't reconnect")
                    unpacker.delete()
                    sys.exit(1)
        else:
            # The device might already be in DFU mode (MAC + 1)
            ble_dfu.target_mac_increase(1)

            # Try connection with new address
            print("[-] Couldn't connect trying DFU MAC next...")
            if not ble_dfu.scan_and_connect():
                print("[-] Can't connect to device")
                unpacker.delete()
                sys.exit(1)

        ble_dfu.start()

        # Disconnect from peer device if not done already and clean up.
        ble_dfu.disconnect()

    except Exception as e:
        # print traceback.format_exc()
        print("[-] Exception at line {}: {}".format(sys.exc_info()[2].tb_lineno, e))
        pass

    # Delete temporary files
    unpacker.delete()


if __name__ == '__main__':

    # Do not litter the world with broken .pyc files.
    sys.dont_write_bytecode = True

    main()

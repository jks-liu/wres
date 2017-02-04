"""Set/Get Winsows Timer Resolution"""

from contextlib import contextmanager
import ctypes
from ctypes import byref
import logging
import os


__version__ = '1.0.0'
__author__ = 'Meme Kagurazaka'

#pylint: disable=invalid-name


ntdll = ctypes.WinDLL('NTDLL.DLL')

def query_resolution():
    """Query resolution of system timer

    Return a tuple of (min, max, current) resolution, in 100-ns units.
    Ref to NtQueryTimerResolution
    http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FTime%2FNtQueryTimerResolution.html
    """
    MinimumResolution = ctypes.c_ulong()
    MaximumResolution = ctypes.c_ulong()
    CurrentResolution = ctypes.c_ulong()

    ntdll.NtQueryTimerResolution(
        byref(MinimumResolution),
        byref(MaximumResolution),
        byref(CurrentResolution)
    )

    return (MinimumResolution.value,
            MaximumResolution.value,
            CurrentResolution.value)


@contextmanager
def set_resolution(DesiredResolution=0):
    """Set resolution of system timer

    Input:
    DesiredResolution[default 0], in 100-ns units.
    This function will auto revision the value if it is out of range,
    so default 0 means set maximum resolution.

    Should be used in `with' statement, target is current resolution,
    in 100-ns units.
    """
    minres, maxres, _ = query_resolution()
    DesiredResolution = min(DesiredResolution, minres)
    DesiredResolution = max(DesiredResolution, maxres)

    CurrentResolution = ctypes.c_ulong()
    ntdll.NtSetTimerResolution(
        DesiredResolution,
        1,
        byref(CurrentResolution)
    )
    logging.info('Set resolution to %lu * 100-ns', DesiredResolution)

    yield CurrentResolution.value

    ntdll.NtSetTimerResolution(
        DesiredResolution,
        0,
        byref(CurrentResolution)
    )
    logging.info('Reset previously setted resolution')


def main():
    """Entry point of windows-resolution

    Show current system timer resolution without command.
    Type `windows-resolution --help' to see other options.
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', help='set resolution in 100-ns units',
                        type=int, metavar='RESOLUTION')
    parser.add_argument('--setmax', help='set maximum resolution',
                        action='store_true')
    parser.add_argument('--setmin', help='set minimum resolution',
                        action='store_true')
    parser.add_argument('-v', '--version', help='show version',
                        action='store_true')
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    if args.version:
        return logging.info("""windows-resolution from wres version v%s

Meme Kagurazaka releases it under Public Domain.
https://github.com/jks-liu/wres
pip install wres""", __version__)

    minres, maxres, curres = query_resolution()

    if args.setmax:
        res = maxres
    elif args.setmin:
        res = minres
    elif args.set is None:
        logging.info("Mininum resolution %9.4f ms", float(minres)/10000)
        logging.info("Maximum resolution %9.4f ms", float(maxres)/10000)
        logging.info("Current resolution %9.4f ms", float(curres)/10000)
        return
    else:
        res = args.set

    with set_resolution(res) as cur:
        logging.info("Current resolution %.4f ms", float(cur)/10000)
        logging.info("Press any key to reset previous resolution and exit")
        os.system('pause')

"""Set/Get Winsows Timer Resolution"""

from contextlib import contextmanager
import ctypes
from ctypes import byref
import logging


__version__ = '0.0.1'
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
    DesiredResolution, in 100-ns units.
    Should be used in `with' statement, target is previous resolution,
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

    yield CurrentResolution.value

    ntdll.NtSetTimerResolution(
        DesiredResolution,
        0,
        byref(CurrentResolution)
    )


def main():
    logging.basicConfig(level=logging.DEBUG)
    def print_info():
        [minres, maxres, curres] = [float(x)/10000 for x in query_resolution()]
        logging.info("Mininum resolution %9.4f ms", minres)
        logging.info("Maximum resolution %9.4f ms", maxres)
        logging.info("Current resolution %9.4f ms", curres)

    print_info()
    with set_resolution(7000):
        print_info()
    print_info()

                                ━━━━━━━━
                                 README
                                ━━━━━━━━


Table of Contents
─────────────────

1 wres
.. 1.1 Install
.. 1.2 Usage
.. 1.3 Util
.. 1.4 details
..... 1.4.1 `set_resolution'
..... 1.4.2 `query_resolution'
.. 1.5 License


1 wres
══════

  Set/Get Winsows Timer Resolution.

  wres is short for Windows RESolution.

  The function of this module is like Windows API [timeBeginPeriod] and
  [timeEndPeriod].  But the implementation used Undocumented
  [NtSetTimerResolution] of NTDLL. It offers microsecond level control.


  [timeBeginPeriod]
  https://msdn.microsoft.com/en-us/library/dd757624(VS.85).aspx

  [timeEndPeriod]
  https://msdn.microsoft.com/en-us/library/dd757626(v%3Dvs.85).aspx

  [NtSetTimerResolution]
  http://undocumented.ntinternals.net/index.html?page%3DUserMode%252FUndocumented%2520Functions%252FTime%252FNtSetTimerResolution.html


1.1 Install
───────────

  ┌────
  │ pip install wres
  └────


1.2 Usage
─────────

  ┌────
  │ import wres
  │
  │ # Query windows timer resolution in 100-ns units
  │ minres, maxres, curres = wres.query_resolution()
  │
  │ # Set resolution to 1.5 ms
  │ # Automatically restore previous resolution when exit with statement
  │ with wres.set_resolution(15000):
  │     pass
  │
  │ # Set resolution to max resolution
  │ with wres.set_resolution():
  │     pass
  └────


1.3 Util
────────

  After installing `wres', command `windows-resolution' is available.
  ┌────
  │ usage: windows-resolution [-h] [-s RESOLUTION] [--setmax] [--setmin] [-v]
  │
  │ Set system timer tesolution. Show current system timer resolution without
  │ argument.
  │
  │ optional arguments:
  │ -h, --help            show this help message and exit
  │     -s RESOLUTION, --set RESOLUTION
  │     set resolution in 100-ns units
  │     --setmax              set maximum resolution
  │     --setmin              set minimum resolution
  │     -v, --version         show version
  └────


1.4 details
───────────

1.4.1 `set_resolution'
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Set resolution of system timer.

  Input:
      `DesiredResolution' [default 0], in 100-ns units.  This function
  will auto revision the value if it is out of range, so default 0 means
  set maximum resolution.

  Should be used in `with' statement, target is current resolution, in
  100-ns units.


1.4.2 `query_resolution'
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  Query resolution of system timer.

  Return a tuple of (min, max, current) resolution, in 100-ns units.
  Ref to [NtQueryTimerResolution].


  [NtQueryTimerResolution]
  http://undocumented.ntinternals.net/index.html?page%3DUserMode%252FUndocumented%2520Functions%252FTime%252FNtQueryTimerResolution.html


1.5 License
───────────

  Meme Kagurazaka (c) 2017, Public Domain.

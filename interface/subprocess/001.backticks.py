import subprocess

# --- replacing shell backticks ---
# https://docs.python.org/2/library/subprocess.html#replacing-bin-sh-shell-backquote
#   output=`mycmd myarg`
#   output = check_output(["mycmd", "myarg"])
# not true, because mycmd is not passed to shell
try:
    output = subprocess.check_output(["mycmd", "myarg"], shell=True)
except OSError as ex:
    # command not found.
    # it is impossible to catch output here, but shell outputs
    # message to stderr, which backticks doesn't catch either
    output = ''
except subprocess.CalledProcessError as ex:
    output = ex.output
# ^ information about error condition is lost
# ^ output in case of OSError is lost

# ux notes:
# - `mycmd myarg` > ["mycmd", "myarg"]
# - `` is invisible
#   subprocess.check_output is hardly rememberable
# - exception checking is excessive and not needed
#   (common pattern is to check return code)


def backticks(command):
   '''
   Execute `command` and return output.
   - no return code
   - no stderr capture
   - bailed out with MemoryError on Windows with 500Mb of output
   '''
   try:
       # this doesn't escape shell patterns, such as:
       # ^ (windows cmd.exe shell)
       output = subprocess.check_output(command, shell=True)
   except OSError as ex:
       # command not found.
       # it is impossible to catch output here, but shell outputs
       # message to stderr, which backticks doesn't catch either
       output = ''
   except subprocess.CalledProcessError as ex:
       output = ex.output
   return output

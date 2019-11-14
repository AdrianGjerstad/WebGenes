#!/usr/bin/env python3

#
# genes.py
#
# Copyright (c) Adrian Gjerstad. Project Licensed Under GNU GPLv3
# You can get yourself a copy of the license at:
#
#   https://github.com/AdrianGjerstad/WebGenes/blob/master/LICENSE
#

########################################
# IMPORTS                              #
########################################

# A-Z STDLIB
from http.server import HTTPServer, BaseHTTPRequestHandler
import ipaddress
import multiprocessing
import os
import sys

# A-Z WEBGENESLIB
from webgenes_path import wg_PATH
from webgenes_exco import wg_ExitCodes

########################################
# WEBGENES REQUEST HANDLER             #
########################################

class wg_WebGenesRequestHandler(BaseHTTPRequestHandler):
  pass

########################################
# WEBGENES SERVER                      #
########################################

class wg_WebGenesServer(HTTPServer):
  pass

########################################
# SERVER SPAWNER                       #
########################################

global httpd
httpd = None
global configurations
configurations = {}

def wg_ServerSpawner():
  global httpd
  global configurations

  httpd = wg_WebGenesServer((configurations.get('ip', '127.0.0.1'), configurations.get('port', 4180)), wg_WebGenesRequestHandler)

  try:
    print('\033[36mServing HTTP at %s:%i...\033[0m' % (configurations.get('ip', '127.0.0.1'), configurations.get('port', 4180)))
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.shutdown()

########################################
# STATUS CHECKER                       #
########################################

def wg_CheckStatus():
  print('WebGenes script checks in progress...')
  print('   0%  ~~~~~~~~~~~~~~~~~~~~')

  if len(sys.argv) == 1:
    print('\033[A\033[AWebGenes script checks failed.\033[K\n   0%  \033[1m\033[31m----------\033[0m~~~~~~~~~~')
    print('WebGenes requires 1 argument; the path to the configuration script.')
    sys.exit(203)
  elif len(sys.argv) > 2:
    print('\033[A\033[AWebGenes script checks failed.\033[K\n   0%  \033[1m\033[31m----------\033[0m~~~~~~~~~~')
    print('WebGenes takes only 1 argument; the path to the configuration script.')
    sys.exit(203)

  print('\033[A  50%  \033[1m\033[32m++++++++++\033[0m~~~~~~~~~~')

  if not os.path.isfile(sys.argv[1]):
    print('\033[A\033[AWebGenes script checks failed.\033[K\n   50%  \033[1m\033[32m++++++++++\033[31m----------\033[0m')
    print('WebGenes was not given a configuration script path that existed as a file.')
    sys.exit(204)

  print('\033[A\033[AWebGenes script checks completed.\033[K\n 100%  \033[1m\033[32m++++++++++++++++++++\033[0m')

########################################
# SUDO CHECK                           #
########################################

wg_SuperUser = os.getuid() == 0

########################################
# CONFIGURATION SCRIPT STDLIB          #
########################################

_wg_config_sudo = not not wg_SuperUser
global _wg_fixed_path
_wg_fixed_path = ''

def _wg_set_ip(value):
  configurations['ip'] = str(ipaddress.ip_network(value, strict=False).network_address)

  return value

def _wg_set_port(value):
  if isinstance(value, int):
    if value <= 1023 and not wg_SuperUser:
      raise ValueError('Port %i is a priveleged port; cannot open without sudo. web::ERR_CONFIG_NONSUDO_PRIVELEGED_PORT' % value)
    else:
      configurations['port'] = value
  else:
    try:
      if int(value, base=0) <= 1023 and not wg_SuperUser:
        raise ValueError('Port %i is a priveleged port; cannot open without sudo. web::ERR_CONFIG_NONSUDO_PRIVELEGED_PORT' % value)
      else:
        configurations['port'] = int(value, base=0)
    finally:
      pass

  return value

def _wg_set_public(value):
  if not os.path.isdir((_wg_fixed_path if not value.startswith('/') else '') + value):
    raise ValueError('There is no directory at %s. web::ERR_CONFIG_NO_DIR' % os.path.abspath((_wg_fixed_path if _wg_config_fix_pwd else '') + value))
  configurations['public'] = os.path.abspath((_wg_fixed_path if _wg_config_fix_pwd else '') + value)

  return value

def _wg_config_configure(attr, value):
  global configurations
  global _wg_fixed_path

  if attr == 'ip':
    configurations['ip'] = str(ipaddress.ip_network(value, strict=False).network_address)
  elif attr == 'port':
    if isinstance(value, int):
      if value <= 1023 and not wg_SuperUser:
        raise ValueError('Port %i is a priveleged port; cannot open without sudo. web::ERR_CONFIG_NONSUDO_PRIVELEGED_PORT' % value)
      else:
        configurations['port'] = value
    else:
      try:
        if int(value, base=0) <= 1023 and not wg_SuperUser:
          raise ValueError('Port %i is a priveleged port; cannot open without sudo. web::ERR_CONFIG_NONSUDO_PRIVELEGED_PORT' % value)
        else:
          configurations['port'] = int(value, base=0)
      finally:
        pass
  elif attr == 'public':
    if not os.path.isdir((_wg_fixed_path if not value.startswith('/') else '') + value):
      raise ValueError('There is no directory at %s. web::ERR_CONFIG_NO_DIR' % os.path.abspath((_wg_fixed_path if _wg_config_fix_pwd else '') + value))
    configurations['public'] = os.path.abspath((_wg_fixed_path if _wg_config_fix_pwd else '') + value)
  else:
    raise NameError('Cannot resolve attribute name %s. web::ERR_CONFIG_ATTR_NOT_RESOLVED' % (str(attr)))

  return value

def _wg_stdout(*args, sep=' ', end='\n', intro='WebGenes Script Output > '):
  sys.stdout.write(intro)
  sys.stdout.write(sep.join(list(args)) + end)
  sys.stdout.flush()

def _wg_stderr(*args, sep=' ', end='\n', intro='WebGenes Script Error > '):
  sys.stderr.write(intro)
  sys.stderr.write(sep.join(list(args)) + end)
  sys.stderr.flush()

def _wg_stdin(*args, sep=' ', intro='WebGenes Script Input > '):
  sys.stdout.write(intro)
  sys.stdout.write(sep.join(list(args)))
  sys.stdout.flush()

  return sys.stdin.readline().strip('\r\n')

wg_ConfigGlobals = {
  '__builtins__': {}
}

wg_ConfigLocals = {
  'BaseException': BaseException,
  'Exception': Exception,
  'TypeError': TypeError,
  'StopAsyncIteration': StopAsyncIteration,
  'StopIteration': StopIteration,
  'GeneratorExit': GeneratorExit,
  'SystemExit': SystemExit,
  'KeyboardInterrupt': KeyboardInterrupt,
  'OSError': OSError,
  'EnvironmentError': EnvironmentError,
  'IOError': IOError,
  'EOFError': EOFError,
  'RuntimeError': RuntimeError,
  'RecursionError': RecursionError,
  'NotImplementedError': NotImplementedError,
  'NameError': NameError,
  'UnboundLocalError': UnboundLocalError,
  'AttributeError': AttributeError,
  'SyntaxError': SyntaxError,
  'IndentationError': IndentationError,
  'TabError': TabError,
  'LookupError': LookupError,
  'IndexError': IndexError,
  'KeyError': KeyError,
  'ValueError': ValueError,
  'UnicodeError': UnicodeError,
  'UnicodeEncodeError': UnicodeEncodeError,
  'UnicodeDecodeError': UnicodeDecodeError,
  'UnicodeTranslateError': UnicodeTranslateError,
  'AssertionError': AssertionError,
  'ArithmeticError': ArithmeticError,
  'FloatingPointError': FloatingPointError,
  'OverflowError': OverflowError,
  'ZeroDivisionError': ZeroDivisionError,
  'SystemError': SystemError,
  'ReferenceError': ReferenceError,
  'MemoryError': MemoryError,
  'BufferError': BufferError,
  'Warning': Warning,
  'UserWarning': UserWarning,
  'DeprecationWarning': DeprecationWarning,
  'PendingDeprecationWarning': PendingDeprecationWarning,
  'SyntaxWarning': SyntaxWarning,
  'RuntimeWarning': RuntimeWarning,
  'FutureWarning': FutureWarning,
  'UnicodeWarning': UnicodeWarning,
  'BytesWarning': BytesWarning,
  'ResourceWarning': ResourceWarning,
  'ConnectionError': ConnectionError,
  'BlockingIOError': BlockingIOError,
  'BrokenPipeError': BrokenPipeError,
  'ChildProcessError': ChildProcessError,
  'ConnectionAbortedError': ConnectionAbortedError,
  'ConnectionRefusedError': ConnectionRefusedError,
  'ConnectionResetError': ConnectionResetError,
  'FileExistsError': FileExistsError,
  'FileNotFoundError': FileNotFoundError,
  'IsADirectoryError': IsADirectoryError,
  'NotADirectoryError': NotADirectoryError,
  'InterruptedError': InterruptedError,
  'PermissionError': PermissionError,
  'ProcessLookupError': ProcessLookupError,
  'TimeoutError': TimeoutError,
  'string': str,
  'canon': repr,
  'int': int,
  'float': float,
  'bool': bool,
  'array': list,
  'istype': isinstance,
  'typeof': lambda x: type(x).__name__,
  'configure': _wg_config_configure,
  'SUDO': _wg_config_sudo,
  'isfile': os.path.isfile,
  'isdir': os.path.isdir,
  'absolute_path': os.path.abspath,
  'relative_path': os.path.relpath,
  'exists': os.path.exists,
  'callable': callable,
  'delattr': delattr,
  'hasattr': hasattr,
  'address': id,
  'length': len,
  'sequence': range,
  'stdout': _wg_stdout,
  'stderr': _wg_stderr,
  'stdin': _wg_stdin,
  'set_ip': _wg_set_ip,
  'set_port': _wg_set_port,
  'set_public': _wg_set_public
}

########################################
# RUN CONFIGURATION SCRIPT             #
########################################

def wg_RunConfigurationScript():

  with open(sys.argv[1], 'r') as f:
    data = f.read()

    try:
      bytecode = compile(data, sys.argv[1], 'exec', dont_inherit=True)

      exec(bytecode, wg_ConfigGlobals, wg_ConfigLocals)
    except Exception as e:
      print('\033[1m\033[31mAn uncaught error occured in config script.\n')
      import traceback
      traceback.print_exc()
      print('\033[0m', end='')

      sys.exit(100)

########################################
# MAIN                                 #
########################################

def wg_Main():
  global configurations

  print('\033[1m\033[33mStart WebGenes Script\033[0m')

  global _wg_fixed_path
  _wg_fixed_path = os.path.dirname(sys.argv[1]) + '/'

  wg_RunConfigurationScript()

  server_process = multiprocessing.Process(target=wg_ServerSpawner)
  server_process.start()

  try:
    server_process.join()
  except KeyboardInterrupt:
    print('\033[G\033[K\033[36mStop serving HTTP at %s:%i...\033[0m' % (configurations.get('ip', '127.0.0.1'), configurations.get('port', 4180)))

    server_process.terminate()
    server_process.join()

    print('\033[36mStopped serving\033[0m')

  return 0

########################################
# __NAME__ GUARD                       #
########################################

if __name__ == '__main__':
  wg_CheckStatus()

  try:
    exit_code = wg_Main()
    if exit_code is None:
      exit_code = 255
  except Exception:
    print('\033[1m\033[31mAn internal Python3 error occured.\nThe below shows the stack trace and error.\n')
    from traceback import print_exc
    print_exc(file=sys.stdout)
    print('\nThe developers of WebGenes have been notified. You may file an issue on GitHub at\n  https://github.com/AdrianGjerstad/WebGenes/issues.\033[0m')

    # TODO: Create request to file the issue automatically

    exit_code = 254

  print('\033[1m\033[33mExiting WebGenes Script\n\033[0m\033[32m  Code: %i\n  Desc: %s\033[0m' % (exit_code, wg_ExitCodes.get(str(exit_code), 'Unknown exit code')))
  sys.exit(exit_code)

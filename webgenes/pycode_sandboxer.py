def sandbox_globals():
  return {
    '__builtin__': {},
    '__builtins__': {}
  }

def __weed_imports(code):
  res = ''
  changes = False
  for k in code.splitlines(True):
    newline_len = len(k)-len(k.splitlines(False)[0])
    semis = k.split('#')[0].split(';')
    comment = ('' if len(k.split('#')) == 1 else k.split('#')[1])
    for l in semis:
      if l.strip(' \n\r\t;').startswith('import') or l.strip(' \n\r\t;').startswith('from'):
        # Import line
        changes = True
        res += '# Redacted import line: ' + l.strip(' \n\r\t;') + '\n'
      else:
        if l != semis[-1]:
          res += l + ';'
        else:
          if len(l) >= newline_len:
            res += l[:-1*newline_len] + ((' ' if len(l[:-1*newline_len]) > 0 else '') + '#' if len(comment) > 0 else '') + comment + l[-1*newline_len:]
          else:
            res += ((' ' if len(l[:-1*newline_len]) > 0 else '') + '#' if len(comment) > 0 else '') + comment
  
  return res, changes

def sandbox(code, *args, **kwargs):
  active_edits_made = False

  filename = kwargs.get('__filename__', '<unknown-file>')
  mode = kwargs.get('__mode__', 'exec')
  if mode not in ['exec', 'eval', 'single']:
    mode = 'exec'
    raise Warning('Viable modes: exec, eval, single')
  
  if kwargs.get('_import_', True) != True:
    # TODO: Weed out imports from code
    code, sandboxed = __weed_imports(code)
    if sandboxed:
      active_edits_made = True
    pass
  
  code_obj = compile(code, filename, mode, dont_inherit=not kwargs.get('__inherit__', True))

  return code, code_obj, active_edits_made
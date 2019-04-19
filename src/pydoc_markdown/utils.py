
import nr.config
import pkg_resources


def import_object(name):
  module, member = name.rpartition('.')[::2]
  module = __import__(module, fromlist=[None])
  try:
    return getattr(module, member)
  except AttributeError:
    raise ImportError('Module "{}" has no member "{}"'.format(module, member))


def load_entry_point(group, name):
  """
  Returns the first entry point registered to the specified *group* that
  matches the *name*. If multiple entry points are registered to that name,
  an #EnvironmentError is raised.

  If no entry point with the specified *name* can be found, a #ValueError
  is raised instead.
  """

  result = None
  for ep in pkg_resources.iter_entry_points(group, name):
    if result is not None:
      raise EnvironmentError('multiple entry points registered to {}:{}'
        .format(group, name))
    result = ep
  if result is None:
    raise ValueError('no entry point registered to {}:{}'.format(group, name))
  return result


class Configurable(object):

  config_class = None

  def __init__(self, config):
    assert self.config_class is not None, type(self)
    self.config = nr.config.extract(self.config_class, config)

  def iter_options(self):
    for option in self.options:
      if len(option) == 2:
        name, type_, default = option[0], option[1], NotImplemented
      else:
        name, type_, default = option
      yield (name, type_, default)

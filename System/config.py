import json

class Configuration():
  def __init__(self, config_json_file='config.json'):
    self.config_json_file = config_json_file
    config_file = open(self.config_json_file)
    self.config = json.load(config_file)
    config_file.close()

  def get(self, key, default=None, store=True):
    """Get the value of a configuration key

    Parameters:
      key <str> Name of the configuration key
      default <object> value to return (and store) if key is not defined in configuration
      store <boolean> if key does not exist in configuration, and default is specified, the value specified as default will be stored in the configuration.
    """

    if key in self.config:
      return self.config[key]
    
    if default is not None:
      if store:
        self.config[key] = default
      return default 
    
    return None

  def set(self, key, value):
    self.config[key] = value
 
  def save(self):
    config_file = open(self.config_json_file, 'w')
    config_file.write( json.dumps(self.config) )
    config_file.close()

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit



def drupal_get_header():
  import urllib2
  from pylons import config
  navigation = urllib2.urlopen(config.get('drupal.site_url') + '/koop_theme/get/header')
  return navigation.read().decode('utf-8')



def drupal_get_secondary_header():
  import urllib2
  from pylons import config
  secondary_header = urllib2.urlopen(config.get('drupal.site_url') + '/koop_theme/get/secondary_header')
  return secondary_header.read().decode('utf-8')



def drupal_get_footer():
  import urllib2
  from pylons import config
  footer = urllib2.urlopen(config.get('drupal.site_url') + '/koop_theme/get/footer')
  return footer.read().decode('utf-8')



def drupal_site_url():
  from pylons import config
  return config.get('drupal.site_url')

  
def is_format_an_webserivce(val):
  '''Depricated function'''
  return False



def is_format_downloadable(val):
  '''Add all the cases where the value is downloadable.'''
  var = val.lower();
  
  if 'zip' in var:
    return True
  elif 'html' in var:
    return True
  elif 'csv' in var:
    return True
  elif 'pdf' in var:
    return True
  elif 'download' in var:
    return True
  elif 'xls' in var:
    return True
  elif 'ods' in var:
    return True
  elif 'mdb' in var:
    return True
  elif 'dbf' in var:
    return True
  elif 'txt' in var:
    return True
  elif 'xsd' in var:
    return True
  elif 'kml' in var:
    return True
  else:
    return False


class ThemePlugin(plugins.SingletonPlugin):
  ''' Koop theme plugin for CKAN '''

  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)

  def update_config(self, config):
    '''Add this plugin's templates dir to CKAN's extra_template_paths,
    so that CKAN will use this plugin's custom templates.'''
    toolkit.add_template_directory(config, 'templates')

  def get_helpers(self):
    '''Register the drupal_get_menu() function above as a template
    helper function.'''

    return {'koop_theme_drupal_get_footer': drupal_get_footer,
    'koop_theme_drupal_get_header': drupal_get_header,
    'koop_theme_drupal_get_secondary_header': drupal_get_secondary_header,
    'koop_theme_is_format_an_webserivce' : is_format_an_webserivce,
    'koop_theme_is_format_downloadable' : is_format_downloadable,
    'drupal_site_url': drupal_site_url}

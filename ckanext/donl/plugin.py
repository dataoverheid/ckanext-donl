import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import urllib2

import logging
log = logging.getLogger(__name__)

def drupal_get_dataset_quality(table, id):
  import urllib2
  from pylons import config
  text = urllib2.urlopen(config.get('drupal.site_url') + '/service/linkcheck/' + table + '/' + id)
  return text.read().decode('utf-8')

def drupal_get_formats():
  from pylons import config
  return 'teststring'


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

  
def is_resource_downloadable(val):
  '''Checks whether the given resource is downloadable'''
  
  var = val.lower()
  
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
  elif 'png' in var:
    return True
  elif 'gif' in var:
    return True
  elif 'jpg' in var:
    return True
  else:
    return False

def url_is_valid( url ):
    try:
        u = urllib2.urlopen(url)
        if u.getcode() == 200:
            return True
        else:
            return False
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False

def get_drupal_taxonomie( taxSystemName ):
    from pylons import config
    import requests
    
    try:
        r = requests.get(config.get('drupal.site_url') + '/service/waardelijsten/' + taxSystemName )
        ret = r.json()
    except NotFound:
        ret = []
    
    return ret

def htmlUnescape( strToUnescape ):
    from HTMLParser import HTMLParser
    hp = HTMLParser()
    return hp.unescape( strToUnescape )

def displayNameToSystemName( displayName ):
    return displayName.replace(" ", "_").lower()

def getTabFormats():
    formats = { }
    tabs = get_drupal_taxonomie("dataset_tab_formaten")
    formats[u'All'] = []
    for tab in tabs:
        formats[tab[u'name']] = []
        for kind in tab[u'children']:
            formats[tab[u'name']].append(kind[u'name'].lower())
            formats[u'All'].append(kind[u'name'].lower())
    return formats

def checkForUnknownResources( resources ):
    tabs = getTabFormats()
    allFormats = tabs['Downloads'] + tabs['Webservice'] + tabs['Documentatie'] + tabs['Links']
    for res in resources:
        if res['format'].lower() not in allFormats:
            return True
    return False


def getDatasetAanmeldenTxt( id, totalSet ):
    for item in totalSet:
        if item[u'name'] == id:
            return item[u'description']
    return None

def resourceLinkStatusDiv( status ):
    if status == True:
        return '<div class="dataset-qualtiy"><div class="dataset-quality-1"></div></div>'
    else:
        return '<div class="dataset-qualtiy"><div class="dataset-quality-3"></div></div>'

class ThemePlugin(plugins.SingletonPlugin):
  ''' Koop theme plugin for CKAN '''

  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)

  def update_config(self, config):
    '''Add this plugin's templates dir to CKAN's extra_template_paths,
    so that CKAN will use this plugin's custom templates.'''
    toolkit.add_template_directory(config, 'templates')
    
    toolkit.add_resource('fanstatic', 'donl')
    

  def get_helpers(self):
    '''Register the drupal_get_menu() function above as a template
    helper function.'''

    return {'koop_theme_drupal_get_footer': drupal_get_footer,
    'koop_theme_drupal_get_header': drupal_get_header,
    'koop_theme_drupal_get_secondary_header': drupal_get_secondary_header,
    'koop_theme_is_resource_downloadable' : is_resource_downloadable,
    'drupal_get_dataset_quality' : drupal_get_dataset_quality,
    'drupal_get_formats':drupal_get_formats,
    'drupal_site_url': drupal_site_url,
    'url_is_valid': url_is_valid,
    'get_drupal_taxonomie': get_drupal_taxonomie,
    'htmlUnescape' : htmlUnescape,
    'displayNameToSystemName': displayNameToSystemName,
    'getTabFormats' : getTabFormats,
    'checkForUnknownResources' : checkForUnknownResources,
    'getDatasetAanmeldenTxt' : getDatasetAanmeldenTxt,
    'resourceLinkStatusDiv' : resourceLinkStatusDiv }

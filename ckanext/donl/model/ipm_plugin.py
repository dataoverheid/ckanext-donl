import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.helpers

from datetime import datetime
from ckan.plugins.toolkit import Invalid

import pprint

import json
import requests
import time
import collections
import csv
import os

import logging
log = logging.getLogger(__name__)

# Memoization stuff: https://github.com/mikeboers/PyMemoize
from memoize import Memoizer
store = {}
memo = Memoizer(store)


# Helpers

def hierarchicalarrayofobjects_to_formselectdict(arr, idfield, displayfield, childrenfield):
  #print "hierarchicalarrayofobjects_to_formselectdict(arr, idfield, displayfield, childrenfield)"
  fsd = []
  traverse_arrayofobjects_to_formselectdict(fsd, None, "", arr, idfield, displayfield, childrenfield)
  return fsd
  
def traverse_arrayofobjects_to_formselectdict(fsd, parentvalue, parenttext, arr, idfield, displayfield, childrenfield):
  #print "traverse_arrayofobjects_to_formselectdict(fsd, parentvalue, parenttext, arr, idfield, displayfield, childrenfield)"
  for obj in arr:
    if childrenfield in obj:
      if obj[idfield]:
        fsd.append({'value':obj[idfield], 'text':parenttext + obj[displayfield], 'parent':parentvalue, 'subtext':obj[displayfield]})
      traverse_arrayofobjects_to_formselectdict(fsd, obj[idfield], obj[displayfield] + " | ", obj[childrenfield], idfield, displayfield, childrenfield)
    else:
      fsd.append({'value':obj[idfield], 'text':parenttext + obj[displayfield], 'parent':parentvalue, 'subtext':obj[displayfield]})

def arrayofobjects_to_formselectdict(arr, idfield, displayfield):
  #print "arrayofobjects_to_formselectdict(arr, idfield, displayfield)"
  return map(lambda d:{'value':d[idfield], 'text':d[displayfield]}, arr)

def array_to_formselectdict(arr):
  #print "array_to_formselectdict(arr)"
  return map(lambda v:{'value':v}, arr)

def tuplearray_to_formselectdict(arr):
  #print "tuplearray_to_formselectdict(arr)"
  return map(lambda (k,v):{'value':k, 'text':v}, arr)
    
def sel_to_dict(arr, displayfield = 'text'):
  #print "sel_to_dict(arr, displayfield = 'text')"
  return dict((el['value'],el[displayfield]) for el in arr)

def read_file_to_tuplearray(filename):
  #print "read_file_to_tuplearray(filename)"
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    m = map(tuple, reader)
  return m
  
def read_file_to_formselectdict(filename):
  #print "read_file_to_formselectdict(filename)"
  return tuplearray_to_formselectdict(read_file_to_tuplearray(filename))



# Template helpers

@memo(max_age=60)
def active_users():
  #print "active_users()"
  import ckan.model as model
  query = '''select id, name, fullname, email from "user" where state='active' order by fullname'''
  res = model.Session.execute(query).fetchall()
  active_users = []
  for id, name, fullname, email in res:
    active_users.append({ 'id': id, 'name': name, 'fullname': fullname, 'email': email })
  
  return active_users

@memo(max_age=60)
def maintainers_with_datasets():
  #print "maintainers_with_datasets()"
  import ckan.model as model
  query = '''select maintainer, count(maintainer) from package where state='active' and private=false group by maintainer order by count(maintainer) desc'''
  res = model.Session.execute(query).fetchall()
  maintainers_with_datasets = []
  for maintainer, number_of_datasets in res:
    maintainers_with_datasets.append({ 'maintainer': maintainer, 'number_of_datasets': number_of_datasets })
  
  return maintainers_with_datasets
    

@memo(max_age=60)
def owms_taxonomie_beleidsagenda_hierarchical():
  #print "owms_taxonomie_beleidsagenda_hierarchical()"
  from pylons import config
  try:
    r = requests.get(config.get('drupal.site_url') + '/service/waardelijsten/taxonomiebeleidsagenda')
    owms_taxonomie_beleidsagenda = r.json()
  except NotFound:
    owms_taxonomie_beleidsagenda = []
  
  owms_taxonomie_beleidsagenda.insert(0, {'name':'', 'uri':''})
  
  return owms_taxonomie_beleidsagenda

@memo(max_age=60)
def owms_taxonomie_beleidsagenda():
  #print "owms_taxonomie_beleidsagenda()"
  return hierarchicalarrayofobjects_to_formselectdict(owms_taxonomie_beleidsagenda_hierarchical(), 'uri', 'name', 'children')

@memo(max_age=60)
def owms_taxonomie_overheidsorganisatie():
  #print "owms_taxonomie_overheidsorganisatie()"
  
  owms_taxonomie_overheidsorganisatie = owms_taxonomie_overheidsorganisatie_hierarchical()
  owms_taxonomie_overheidsorganisatie.insert(0, {'name':'', 'uri':''})
  
  return hierarchicalarrayofobjects_to_formselectdict(owms_taxonomie_overheidsorganisatie, 'uri', 'name', 'children')

@memo(max_age=60)
def owms_taxonomie_overheidsorganisatie_hierarchical():
  #print "owms_taxonomie_overheidsorganisatie_hierarchical()"
  from pylons import config
  try:
    r = requests.get(config.get('drupal.site_url') + '/service/waardelijsten/overheidsorganisatie')
    owms_taxonomie_overheidsorganisatie = r.json()
  except NotFound:
    owms_taxonomie_overheidsorganisatie = []
  
  return owms_taxonomie_overheidsorganisatie


@memo(max_age=60)
def owms_frequentie():
  #print "owms_frequentie()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/owms_frequentie.csv')

@memo(max_age=60)
def adms_status():
  #print "adms_status()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/adms_status.csv')

@memo(max_age=60)
def dataset_status():
  #print "dataset_status()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/dataset_status.csv')

@memo(max_age=60)
def accessibility():
  #print "accessibility()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/accessibility.csv')

@memo(max_age=60)
def language():
  #print "language()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/language.csv')

@memo(max_age=60)
def lod_stars():
  #print "lod_stars()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/lod_stars.csv')

@memo(max_age=60)
def distribution_format():
  #print "distribution_format()"
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/distribution_format.csv')

@memo(max_age=60)
def licenses():
  import json

  try:
    with open('/home/ckan/stamdata/donl/donl_licenties.json') as json_file:
      licenses = json.load(json_file)
  except:
    licenses = []
  
  return licenses


# Validators

def date_modified_validator(key, data, errors, context):
  #print "date_modified_validator(key, data, errors, context)"
  ''' date modified must be in dd-mm-yyyy format '''
  
  import ckan.lib.navl.dictization_functions as df
  Invalid = df.Invalid
  
  date_modified = None
  
  for data_key, data_value in data.iteritems():
    if (data_key[0] == key[0]):
      date_modified = data_value
  
  try:
    if date_modified != datetime.strptime(date_modified, "%d-%m-%Y").strftime('%d-%m-%Y'):
      raise Invalid('Niet in dd-mm-jjjj formaat')
  except ValueError:
    raise Invalid('Niet in dd-mm-jjjj formaat')
   


def date_planned_validator(key, data, errors, context):
  #print "date_planned_validator(key, data, errors, context)"
  ''' date_planned is required when status is 'Gepland' of 'In onderzoek' '''

  from pylons import config
  gepland_uri = config.get('donl.business_rules.dataset_status.gepland')
  in_onderzoek_uri = config.get('donl.business_rules.dataset_status.in_onderzoek')

  import ckan.lib.navl.dictization_functions as df
  Invalid = df.Invalid

  dataset_status = None
  date_planned = None
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'dataset_status'):
      dataset_status = data_value
    if (data_key[0] == 'date_planned'):
      date_planned = data_value
  
  if (dataset_status == gepland_uri or dataset_status == in_onderzoek_uri) and (date_planned is None or date_planned == ''):
    raise Invalid('Dit veld moet gevuld zijn indien status Gepland of In onderzoek is.')

def license_id_validator(key, data, errors, context):
  ''' license_id moet bekend zijn in donl_licenties.json '''

  import ckan.lib.navl.dictization_functions as df
  Invalid = df.Invalid
  
  allowed_license_ids = list( item['id'] for item in licenses() )
  license_id = None
  
  for data_key, data_value in data.iteritems():
    if (data_key[0] == key[0]):
      license_id = data_value
  
  if license_id == None or license_id not in allowed_license_ids:
    raise Invalid(str.format("Opgegeven license_id '{0}' is onbekend. Mogelijke waarden: {1}", license_id, ", ".join(allowed_license_ids)))


def accessibility_validator(key, data, errors, context):
  #print "accessibility_validator(key, data, errors, context)"
  ''' accessibility can not be 'Publiek' when license is unknown or not open '''

  from pylons import config
  publiek_uri = config.get('donl.business_rules.accessibility.publiek')
  license_id_uris = config.get('donl.business_rules.license_id.niet_publiek').split()

  import ckan.lib.navl.dictization_functions as df
  Invalid = df.Invalid

  accessibility = None
  license_id = None
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'accessibility'):
      accessibility = data_value
    if (data_key[0] == 'license_id'):
      license_id = data_value
  
  if accessibility == publiek_uri and license_id in license_id_uris:
    raise Invalid('Ongeldige waarde bij huidige licentie.')



def is_sysadmin_or_koop(key, data, errors, context):
  #print "is_sysadmin_or_koop(key, data, errors, context)"
  model = context['model']
  user = context.get('user')
  user_model = model.User.get(user)
  ignore_auth = context.get('ignore_auth')

  return ignore_auth or (user and ckan.authz.is_sysadmin(user)) or (user_model and user_model.fullname == 'beheer')


def ignore_not_sysadmin_or_koop(key, data, errors, context):
  #print "ignore_not_sysadmin_or_koop(key, data, errors, context)"
  '''Ignore the field if user not sysadmin or ignore_auth or KOOP (name 'beheer') in context.'''

  if is_sysadmin_or_koop(key, data, errors, context):
      log.debug('ignore_not_sysadmin_or_koop: authorized, keeping %s', key)
      return

  log.debug('ignore_not_sysadmin_or_koop: not authorized, popping %s', key)
  log.debug('ignore_not_sysadmin_or_koop: data pre-pop: %s', data.get(key))
  data.pop(key)
  log.debug('ignore_not_sysadmin_or_koop: data post-pop: %s', data.get(key))



# Converters / default value providers

def remove_from_extras(data, key):
  to_remove = []
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'extras'
        and data_key[1] == key):
      to_remove.append(data_key)
  for item in to_remove:
    del data[item]


def dataset_status_default(value, context):
  #print "dataset_status_default(value, context)"
  return value or dataset_status()[0].get('value')

def md_wijzigingsdatum_default(value, context):
  #print "md_wijzigingsdatum_default(value, context)"
  return time.strftime("%Y-%m-%d")
  
def md_soortwijziging_default_created(value, context):
  #print "md_soortwijziging_default_created(value, context)"
  return ":created"

def md_soortwijziging_default_updated(value, context):
  #print "md_soortwijziging_default_updated(value, context)"
  return ":updated"

def contact_point_default(value, context):
  #print "contact_point_default(value, context)"
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  return value or user.email

def source_default(value, context):
  #print "source_default(value, context)"
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  return value or user.display_name or user.fullname or user.name or user.id

def owner_org_default(value, context):
  #print "owner_org_default(value, context)"
  return value or ckan.lib.helpers.organizations_available('create_dataset')[0].get('id')
  
def creator_user_id_default(value, context):
  #print "creator_user_id_default(value, context)"
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  return value or user.id


@memo(max_age=60)
def maintainer_from_profile(user_name):
  #print "maintainer_from_profile(user_name)"
  import ckan.model as model
  user = model.User.get(user_name)
  return get_user_extras(user.id).get('donl_data_eigenaar')

@memo(max_age=60)
def author_from_profile(user_name):
  #print "author_from_profile(user_name)"
  import ckan.model as model
  user = model.User.get(user_name)
  return get_user_extras(user.id).get('donl_verstrekker')

@memo(max_age=60)
def email_from_profile(user_name):
  #print "email_from_profile(user_name)"
  import ckan.model as model
  user = model.User.get(user_name)
  return user.email


def maintainer_default(value, context):
  #print "maintainer_default(value, context)"
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  extras = get_user_extras(user.id)
  if user.sysadmin:
    return value or extras.get('donl_data_eigenaar')
  else:
    return extras.get('donl_data_eigenaar') or value

def author_default(value, context):
  #print "author_default(value, context)"
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  extras = get_user_extras(user.id)
  if user.sysadmin:
    return value or extras.get('donl_verstrekker') or None
  else:
    return extras.get('donl_verstrekker') or value or None


def get_user_extras(user_id):
  #print "get_user_extras(user_id)"
  ''' Depends on ckanext-userextra plugin. '''
  from ckanext.userextra.model import UserExtra
  existing_extras = UserExtra.get_extra(user_id)
  return existing_extras


def maintainer_facet_default(key, data, errors, context):
  #print "maintainer_facet_default(key, data, errors, context)"
  # Simply copies the maintainer uri to the maintainer_facet field
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'maintainer'):
      data[(key[0],)] = data_value
      break


def theme_facet_default(key, data, errors, context):
  #print "theme_facet_default(key, data, errors, context)"
  uri = None
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'theme'):
      uri = data_value
      break

  for obj in owms_taxonomie_beleidsagenda():
    if (obj.get('value') == uri):
      data[(key[0],)] = obj.get('parent') or obj.get('value')
      break

def subtheme_facet_default(key, data, errors, context):
  #print "subtheme_facet_default(key, data, errors, context)"
  uri = None
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'theme'):
      uri = data_value
      break

  for obj in owms_taxonomie_beleidsagenda():
    if (obj.get('value') == uri):
      if obj.get('parent'):
        data[(key[0],)] = uri
      else:
        data[(key[0],)] = None
      break

def maintainer_displayname_default(key, data, errors, context):
  #print "maintainer_displayname_default(key, data, errors, context)"
  uri = None
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'maintainer'):
      uri = data_value
      break

  for obj in owms_taxonomie_overheidsorganisatie():
    if (obj.get('value') == uri):
      data[(key[0],)] = obj.get('text')
      break
  
def theme_displayname_default(key, data, errors, context):
  #print "theme_displayname_default(key, data, errors, context)"
  uri = None
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'theme'):
      uri = data_value
      break

  for obj in owms_taxonomie_beleidsagenda():
    if (obj.get('value') == uri):
      data[(key[0],)] = obj.get('text')
      break


def facet_value_displayname(item, name):
  #print "facet_value_displayname(item, name)"
  label = item.get('display_name', item.get('name')) if isinstance(item, dict) else item
  if (name == 'res_format'):
    return sel_to_dict(distribution_format()).get(label, label)
  elif (name == 'language'):
    return sel_to_dict(language()).get(label, label)
  elif (name == 'maintainer_facet'):
    return sel_to_dict(owms_taxonomie_overheidsorganisatie(), 'subtext').get(label, label)
  elif (name == 'theme_facet'):
    return sel_to_dict(owms_taxonomie_beleidsagenda()).get(label, label)
  elif (name == 'subtheme_facet'):
    return sel_to_dict(owms_taxonomie_beleidsagenda(), 'subtext').get(label, label)
  elif (name == 'dataset_status'):
    return sel_to_dict(dataset_status()).get(label, label)
  elif (name == 'accessibility'):
    return sel_to_dict(accessibility()).get(label, label)
  elif (name == 'high_value_dataset'):
    return tk._('Ja') if label in [True, 'true', 'True', 1, '1'] else tk._('Nee')
  else:
    return label





# The actual plugin

class IpmPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
  p.implements(p.IDatasetForm, inherit=True)
  p.implements(p.IConfigurer)
  p.implements(p.ITemplateHelpers)
  p.implements(p.IFacets)
  p.implements(p.IPackageController, inherit=True)

  # IPackageController implementations
  def before_search(self, search_params):
    #print "before_search(self, search_params)"
    # Change the default sort
    if search_params.get('sort') in (None, 'rank'):
        search_params['sort'] = 'score desc, modified desc, metadata_modified desc'
    return search_params
    
  # IFacets implementations
  def dataset_facets(self, facets_dict, package_type):
    #print "dataset_facets(self, facets_dict, package_type)"
    facets_dict['maintainer_facet'] = tk._('Data-eigenaar')
    facets_dict['theme_facet'] = tk._('Thema')
    facets_dict['subtheme_facet'] = tk._('Subthema')
    facets_dict['res_format'] = tk._('Bronformaat')
    facets_dict['organization'] = tk._('Catalogus')
    facets_dict['language'] = tk._('Taal')
    facets_dict['dataset_status'] = tk._('Status')
    facets_dict['accessibility'] = tk._('Toegang')
    facets_dict['high_value_dataset'] = tk._('High value dataset')
    return facets_dict

  def organization_facets(self, facets_dict, organization_type, package_type):
    #print "organization_facets(self, facets_dict, organization_type, package_type)"
    facets_dict['maintainer_facet'] = tk._('Data-eigenaar')
    facets_dict['theme_facet'] = tk._('Thema')
    facets_dict['subtheme_facet'] = tk._('Subthema')
    facets_dict['res_format'] = tk._('Bronformaat')
    facets_dict['organization'] = tk._('Catalogus')
    facets_dict['language'] = tk._('Taal')
    facets_dict['dataset_status'] = tk._('Status')
    facets_dict['accessibility'] = tk._('Toegang')
    facets_dict['high_value_dataset'] = tk._('High value dataset')
    return facets_dict

  def group_facets(self, facets_dict, group_type, package_type):
    #print "group_facets(self, facets_dict, group_type, package_type)"
    facets_dict['maintainer_facet'] = tk._('Data-eigenaar')
    facets_dict['theme_facet'] = tk._('Thema')
    facets_dict['subtheme_facet'] = tk._('Subthema')
    facets_dict['res_format'] = tk._('Bronformaat')
    facets_dict['organization'] = tk._('Catalogus')
    facets_dict['language'] = tk._('Taal')
    facets_dict['dataset_status'] = tk._('Status')
    facets_dict['accessibility'] = tk._('Toegang')
    facets_dict['high_value_dataset'] = tk._('High value dataset')
    return facets_dict


  def get_helpers(self):
    #print "get_helpers(self)"
    # Template helper function names should begin with the name of the
    # extension they belong to, to avoid clashing with functions from
    # other extensions.
    return {
      'donl_owms_taxonomie_beleidsagenda': owms_taxonomie_beleidsagenda,
      'donl_owms_taxonomie_overheidsorganisatie': owms_taxonomie_overheidsorganisatie,
      'donl_owms_taxonomie_overheidsorganisatie_hierarchical': owms_taxonomie_overheidsorganisatie_hierarchical,
      'donl_owms_frequentie': owms_frequentie,
      'donl_adms_status': adms_status,
      'donl_dataset_status': dataset_status,
      'donl_accessibility': accessibility,
      'donl_language': language,
      'donl_lod_stars': lod_stars,
      'donl_distribution_format': distribution_format,
      'donl_sel_to_dict': sel_to_dict,
      'donl_maintainers_with_datasets' : maintainers_with_datasets,
      'donl_active_users' : active_users,
      'donl_facet_value_displayname' : facet_value_displayname,
      'donl_get_user_extras' : get_user_extras,
      'donl_maintainer_from_profile': maintainer_from_profile,
      'donl_author_from_profile': author_from_profile,
      'donl_email_from_profile': email_from_profile,
    }
    

  def _modify_package_resource_schema(self, schema):
    #print "_modify_package_resource_schema(self, schema)"
    schema['resources'].update({
      'download_url': [tk.get_validator('ignore_missing')],
      'modified': [tk.get_validator('ignore_missing')],
      'adms_status': [tk.get_validator('ignore_missing')],
      'issued': [tk.get_validator('ignore_missing')],
      'bytesize': [tk.get_validator('ignore_missing')],
      'link_status': [tk.get_validator('ignore_missing')],
      'is_duplicate_of': [tk.get_validator('ignore_missing')],
    })
    return schema


  def _modify_package_schema(self, schema):
    # Used by create_package_schema() and update_package_schema()
    
    schema.update({
      'identifier': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'title': [tk.get_validator('not_empty')],
      'owner_org': [owner_org_default],
      'creator_user_id': [creator_user_id_default],
      'maintainer': [maintainer_default, tk.get_validator('not_empty')],
      'author': [author_default],
      'notes': [tk.get_validator('not_empty')],
      'license_id': [license_id_validator],
      'high_value_dataset': [tk.get_validator('boolean_validator'), tk.get_converter('convert_to_extras')],
      'modified': [tk.get_validator('not_empty'), tk.get_converter('convert_to_extras')],
      'language': [tk.get_validator('not_empty'), tk.get_converter('convert_to_extras')],
      'theme': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'subtheme': [tk.get_converter('ignore_missing'), tk.get_validator('convert_to_extras')],
      'landingpage': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'spatial': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'temporal_from': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'temporal_to': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'rights': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'accrual_periodicity': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'issued': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'conforms_to': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'version_notes': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'contact_point': [contact_point_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'source': [source_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'lod_stars': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'dataset_status': [dataset_status_default, tk.get_validator('not_empty'), tk.get_converter('convert_to_extras')],
      'md_uri': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'md_uitgiftedatum': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'md_titel': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'md_omschrijving': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'grondslag': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'grondslag_citeertitel': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
        
      'accessibility': [accessibility_validator, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'date_planned': [date_planned_validator, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'access_restrictions_reuse': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'features': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      
      'dataset_quality': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
        
      'maintainer_displayname': [maintainer_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'theme_displayname': [theme_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],

      'maintainer_facet': [maintainer_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'theme_facet': [theme_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'subtheme_facet': [subtheme_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],

      'duplicate_resources': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
    })

    schema = self._modify_package_resource_schema(schema)
    
    #schema.update({
    #  
    #})

    return schema


  def show_package_schema(self):
    #print "show_package_schema(self)"
    # Return a schema to validate datasets before they’re shown to the user.
    #author, creator_user_id
    schema = super(IpmPlugin, self).show_package_schema()
    schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))
    schema.update({
      'identifier': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'title': [tk.get_validator('not_empty')],
      'owner_org': [owner_org_default],
      #'creator_user_id': [creator_user_id_default],
      'maintainer': [tk.get_validator('not_empty')],
      #'author': [author_default],
      'notes': [tk.get_validator('not_empty')],
      'high_value_dataset': [tk.get_converter('convert_from_extras'), tk.get_validator('boolean_validator')],
      'modified': [tk.get_converter('convert_from_extras'), tk.get_validator('not_empty')],
      'language': [tk.get_converter('convert_from_extras'), tk.get_validator('not_empty')],
      'theme': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'subtheme': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'landingpage': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'spatial': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'temporal_from': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'temporal_to': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'rights': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'accrual_periodicity': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'issued': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'conforms_to': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'version_notes': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'contact_point': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'source': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'lod_stars': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'dataset_status': [dataset_status_default, tk.get_converter('convert_from_extras'), tk.get_validator('not_empty')],
      'md_uri': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_soortwijziging': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_uitgiftedatum': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_titel': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_omschrijving': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'grondslag': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'grondslag_citeertitel': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'accessibility': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'date_planned': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'access_restrictions_reuse': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'features': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
        
      'dataset_quality': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
        
      'maintainer_displayname': [maintainer_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')],
      'theme_displayname': [theme_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')],

      'maintainer_facet': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'theme_facet': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'subtheme_facet': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],

      'duplicate_resources': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
    })

    schema = self._modify_package_resource_schema(schema)
    
    #schema.update({
    #  
    #})
    
    return schema


  def create_package_schema(self):
    #print "create_package_schema(self)"
    # Return the schema for validating new dataset dicts.
    
    schema = super(IpmPlugin, self).create_package_schema()
    schema = self._modify_package_schema(schema)
    schema.update({
      'md_soortwijziging': [md_soortwijziging_default_created, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
    })
    return schema


  def update_package_schema(self):
    #print "update_package_schema(self)"
    # Return the schema for validating updated dataset dicts.
    
    schema = super(IpmPlugin, self).update_package_schema()
    schema = self._modify_package_schema(schema)
    schema.update({
      'md_soortwijziging': [md_soortwijziging_default_updated, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],      
    })
    return schema
  
      
  def is_fallback(self):
    #print "is_fallback(self)"
    # Return True to register this plugin as the default handler for
    # package types not handled by any other IDatasetForm plugin.
    return True


  def package_types(self):
    #print "package_types(self)"
    # This plugin doesn't handle any special package types, it just
    # registers itself as the default (above).
    return []
    
    
  def update_config(self, config):
    #print "update_config(self, config)"
    # Add this plugin's templates dir to CKAN's extra_template_paths, so
    # that CKAN will use this plugin's custom templates.
    tk.add_template_directory(config, 'templates')
    
    

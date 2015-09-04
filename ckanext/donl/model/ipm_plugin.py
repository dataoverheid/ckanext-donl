import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.helpers

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
  fsd = []
  traverse_arrayofobjects_to_formselectdict(fsd, None, "", arr, idfield, displayfield, childrenfield)
  return fsd
  
def traverse_arrayofobjects_to_formselectdict(fsd, parentvalue, parenttext, arr, idfield, displayfield, childrenfield):
  for obj in arr:
    if childrenfield in obj:
      if obj[idfield]:
        fsd.append({'value':obj[idfield], 'text':parenttext + obj[displayfield], 'parent':parentvalue, 'subtext':obj[displayfield]})
      traverse_arrayofobjects_to_formselectdict(fsd, obj[idfield], obj[displayfield] + " | ", obj[childrenfield], idfield, displayfield, childrenfield)
    else:
      fsd.append({'value':obj[idfield], 'text':parenttext + obj[displayfield], 'parent':parentvalue, 'subtext':obj[displayfield]})

def arrayofobjects_to_formselectdict(arr, idfield, displayfield):
  return map(lambda d:{'value':d[idfield], 'text':d[displayfield]}, arr)

def array_to_formselectdict(arr):
  return map(lambda v:{'value':v}, arr)

def tuplearray_to_formselectdict(arr):
  return map(lambda (k,v):{'value':k, 'text':v}, arr)
    
def sel_to_dict(arr, displayfield = 'text'):
  return dict((el['value'],el[displayfield]) for el in arr)

def read_file_to_tuplearray(filename):
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    m = map(tuple, reader)
  return m
  
def read_file_to_formselectdict(filename):
  return tuplearray_to_formselectdict(read_file_to_tuplearray(filename))



# Template helpers

@memo(max_age=60)
def active_users():
  import ckan.model as model
  query = '''select id, name, fullname, email from "user" where state='active' order by fullname'''
  res = model.Session.execute(query).fetchall()
  active_users = []
  for id, name, fullname, email in res:
    active_users.append({ 'id': id, 'name': name, 'fullname': fullname, 'email': email })
  
  return active_users

@memo(max_age=60)
def maintainers_with_datasets():
  import ckan.model as model
  query = '''select maintainer, count(maintainer) from package where state='active' and private=false group by maintainer order by count(maintainer) desc'''
  res = model.Session.execute(query).fetchall()
  maintainers_with_datasets = []
  for maintainer, number_of_datasets in res:
    maintainers_with_datasets.append({ 'maintainer': maintainer, 'number_of_datasets': number_of_datasets })
  
  return maintainers_with_datasets
    

@memo(max_age=60)
def owms_taxonomie_beleidsagenda_hierarchical():
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
  return hierarchicalarrayofobjects_to_formselectdict(owms_taxonomie_beleidsagenda_hierarchical(), 'uri', 'name', 'children')

@memo(max_age=60)
def owms_taxonomie_overheidsorganisatie():
  
  owms_taxonomie_overheidsorganisatie = owms_taxonomie_overheidsorganisatie_hierarchical()
  owms_taxonomie_overheidsorganisatie.insert(0, {'name':'', 'uri':''})
  
  return hierarchicalarrayofobjects_to_formselectdict(owms_taxonomie_overheidsorganisatie, 'uri', 'name', 'children')

@memo(max_age=60)
def owms_taxonomie_overheidsorganisatie_hierarchical():
  from pylons import config
  try:
    r = requests.get(config.get('drupal.site_url') + '/service/waardelijsten/overheidsorganisatie')
    owms_taxonomie_overheidsorganisatie = r.json()
  except NotFound:
    owms_taxonomie_overheidsorganisatie = []
  
  return owms_taxonomie_overheidsorganisatie


@memo(max_age=60)
def owms_frequentie():
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/owms_frequentie.csv')

@memo(max_age=60)
def adms_status():
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/adms_status.csv')

@memo(max_age=60)
def language():
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/language.csv')

@memo(max_age=60)
def lod_stars():
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/lod_stars.csv')

@memo(max_age=60)
def distribution_format():
  return read_file_to_formselectdict('/home/ckan/stamdata/donl/distribution_format.csv')


# Converters / default value providers

def md_wijzigingsdatum_default(value, context):
  return time.strftime("%Y-%m-%d")
  
def md_soortwijziging_default_created(value, context):
  return ":created"

def md_soortwijziging_default_updated(value, context):
  return ":updated"

def contact_point_default(value, context):
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  return value or user.email

def source_default(value, context):
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  return value or user.display_name or user.fullname or user.name or user.id

def owner_org_default(value, context):
  return value or ckan.lib.helpers.organizations_available('create_dataset')[0].get('id')
  
def creator_user_id_default(value, context):
  model = context['model']
  user = context['user']
  user = model.User.get(user)
  return value or user.id


def maintainer_facet_default(key, data, errors, context):
  # Simply copies the maintainer uri to the maintainer_facet field
  for data_key, data_value in data.iteritems():
    if (data_key[0] == 'maintainer'):
      data[(key[0],)] = data_value
      break


def theme_facet_default(key, data, errors, context):
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
    # Change the default sort
    if search_params.get('sort') in (None, 'rank'):
        search_params['sort'] = 'score desc, modified desc, metadata_modified desc'
    return search_params
    
  # IFacets implementations
  def dataset_facets(self, facets_dict, package_type):
    facets_dict['maintainer_facet'] = tk._('Data-eigenaar')
    facets_dict['theme_facet'] = tk._('Thema')
    facets_dict['subtheme_facet'] = tk._('Subthema')
    facets_dict['res_format'] = tk._('Bronformaat')
    facets_dict['organization'] = tk._('Catalogus')
    facets_dict['language'] = tk._('Taal')
    return facets_dict

  def organization_facets(self, facets_dict, organization_type, package_type):
    facets_dict['maintainer_facet'] = tk._('Data-eigenaar')
    facets_dict['theme_facet'] = tk._('Thema')
    facets_dict['subtheme_facet'] = tk._('Subthema')
    facets_dict['res_format'] = tk._('Bronformaat')
    facets_dict['organization'] = tk._('Catalogus')
    facets_dict['language'] = tk._('Taal')
    return facets_dict

  def group_facets(self, facets_dict, group_type, package_type):
    facets_dict['maintainer_facet'] = tk._('Data-eigenaar')
    facets_dict['theme_facet'] = tk._('Thema')
    facets_dict['subtheme_facet'] = tk._('Subthema')
    facets_dict['res_format'] = tk._('Bronformaat')
    facets_dict['organization'] = tk._('Catalogus')
    facets_dict['language'] = tk._('Taal')
    return facets_dict

  def get_helpers(self):
    # Template helper function names should begin with the name of the
    # extension they belong to, to avoid clashing with functions from
    # other extensions.
    return {
      'donl_owms_taxonomie_beleidsagenda': owms_taxonomie_beleidsagenda,
      'donl_owms_taxonomie_overheidsorganisatie': owms_taxonomie_overheidsorganisatie,
      'donl_owms_taxonomie_overheidsorganisatie_hierarchical': owms_taxonomie_overheidsorganisatie_hierarchical,
      'donl_owms_frequentie': owms_frequentie,
      'donl_adms_status': adms_status,
      'donl_language': language,
      'donl_lod_stars': lod_stars,
      'donl_distribution_format': distribution_format,
      'donl_sel_to_dict': sel_to_dict,
      'donl_maintainers_with_datasets' : maintainers_with_datasets,
      'donl_active_users' : active_users,
      'donl_facet_value_displayname' : facet_value_displayname
    }
    

  def _modify_package_resource_schema(self, schema):
    schema['resources'].update({
      'download_url': [tk.get_validator('ignore_missing')],
      'modified': [tk.get_validator('ignore_missing')],
      'adms_status': [tk.get_validator('ignore_missing')],
      'issued': [tk.get_validator('ignore_missing')],
      'bytesize': [tk.get_validator('ignore_missing')],
    })
    return schema


  def _modify_package_schema(self, schema):
    # Used by create_package_schema() and update_package_schema()
    
    schema.update({
      'identifier': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'title': [tk.get_validator('not_empty')],
      'owner_org': [owner_org_default],
      'creator_user_id': [creator_user_id_default],
      'maintainer': [tk.get_validator('not_empty')],
      'notes': [tk.get_validator('not_empty')],
      'modified': [tk.get_validator('not_empty'), tk.get_converter('convert_to_extras')],
      'language': [tk.get_validator('not_empty'), tk.get_converter('convert_to_extras')],
      'theme': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      #'theme_secondary': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
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
      'md_uri': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'md_uitgiftedatum': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'md_titel': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'md_omschrijving': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'grondslag': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'grondslag_citeertitel': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
    })
    
    schema = self._modify_package_resource_schema(schema)
    
    schema.update({
      'maintainer_displayname': [maintainer_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'theme_displayname': [theme_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],

      'maintainer_facet': [maintainer_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'theme_facet': [theme_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
      'subtheme_facet': [subtheme_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')]
    })

    return schema


  def show_package_schema(self):
    # Return a schema to validate datasets before they’re shown to the user.

    schema = super(IpmPlugin, self).show_package_schema()
    schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))
    schema.update({
      'identifier': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'title': [tk.get_validator('not_empty')],
      'owner_org': [owner_org_default],
      'maintainer': [tk.get_validator('not_empty')],
      'notes': [tk.get_validator('not_empty')],
      'modified': [tk.get_converter('convert_from_extras'), tk.get_validator('not_empty')],
      'language': [tk.get_converter('convert_from_extras'), tk.get_validator('not_empty')],
      'theme': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'subtheme': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      #'theme_secondary': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      #'subtheme_secondary': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
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
      'md_uri': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_soortwijziging': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_uitgiftedatum': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_titel': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'md_omschrijving': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'grondslag': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
      'grondslag_citeertitel': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
    })

    schema = self._modify_package_resource_schema(schema)

    schema.update({
      'maintainer_displayname': [maintainer_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')],
      'theme_displayname': [theme_displayname_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')],

      'maintainer_facet': [maintainer_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')],
      'theme_facet': [theme_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')],
      'subtheme_facet': [subtheme_facet_default, tk.get_validator('ignore_missing'), tk.get_converter('convert_from_extras')]
    })
    
    return schema


  def create_package_schema(self):
    # Return the schema for validating new dataset dicts.
    
    schema = super(IpmPlugin, self).create_package_schema()
    schema = self._modify_package_schema(schema)
    schema.update({
      'md_soortwijziging': [md_soortwijziging_default_created, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
    })
    return schema


  def update_package_schema(self):
    # Return the schema for validating updated dataset dicts.
    
    schema = super(IpmPlugin, self).update_package_schema()
    schema = self._modify_package_schema(schema)
    schema.update({
      'md_soortwijziging': [md_soortwijziging_default_updated, tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
    })
    return schema


  def is_fallback(self):
    # Return True to register this plugin as the default handler for
    # package types not handled by any other IDatasetForm plugin.
    return True


  def package_types(self):
    # This plugin doesn't handle any special package types, it just
    # registers itself as the default (above).
    return []
    
    
  def update_config(self, config):
    # Add this plugin's templates dir to CKAN's extra_template_paths, so
    # that CKAN will use this plugin's custom templates.
    tk.add_template_directory(config, 'templates')
    
    

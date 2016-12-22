import ckan.plugins as p
from ckan.logic.auth import get_package_object
from ckanext.userextra.model import UserExtra
import ckan.logic.auth


import logging
log = logging.getLogger(__name__)


def donl_package_update(context, data_dict):
    model = context['model']
    user = context.get('user')
    user_obj = model.User.get( user )
    package = get_package_object(context, data_dict)

    # Allow sysadmins to edit anything
    if user_obj.sysadmin:
        return {'success': True}

    # Leave the core CKAN auth to work out the hierarchy stuff
    result = ckan.logic.auth.update.package_update(context, data_dict)

    # Check extras for donl_data_eigenaar
    # When extras contains a value for donl_data_eigenaar, don't authorize when package maintainer does not match extras value
    # TODO Should we authorize the user anyway if he is the owner of this dataset?
    extras = UserExtra.get_extra(user_obj.id)
    if extras and extras.get('donl_data_eigenaar'):
      result['success'] = result['success'] and (extras.get('donl_data_eigenaar') == package.maintainer)
      log.debug('Allow donl_package_update? %s (pkg: %s - pkg.mnt: %s - user.mnt: %s', result['success'], package.name, package.maintainer, extras.get('donl_data_eigenaar'))

    return result


def donl_resource_create_upload(context, data_dict):
    result = {}
    
    if data_dict.get('is_draft'):
        # When the dataset is a draft, assume uploading is allowed by default
        result['success'] = True
    else:
        # Is creating a resource allowed by CKAN?
        result = ckan.logic.auth.create.resource_create(context, data_dict)
    
    # Check user extras in profile for donl_storage flag (with its origin in Drupal user profile)
    model = context['model']
    user = context.get('user')
    user_obj = model.User.get( user )

    existing_extras = UserExtra.get_extra(user_obj.id)
    result['success'] = result['success'] and existing_extras.get('donl_storage') and existing_extras.get('donl_storage') in ['True','true','1']

    log.debug('Allow donl_resource_create_upload? %s', result['success'])

    # Return
    return result


def donl_resource_update_upload(context, data_dict):
    # Is updating a resource allowed by CKAN?
    result = ckan.logic.auth.update.resource_update(context, data_dict)

    # Check user extras in profile for donl_storage flag (with its origin in Drupal user profile)
    model = context['model']
    user = context.get('user')
    user_obj = model.User.get( user )

    existing_extras = UserExtra.get_extra(user_obj.id)
    result['success'] = result['success'] and existing_extras.get('donl_storage') and existing_extras.get('donl_storage') in ['True','true','1']
    
    log.debug('Allow donl_resource_update_upload? %s', result['success'])

    # Return
    return result


class DonlAuthorizePlugin(p.SingletonPlugin):
    p.implements(p.IAuthFunctions, inherit=True)

    def get_auth_functions(self):
        return {
          'resource_create_upload': donl_resource_create_upload,
          'resource_update_upload': donl_resource_update_upload,
          'package_update': donl_package_update
        }
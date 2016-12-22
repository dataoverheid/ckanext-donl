import ckan.plugins as p

class DrupalAuthPlugin(p.SingletonPlugin):
    '''Reads Drupal login cookies to log user in.'''
    p.implements(p.IMiddleware, inherit=True)

    def make_middleware(self, app, config):
        from ckanext.donl.authentication.drupal_auth import DrupalAuthMiddleware
        return DrupalAuthMiddleware(app, config)
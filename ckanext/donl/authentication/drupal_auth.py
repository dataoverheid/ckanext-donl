import Cookie
import logging
import datetime
import hashlib

from ckanext.donl.drupalclient import DrupalClient, DrupalXmlRpcSetupError, \
     DrupalRequestError
from xmlrpclib import ServerProxy

log = logging.getLogger(__name__)

class DrupalAuthMiddleware(object):
    '''Allows CKAN user to login via Drupal. It looks for the Drupal cookie
    and gets user details from Drupal using XMLRPC.
    so works side-by-side with normal CKAN logins.'''

    def __init__(self, app, app_conf):
        self.app = app
        self.drupal_client = None
        self._user_name_prefix = 'user_d'

        minutes_between_checking_drupal_cookie = app_conf.get('minutes_between_checking_drupal_cookie', 30) 
        self.seconds_between_checking_drupal_cookie = int(minutes_between_checking_drupal_cookie) * 60
        # if that int() raises a ValueError then the app will not start

    def _parse_cookies(self, environ):
        is_ckan_cookie = [False]
        drupal_session_id = [False]
        server_name = environ['SERVER_NAME']
        for k, v in environ.items():
            key = k.lower()
            if key  == 'http_cookie':
                is_ckan_cookie[0] = self._is_this_a_ckan_cookie(v)
                drupal_session_id[0] = self._drupal_cookie_parse(v, server_name)
        is_ckan_cookie = is_ckan_cookie[0]
        drupal_session_id = drupal_session_id[0]
        return is_ckan_cookie, drupal_session_id

    @staticmethod
    def _drupal_cookie_parse(cookie_string, server_name):
        '''Returns the Drupal Session ID from the cookie string.'''
        cookies = Cookie.SimpleCookie()
        try:
            cookies.load(str(cookie_string))
        except Cookie.CookieError:
            log.error("Received invalid cookie: %s" % cookie_string)
            return False
        similar_cookies = []
        for cookie in cookies:
            if cookie.startswith('SESS') or cookie.startswith('SSESS'):
                # Drupal 6 uses md5, Drupal 7 uses sha256
                server_hash = hashlib.sha256(server_name).hexdigest()[:32]
                if cookie == 'SESS%s' % server_hash:
                    log.debug('Drupal cookie found for server request %s', server_name)
                    return cookies[cookie].value
                elif cookie == 'SSESS%s' % server_hash:
                    log.debug('Drupal cookie (secure) found for server request %s', server_name)
                    return cookies[cookie].value
                else:
                    similar_cookies.append(cookie)
        if similar_cookies:
            log.debug('Drupal cookies ignored with incorrect hash for server %r: %r',
                      server_name, similar_cookies)
        return None

    @staticmethod
    def _is_this_a_ckan_cookie(cookie_string):
        cookies = Cookie.SimpleCookie()
        try:
            cookies.load(str(cookie_string))
        except Cookie.CookieError:
            log.warning("Received invalid cookie: %s" % cookie_string)
            return False

        if not 'auth_tkt' in cookies:
            return False
        return True

    def _munge_drupal_id_to_ckan_user_name(self, drupal_id):
        drupal_id.lower().replace(' ', '_')
        return u'%s%s' % (self._user_name_prefix, drupal_id)

    def _log_out(self, environ, new_headers):
        # don't progress the user info for this request
        environ['REMOTE_USER'] = None
        environ['repoze.who.identity'] = None
        # tell auth_tkt to logout whilst adding the header to tell
        # the browser to delete the cookie
        identity = {}
        headers = environ['repoze.who.plugins']['donl_auth_tkt'].forget(environ, identity)
        if headers:
            new_headers.extend(headers)
        # Remove cookie from request, so that if we are doing a login again in this request then
        # it is aware of the cookie removal
        #log.debug('Removing cookies from request: %r', environ.get('HTTP_COOKIE', ''))
        cookies = environ.get('HTTP_COOKIE', '').split('; ')
        cookies = '; '.join([cookie for cookie in cookies if not cookie.startswith('auth_tkt=')])
        environ['HTTP_COOKIE'] = cookies
        #log.debug('Cookies in request now: %r', environ['HTTP_COOKIE'])

        log.debug('Logged out Drupal user')

    def __call__(self, environ, start_response):
        '''
        Middleware that sets the CKAN logged-in/logged-out status according
        to Drupal's logged-in/logged-out status.

        Every request comes through here before hitting CKAN because it is
        configured as middleware.
        '''
        new_headers = []

        self.do_drupal_login_logout(environ, new_headers)

        #log.debug('New headers: %r', new_headers)
        def cookie_setting_start_response(status, headers, exc_info=None):
            if headers:
                headers.extend(new_headers)
            else:
                headers = new_headers
            return start_response(status, headers, exc_info)
        new_start_response = cookie_setting_start_response

        return self.app(environ, new_start_response)

    def do_drupal_login_logout(self, environ, new_headers):
        '''Looks at cookies and auth_tkt and may tell auth_tkt to log-in or log-out
        to a Drupal user.'''
        is_ckan_cookie, drupal_session_id = self._parse_cookies(environ)

        # Is there a Drupal cookie? We may want to do a log-in for it.
        if drupal_session_id:
            # Look at any authtkt logged in user details
            authtkt_identity = environ.get('repoze.who.identity')
            if authtkt_identity:
                authtkt_user_name = authtkt_identity['repoze.who.userid'] #same as environ.get('REMOTE_USER', '')
                authtkt_drupal_session_id = authtkt_identity['userdata']
            else:
                authtkt_user_name = ''
                authtkt_drupal_session_id = ''

            if not authtkt_user_name:
                # authtkt not logged in, so log-in with the Drupal cookie
                self._do_drupal_login(environ, drupal_session_id, new_headers)
                return
            elif authtkt_user_name.startswith(self._user_name_prefix):
                # A drupal user is logged in with authtkt.
                # See if that the authtkt matches the drupal cookie's session
                if authtkt_drupal_session_id != drupal_session_id:
                    # Drupal cookie session has changed, so tell authkit to forget the old one
                    # before we do the new login
                    log.debug('Drupal cookie session has changed.')
                    #log.debug('Drupal cookie session has changed from %r to %r.', authtkt_drupal_session_id, drupal_session_id)
                    self._log_out(environ, new_headers)
                    self._do_drupal_login(environ, drupal_session_id, new_headers)
                    #log.debug('Headers on log-out log-in result: %r', new_headers)
                    return
                else:
	            log.debug('Drupal cookie session stayed the same.')
                    # Drupal cookie session matches the authtkt - leave user logged ini

                    # Just check that authtkt cookie is not too old - in the
                    # mean-time, Drupal may have invalidated the user, for example.
                    if self.is_authtkt_cookie_too_old(authtkt_identity):
                        log.info('Rechecking Drupal cookie')
                        self._log_out(environ, new_headers)
                        self._do_drupal_login(environ, drupal_session_id, new_headers)
                    return
            else:
                # There's a Drupal cookie, but user is logged in as a normal CKAN user.
                # Ignore the Drupal cookie.
                return
        elif not drupal_session_id and is_ckan_cookie:
            # Deal with the case where user is logged out of Drupal
            # i.e. user WAS were logged in with Drupal and the cookie was
            # deleted (probably because Drupal logged out)

            # Is the logged in user a Drupal user?
            user_name = environ.get('REMOTE_USER', '')
            if user_name and user_name.startswith(self._user_name_prefix):
                log.debug('Was logged in as Drupal user %r but Drupal cookie no longer there.', user_name)
                self._log_out(environ, new_headers)


    def _do_drupal_login(self, environ, drupal_session_id, new_headers):
        '''Given a Drupal cookie\'s session ID, check it with Drupal, create/modify
        the equivalent CKAN user with properties copied from Drupal and log the
        person in with auth_tkt and its cookie.
        '''
        if self.drupal_client is None:
            self.drupal_client = DrupalClient()
        # ask drupal for the drupal_user_id for this session
        try:
            drupal_user_id = self.drupal_client.get_user_id_from_session_id(drupal_session_id)
        except DrupalRequestError, e:
            log.error('Error checking session with Drupal: %s', e)
            return
        if not drupal_user_id:
            log.debug('Drupal said the session ID found in the cookie is not valid.')
            return

        # ask drupal about this user
        drupal_user_properties = self.drupal_client.get_user_properties(drupal_user_id)
        user_dict = DrupalUserMapping.drupal_user_to_ckan_user(
                drupal_user_properties)

        # see if user already exists in CKAN
        ckan_user_name = user_dict['name']
        from ckan import model
        from ckan.model.meta import Session
        query = Session.query(model.User).filter_by(name=unicode(ckan_user_name))
        if not query.count():
            # need to add this user to CKAN
            user = model.User(**user_dict)
            Session.add(user)
            Session.commit()
            log.debug('Drupal user added to CKAN as: %s', user.name)
        else:
            user = query.one()
            log.debug('Drupal user found in CKAN: %s', user.name)

            if user.email != user_dict['email'] or \
                    user.fullname != user_dict['name']:
                user.email = user_dict['email']
                user.fullname = user_dict['fullname']
                
                log.debug('User details updated from Drupal: %s %s',
                          user.email, user.fullname)
                model.Session.commit()

        # extra fields (depends on ckanext-userextra)
        query = Session.query(model.User).filter_by(name=unicode(ckan_user_name))
        if query.count():
            user = query.one()
            self.upsert_extras(user, user_dict)
            
        # set CKAN roles based on Drupal roles
        self.set_roles(ckan_user_name, drupal_user_properties['roles'].values())

        # There is a chance that on this request we needed to get authtkt
        # to log-out. This would have created headers like this:
        #   'Set-Cookie', 'auth_tkt="INVALID"...'
        # but since we are about to login again, which will create a header
        # setting that same cookie, we need to get rid of the invalidation
        # header first.
        new_headers[:] = [(key, value) for (key, value) in new_headers \
                            if (not (key=='Set-Cookie' and value.startswith('auth_tkt="INVALID"')))]
        #log.debug('Headers reduced to: %r', new_headers)

        # Ask auth_tkt to remember this user so that subsequent requests
        # will be authenticated by auth_tkt.
        # auth_tkt cookie template needs to also go in the response.
        identity = {'repoze.who.userid': str(ckan_user_name),
                    'tokens': '',
                    'userdata': drupal_session_id}
        headers = environ['repoze.who.plugins']['donl_auth_tkt'].remember(environ, identity)
        if headers:
            new_headers.extend(headers)

        # Tell app during this request that the user is logged in
        environ['REMOTE_USER'] = user.name
        log.debug('Set REMOTE_USER = %r', user.name)




    def upsert_extras(self, user, user_dict):
        ''' Upserts the user's extras (for DONL) into the database when they have changed.
        
        Depends on ckanext-userextra plugin.
        '''
        from ckanext.userextra.model import UserExtra
        
        existing_extras = UserExtra.get_extra(user.id)
        given_extras = dict((k,v) for k, v in user_dict.items() if k.startswith('donl_'))
        
        if (existing_extras != given_extras):
            UserExtra.purge(user.id)
            UserExtra.from_dict(user.id, given_extras)
            log.debug('Persisted given extras to database for user id %s: %s', user.id, given_extras)

        self.process_extras(user, given_extras)




    def process_extras(self, user, extras):
        ''' Checks the extras for the donl_catalogus field to be set.
        When set, add/update this user as an admin in this organization.
        When not set AND a default organization is set in the Pylon's config (production.ini), add/update this user as an admin in this default organization.
        
        Depends on ckanext-userextra plugin.
        '''
        from pylons import config
        from ckan import model
        import ckan.plugins.toolkit as toolkit
        
        org_name = config.get('donl.default_organization')
        if (extras and extras.get('donl_catalogus')):
          org_name = extras.get('donl_catalogus').rsplit('/', 1)[-1]
        
        if (org_name):
          member_create(context={'model': model, 'session': model.Session, 'user': user},data_dict={'user': user,'id':org_name, 'object':user.id, 'capacity':'admin','object_type':'user'})






    def set_roles(self, user_name, drupal_roles):
        '''Sets CKAN user roles based on the drupal roles.

        Restricted to sysadmin. Publishing roles initially imported during migration from
        Drupal.

        Example drupal_roles:
        ['package admin', 'publisher admin', 'authenticated user', 'publishing user']
        where sysadmin roles are:
               3   'administrator' - total control
               11  'package admin' - admin of datasets
                   'publisher admin' - admin of publishers
        other roles:
                   'publishing user' - anyone who has registered - includes spammers
        '''
        from ckan import model
        from ckan import authz
        needs_commit = False
        user = model.User.by_name(user_name)

        # Sysadmin or not
        log.debug('User roles in Drupal: %r', drupal_roles)
        should_be_sysadmin = bool(set(('administrator', 'package admin', 'publisher admin', 'ckan administrator')) & set(drupal_roles))
        if should_be_sysadmin and not user.sysadmin:
            # Make user a sysadmin
            user.syadmin = True
            log.info('User made a sysadmin: %s', user_name)
            needs_commit = True
        elif not should_be_sysadmin and user.sysadmin:
            # Stop user being a sysadmin - disabled for time being which 'ckan
            # administrator' is populated
            #user.sysadmin = False
            #log.info('User now not a sysadmin: %s', user_name)
            #needs_commit = True
            pass
        if needs_commit:
            model.repo.commit_and_remove()

    def is_authtkt_cookie_too_old(self, authtkt_identity):
        authtkt_time = datetime.datetime.fromtimestamp(authtkt_identity['timestamp'])
        age = datetime.datetime.now() - authtkt_time
        age_in_seconds = age.seconds + age.days * 24 * 3600
        log.debug('Seconds since checking Drupal cookie: %s (threshold=%s)', age_in_seconds, self.seconds_between_checking_drupal_cookie)
        return age_in_seconds > self.seconds_between_checking_drupal_cookie

class DrupalUserMapping:
    _user_name_prefix = 'user_d'

    @classmethod
    def drupal_id_to_ckan_user_name(cls, drupal_id):
        # Drupal ID is always a number
        drupal_id.lower().replace(' ', '_') # just in case
        return u'%s%s' % (cls._user_name_prefix, drupal_id)

    @classmethod
    def ckan_user_name_to_drupal_id(cls, ckan_user_name):
        if ckan_user_name.startswith(cls._user_name_prefix):
            return ckan_user_name[len(cls._user_name_prefix):]
        else:
            return None # Not a Drupal user

    @classmethod
    def drupal_user_to_ckan_user(cls, drupal_user_dict, existing_user_name=None):
        return dict(
            name = existing_user_name or cls.drupal_id_to_ckan_user_name(drupal_user_dict['uid']),
            fullname = unicode(drupal_user_dict['name']),
            donl_data_eigenaar = unicode(drupal_user_dict['donl_data_eigenaar']),
            donl_verstrekker = unicode(drupal_user_dict['donl_verstrekker']),
            donl_catalogus = unicode(drupal_user_dict['donl_organisatienaam']),
            donl_storage = unicode(drupal_user_dict['donl_ckan_storage']),
            about = u'User account imported from Drupal system.',
            email = drupal_user_dict['mail'],
            created = datetime.datetime.fromtimestamp(int(drupal_user_dict['created']))
            )




def member_create(context, data_dict=None):
    '''Make an object (e.g. a user, dataset or group) a member of a group.

    If the object is already a member of the group then the capacity of the
    membership will be updated.

    You must be authorized to edit the group.

    :param user: the user object
    :type user: user object
    :param id: the id or name of the group to add the object to
    :type id: string
    :param object: the id or name of the object to add
    :type object: string
    :param object_type: the type of the object being added, e.g. ``'package'``
        or ``'user'``
    :type object_type: string
    :param capacity: the capacity of the membership
    :type capacity: string

    :returns: the newly created (or updated) membership
    :rtype: dictionary

    '''
    from ckan import model
    import ckan.plugins.toolkit as toolkit
    import ckan.logic as logic

    user, group_id, obj_id, obj_type, capacity = \
        toolkit.get_or_bust(data_dict, ['user', 'id', 'object', 'object_type', 'capacity'])

    rev = model.repo.new_revision()
    #rev.author = user
    #rev.message = 'Drupal DONL Catalogus'

    group = model.Group.get(group_id)
    if not group:
        raise NotFound('Group was not found.')

    obj_class = logic.model_name_to_class(model, obj_type)
    obj = obj_class.get(obj_id)
    if not obj:
        raise NotFound('%s was not found.' % obj_type.title())

    # Look up existing, in case it exists
    member = model.Session.query(model.Member).\
        filter(model.Member.table_name == obj_type).\
        filter(model.Member.table_id == obj.id).\
        filter(model.Member.group_id == group.id).\
        filter(model.Member.state == 'active').first()
    if not member:
        member = model.Member(table_name=obj_type,
                              table_id=obj.id,
                              group_id=group.id,
                              state='active')

        member.capacity = capacity
    
        model.Session.add(member)
        model.repo.commit()
        log.debug('Username %s added as admin in organization %s', user.name, group.name)


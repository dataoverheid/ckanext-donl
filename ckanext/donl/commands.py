from ckan import model
from ckan.lib.cli import CkanCommand
from ckan.logic import get_action, NotFound

import sys


class DonlCommand(CkanCommand):
    '''
    CKAN DONL Extension

    Usage::

        paster donl updatedb-assembla358 [max_items] -c <path to config file>
           - Initializes the new fields introduced by Assembla #358 for all current datasets.
           When max_items is given, the command exits after max_items modified items.

    The commands should be run from the ckanext-donl directory.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print DonlCommand.__doc__
            return

        cmd = self.args[0]
        self._load_config()
        
        if cmd == 'updatedb-assembla358':
            if len(self.args) == 2:
                self.updatedb_assembla358(self.args[1])
            else:
                self.updatedb_assembla358()
        else:
            print 'Command "%s" not recognized' % (cmd,)

    def updatedb_assembla358(self, max_items = None):
        '''
        Initializes the new fields introduced by Assembla #358 for all current datasets
        '''
        packages = []

        # Get all packages
        pkgs = model.Session.query(model.Package).filter_by(state='active').order_by('name').all()
        packages.extend(pkgs)
        
        if packages:
          print 'Datasets to check for empty new fields: %d' % len(packages)
        if not (packages):
          print 'No datasets to process!'
          sys.exit(1)
        
        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)

        counter = 0
        
        if max_items:
          print 'Note: processing will stop after %d modified items' % int(max_items)
        
        for package in packages:
          sys.stdout.write('Processing dataset: %s ... ' % package.name)

          pkg = model.Session.query(model.Package).get(package.id)
          model.repo.new_revision()

          package_modified = False
          
          if not pkg.extras.get('dataset_status'):
            pkg.extras[u'dataset_status'] = u'http://data.overheid.nl/status/beschikbaar'
            package_modified = True
          
          if not pkg.extras.get('accessibility'):
            pkg.extras[u'accessibility'] = u'http://data.overheid.nl/acessrights/publiek'
            package_modified = True

          if not pkg.extras.get('high_value_dataset'):
            pkg.extras[u'high_value_dataset'] = False
            package_modified = True
          
          if package_modified:
            sys.stdout.write('Committing changes... ')
            counter += 1
            model.Session.commit()
            print 'Changes committed!'
          else:
            print 'Unchanged.'

          if max_items and counter == int(max_items):
            print 'Exiting after %d items!' % counter
            print 'DONE'
            sys.exit(1)
            
        print 'DONE!'

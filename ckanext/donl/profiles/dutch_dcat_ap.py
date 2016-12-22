from rdflib.namespace import Namespace
from ckanext.dcat.profiles import RDFProfile

import ckanext.donl.model.ipm_plugin as ipm

import logging
log = logging.getLogger(__name__)

DCT = Namespace("http://purl.org/dc/terms/")


class DutchDCATAPProfile(RDFProfile):
    '''
    An RDF profile for the Dutch DCAT-AP recommendation for data portals

    It requires the European DCAT-AP profile (`euro_dcat_ap`)
    '''

    def parse_dataset(self, dataset_dict, dataset_ref):
        #log.debug('parse_dataset - dataset_dict: %s', dataset_dict)
        #log.debug('parse_dataset - dataset_ref: %s', dataset_ref)

        # publisher -> maintainer
        publisher = self._publisher(dataset_ref, DCT.publisher)
        if publisher:
            #dataset_dict['extras'].append({'key': 'maintainer', 'value': str(publisher.get('uri'))})
            #dataset_dict['extras'].append({'key': 'maintainer_email', 'value': str(publisher.get('email'))})
            dataset_dict['maintainer'] = str(publisher.get('uri'))
            dataset_dict['maintainer_email'] = str(publisher.get('email'))
        
        #print self._get_dataset_value(dataset_dict, 'uri')
        
        # Ugly possible fix for URL already in use problem
        dataset_dict['title'] = dataset_dict['title'] + ' ' + self._get_dataset_value(dataset_dict, 'identifier')

        # Required fields which probably don't exist in original
        if not self._get_dataset_value(dataset_dict, 'dataset_status'):
            #dataset_dict['extras'].append({'key': 'dataset_status', 'value': str(ipm.dataset_status_default(None, None))})
            dataset_dict['dataset_status'] = str(ipm.dataset_status_default(None, None))
        
        return dataset_dict

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        #log.debug('graph_from_dataset - dataset_dict: %s', dataset_dict)
        #log.debug('graph_from_dataset - dataset_ref: %s', dataset_ref)
        g = self.g


ckanext-donl
=================

Dit is Indicia's CKAN-extensie voor data.overheid.nl

Installatie
-----------

Activate CKAN environment

	. /home/ckan/ckan/lib/default/bin/activate


Installatie PyMemoize

	cd ckanext-donl/modules/PyMemoize-master
	sudo python setup.py install


CKAN extensie

	cd ckanext-donl/
	sudo python setup.py develop


Apache herstarten
	
	sudo service httpd restart



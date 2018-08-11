Odoo_imppn : Module build to export invoices (active and passive) to an accounting system format (python library)

=============================================================================

Before installing the module :

start odoo and create database then go to settings > users > Administrator 

Edit form , select technical features and hit save.

refrech the page 

now go to settings > technical > database structure > models

search for res_company , select the mddel then hit edit 

add item (x_teamsystem_id) type field integer and click save & close , hit save.

now we get to settings > local modules , and search for Accounting and Finance and install it.

=============================================================================

this module is using a costumize python library that odoo doesn't recognize 

to install it we need to copie this file https://github.com/matteopolleschi/pyIMPPN

into odoo8 container odoo8:/usr/lib/python2.7/dist-packages/

then run the commande :

cd pyIMPPN 

python setup.py install
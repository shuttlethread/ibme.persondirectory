Introduction
============

A simple dexterity-based directory with faceted search. Developed initially
as a directory of academic staff. This is designed to be used along with a
Diazo theme to present the results.

Installation
============

Install as any other Plone add-on, i.e. add to your ``buildout.cfg`` and then
enable your add-on in your site. See 
`official install documentation for more advice <http://plone.org/documentation/kb/add-ons/installing>`__.

Configuration
=============

Before you start creating a directory, consider what fields you want your
directory entries to have. For example, "department", "favourite animal", etc.
Initially, directory entries have 2 fields, ``title`` and ``image``. These can be
edited or new fields added. To do this:

* Go to the Plone control panel
* Select "Dexterity content types"
* Select "Directory Entry"
* Click the "Fields" tab.

Add as many fields as you require, and/or alter the title/description of the
existing fields.

Once set up, you can add a Person directory anywhere to your site using "Add new".

Facets
------

If you would like the "department" field you configured earlier to be sortable
with facets (i.e you can filter the entries with links down the right hand
side), then you need to select in in the directories' "Fields to filter by"
list.

Suggestion Fields
-----------------

If a field is selected as a facet, then you can also use the
``SuggestionFieldWidget`` on a TextLine field to show previously used values.
To do this you need to alter the entry schema XML (click "Edit XML Field Model")
and change it to::

    <field name="research_group" type="zope.schema.TextLine">
      <title>Research Group</title>
      <form:widget type="ibme.persondirectory.widget.SuggestionFieldWidget"/>
    </field>

Entry images
------------

By default, there is an ``image`` field that can be used to, e.g. add portraits.
The image will be scaled by ``plone.app.imaging``. You can alter the dimensions
in the "Image Handling" section of the Plone control panel. Edit the "pdir-image"
size.

Sorting
-------

By default, entries are sorted alphabetically. However you can change this by
editing the directory object.

Credits
=======

Authors:

* Jamie Lentin [lentinj], http://shuttlethread.com

Developed as part of the `Oxford IBME website <http://www.ibme.ox.ac.uk/>`__.

Further work
============

The resulting display is rather uninspiring admittedly, this is most useful
in combination with your own Diazo theme. However, the initial view could be
tarted up a bit.

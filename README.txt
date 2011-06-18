= raisin.box =

This package contains the definition of the boxes that appear on the pages rendered by
repoze.bfg.

    boxes.ini

It also contains information from where to fetch the resources contained in the boxes:

    resources.ini

While most boxes should render without any changes, some boxes require special handling.
All boxes have a method for augmenting their configuration dynamically in

    boxes.py

An example of augmenting just the basics, like the title, description and description type:

    @augment_resource((PICKLED,))
    def project_about(self, box):
        box['title'] = 'About'
        box['description'] = box[PICKLED]['description']       
        box['description_type'] = 'infotext'
        return box       

An example of correcting the height of a chart depending on the length of the table data:

    @augment_resource((JSON, PICKLED))
    def read_quality(self, box):
        # Need to extract some infos from the table, so load the pickled dictionary
        table = box[PICKLED]
        height = max(len(table['table_data']) * 60, 160)
        box['chartoptions']['height'] = str(height)

= The augment_resource decorator =

The augment_resource decorator defines what resource representations should be fetched.

* JSON

    * Neede for charts that rely on Google visualization tools

* PICKLED

    * Needed if your method needs access to the Python dictionary representation of a resource

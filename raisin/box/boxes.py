"""Definition of methods augmenting resources."""

import csv
# JSON is needed for Google visualization charts
# It is not needed for resources that are just Python dictionaries
from config import JSON
# PICKLED is only needed when the box needs to work on the Python representation
# in order to augment the box information.
# It is not needed when the JSON resource can be passed through as is
from config import PICKLED
from raisin.box import RESOURCES_REGISTRY
from gvizapi import gviz_api


class augment(object):
    """This is a decorator that registers methods augmenting resources.

    Use the decorator like this:

        @augment((JSON,PICKLED))
        def project_meta(context, box):

    The list of formats needed in the method are given as the formats parameter.

    * JSON is always needed when a resource is fetched from a remote server

    * PICKLED is needed when you need to do some calculations.

    This is how to use the information from the pickled information:

    box['description'] = [{'Species': box[PICKLED]['species']}]
    """

    def __init__(self, formats):
        """Store the formats that need to be fetched for the method"""
        self.formats = formats

    def __call__(self, wrapped=None):
        """Register the method in the RESOURCES_REGISTRY"""
        if wrapped:
            RESOURCES_REGISTRY.append((wrapped.__name__,
                                       wrapped,
                                       self.formats, ))


def get_lines(box):
    """Get the lines out of a data table."""
    if not box[PICKLED]:
        return {}
    if not 'table_description' in box[PICKLED]:
        raise AttributeError(str(box))
    if not 'table_data' in box[PICKLED]:
        raise AttributeError(str(box))
    table = gviz_api.DataTable(box[PICKLED]['table_description'],
                               box[PICKLED]['table_data'])
    reader = csv.DictReader(table.ToCsv().split('\n'),
                            delimiter=',',
                            quotechar='"',
                            skipinitialspace=True)
    try:
        lines = reader.next()
    except StopIteration:
        lines = {}
    return lines

# pylint: disable-msg=W0613
# Sometimes not all parameters are used, which is not a problem

@augment((PICKLED,))
def projects(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = ''
    box['description'] = lines
    box['description_type'] = 'projectlist'
    return box


@augment((PICKLED,))
def project_about(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = 'About'
    box['description'] = lines.get('Project Description', '')
    box['description_type'] = 'infotext'
    return box


@augment((PICKLED,))
def run_about(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = 'About'
    box['description'] = lines.get('Project Description', '')
    box['description_type'] = 'infotext'
    return box


@augment((PICKLED,))
def project_meta(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = ''
    box['description'] = [{'Species': lines.get('Species', '')}]
    box['description_type'] = 'properties'
    return box


@augment((PICKLED,))
def experiment_about(context, box):
    """Augment resource."""
    box['title'] = 'About'
    lines = get_lines(box)
    box['description'] = lines.get('Description', '')
    box['description_type'] = 'infotext'
    return box


@augment((PICKLED,))
def experiments(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = ''
    box['description'] = lines
    box['description_type'] = 'linklist'
    return box


@augment((JSON, PICKLED))
def project_experimentstable(context, box):
    """Augment resource."""
    if not box[PICKLED]:
        return
    column_number = len(box[PICKLED]['table_description'])
    js = """
   function makeExperimentLink(dataTable, rowNum){
       if (dataTable.getValue(rowNum, 0) != undefined) {
           return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/' + dataTable.getValue(rowNum, 1) + '/' + dataTable.getValue(rowNum, 2) + '/tab/experiments' + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 2) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
       }
       else {
           return '';
       };
   }
   view.setColumns([{calc:makeExperimentLink, type:'string', label:'Experiment'},%s]);
""" % str(range(3, column_number))[1:-1]
    # e.g.
    # >>> str(range(2, 4))[1:-1]
    # '2, 3'
    box['javascript'] = js
    return box


@augment((JSON, PICKLED,))
def project_experiment_subset_start(context, box):
    """Augment resource."""
    return box

@augment((JSON, PICKLED,))
def project_experiment_subset_selection(context, box):
    """Augment resource."""
    js = """
   function makeExperimentSubsetLink(dataTable, rowNum){
       if (dataTable.getValue(rowNum, 0) != undefined) {
           return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/experiment/subset/' + dataTable.getValue(rowNum, 1) + '/' + dataTable.getValue(rowNum, 2) + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 4) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
       }
       else {
           return '';
       };
   }
   view.setColumns([3, {calc:makeExperimentSubsetLink, type:'string', label:'Parameter Value'}, 5]);
"""
    box['javascript'] = js
    return box


@augment((JSON, PICKLED))
def project_experiment_subset(context, box):
    """Augment resource."""
    column_number = len(box[PICKLED]['table_description'])
    js = """
   function makeExperimentLink(dataTable, rowNum){
       if (dataTable.getValue(rowNum, 0) != undefined) {
           return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/' + dataTable.getValue(rowNum, 1) + '/' + dataTable.getValue(rowNum, 2) + '/tab/experiments' + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 2) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
       }
       else {
           return '';
       };
   }
   view.setColumns([{calc:makeExperimentLink, type:'string', label:'Experiment'},%s]);
""" % str(range(3, column_number))[1:-1]
    # e.g.
    # >>> str(range(2, 4))[1:-1]
    # '2, 3'
    box['javascript'] = js
    return box


@augment((JSON, PICKLED,))
def project_experiment_subset_pending(context, box):
    """Augment resource."""
    return box


@augment((JSON,))
def project_downloads(context, box):
    """Augment resource."""
    js = """
   function makeDownloadLink(dataTable, rowNum){
       if (dataTable.getValue(rowNum, 0) != undefined) {
           return String.fromCharCode('60') + 'a href=\"' + dataTable.getValue(rowNum, 3) + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 0) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
       }
       else {
           return '';
       };
   }
   view.setColumns([1,2,{calc:makeDownloadLink, type:'string', label:'.csv File Download Link'}]);
    """
    box['javascript'] = js
    return box


@augment((JSON,))
def rnadashboard(context, box):
    """Augment resource."""
    box['title'] = ''
    return box


@augment((JSON,))
def rnadashboard_results(context, box):
    """Augment resource."""
    return box


@augment((PICKLED,))
def experiment_sample_info(context, box):
    """Augment resource."""
    return _sample_info(context, box)


@augment((PICKLED,))
def run_sample_info(context, box):
    """Augment resource."""
    return _sample_info(context, box)


def _sample_info(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = 'Sample Information'
    box['description'] = []
    if lines:
        if lines['Species']:
            box['description'].append({'Species': lines['Species']})
        if lines['Cell Type']:
            box['description'].append({'Cell Type': lines['Cell Type']})
        if lines['RNA Type']:
            box['description'].append({'RNA Type': lines['RNA Type']})
        if lines['Compartment']:
            box['description'].append({'Compartment': lines['Compartment']})
        if lines['Bio Replicate']:
            box['description'].append({'Bio Replicate': lines['Bio Replicate']})
        if lines['Date']:
            box['description'].append({'Date': lines['Date']})
    box['description_type'] = 'properties'
    return box


@augment((PICKLED,))
def experiment_mapping_info(context, box):
    """Augment resource."""
    return _mapping_info(context, box)


@augment((PICKLED,))
def run_mapping_info(context, box):
    """Augment resource."""
    return _mapping_info(context, box)


@augment((PICKLED,))
def lane_mapping_info(context, box):
    """Augment resource."""
    return _mapping_info(context, box)


def _mapping_info(context, box):
    """Augment resource."""
    lines = get_lines(box)
    box['title'] = 'Mapping Information'
    box['description'] = []
    if lines:
        add = box['description'].append
        if lines.get('Read Length', ''):
            add({'Read Length': lines['Read Length']})
        if lines.get('Mismatches', ''):
            add({'Mismatches': lines['Mismatches']})
        if lines.get('Annotation Version', ''):
            add({'Annotation Version': lines['Annotation Version']})
        if lines.get('Annotation Source', ''):
            add({'Annotation Source': lines['Annotation Source']})
        if lines.get('Genome Assembly', ''):
            add({'Genome Assembly': lines['Genome Assembly']})
        if lines.get('Genome Source', ''):
            add({'Genome Source': lines['Genome Source']})
        if lines.get('Genome Gender', ''):
            add({'Genome Gender': lines['Genome Gender']})
        if lines.get('UCSC Custom Track', '') != "":
            link = """<a target="_blank" href="%(href)s">%(content)s</a>"""
            parts = {'href': lines['UCSC Custom Track'],
                     'content': "Display as a custom track at UCSC"}
            add({'Visualization': link % parts})
    box['description_type'] = 'properties'
    return box


@augment((JSON,))
def experiment_read_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_read_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_read_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def experiment_mapping_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_mapping_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_mapping_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def experiment_expression_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_expression_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_expression_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def experiment_splicing_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_splicing_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_splicing_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON, PICKLED))
def experiment_reads_containing_ambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def run_reads_containing_ambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def experiment_reads_containing_only_unambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def run_reads_containing_only_unambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def experiment_average_percentage_of_unique_reads(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def run_average_percentage_of_unique_reads(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON,))
def experiment_total_ambiguous_and_unambiguous_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_total_ambiguous_and_unambiguous_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_total_ambiguous_and_unambiguous_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def experiment_average_and_average_unique_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_average_and_average_unique_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_average_and_average_unique_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON, PICKLED))
def experiment_percentage_of_reads_with_ambiguous_bases(context, box):
    """Augment resource."""
    return _percentage_of_reads_with_ambiguous_bases(context, box)


@augment((JSON, PICKLED))
def run_percentage_of_reads_with_ambiguous_bases(context, box):
    """Augment resource."""
    return _percentage_of_reads_with_ambiguous_bases(context, box)


@augment((JSON, PICKLED))
def lane_percentage_of_reads_with_ambiguous_bases(context, box):
    """Augment resource."""
    return _percentage_of_reads_with_ambiguous_bases(context, box)


@augment((JSON, PICKLED))
def experiment_quality_score_by_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def run_quality_score_by_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def lane_quality_score_by_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def experiment_ambiguous_bases_per_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def run_ambiguous_bases_per_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def lane_ambiguous_bases_per_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def experiment_merged_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def run_merged_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def lane_merged_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def experiment_genome_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def run_genome_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def lane_genome_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def experiment_junction_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def run_junction_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def lane_junction_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def experiment_split_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def run_split_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def lane_split_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def experiment_detected_genes(context, box):
    """Augment resource."""
    return _detected_genes(context, box)


@augment((JSON, PICKLED))
def run_detected_genes(context, box):
    """Augment resource."""
    return _detected_genes(context, box)


@augment((JSON, PICKLED))
def lane_detected_genes(context, box):
    """Augment resource."""
    return _detected_genes(context, box)


@augment((JSON,))
def experiment_gene_expression_profile(context, box):
    """Augment resource."""
    return _gene_expression_profile(context, box)


@augment((JSON,))
def run_gene_expression_profile(context, box):
    """Augment resource."""
    return _gene_expression_profile(context, box)


@augment((JSON,))
def lane_gene_expression_profile(context, box):
    """Augment resource."""
    return _gene_expression_profile(context, box)


@augment((JSON,))
def experiment_gene_expression_levels(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_gene_expression_levels(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_gene_expression_levels(context, box):
    """Augment resource."""
    pass


@augment((JSON, PICKLED))
def experiment_top_genes(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def run_top_genes(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def lane_top_genes(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def experiment_top_transcripts(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def run_top_transcripts(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def lane_top_transcripts(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def experiment_top_exons(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def run_top_exons(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON, PICKLED))
def lane_top_exons(context, box):
    """Augment resource."""
    return _thousands_formatter(context, box)


@augment((JSON,))
def experiment_exon_inclusion_profile(context, box):
    """Augment resource."""
    return _exon_inclusion_profile(context, box)


@augment((JSON,))
def run_exon_inclusion_profile(context, box):
    """Augment resource."""
    return _exon_inclusion_profile(context, box)


@augment((JSON,))
def lane_exon_inclusion_profile(context, box):
    """Augment resource."""
    return _exon_inclusion_profile(context, box)


@augment((JSON,))
def experiment_reads_supporting_exon_inclusions(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_reads_supporting_exon_inclusions(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_reads_supporting_exon_inclusions(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def experiment_novel_junctions_from_annotated_exons(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_novel_junctions_from_annotated_exons(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_novel_junctions_from_annotated_exons(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def experiment_novel_junctions_from_unannotated_exons(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def run_novel_junctions_from_unannotated_exons(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def lane_novel_junctions_from_unannotated_exons(context, box):
    """Augment resource."""
    pass


def _exon_inclusion_profile(context, box):
    """Augment resource."""
    box['chartoptions']['vAxis'] = "{logScale:true}"
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    area = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = area
    return box


def _gene_expression_profile(context, box):
    """Augment resource."""
    box['chartoptions']['vAxis'] = "{logScale:true}"
    box['chartoptions']['hAxis'] = "{logScale:true}"
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    area = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = area
    return box


def _custom_spaced_chart(context, box):
    """Augment resource."""
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    area = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = area
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''


def _thousands_formatter(context, box):
    """Augment resource."""
    javascript = "thousandsformatter.format(data, %s);\n"
    table = box[PICKLED]
    i = 0
    for column, column_type in table['table_description']:
        if column_type == 'number':
            box['javascript'] += javascript % i
        i = i + 1
    return box


def _detected_genes(context, box):
    """Augment resource."""
    box['javascript'] = ""
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(1, len(table['table_description'])):
        box['javascript'] += """thousandsformatter.format(data, %s);\n""" % i
    return box


def _mapped_reads(context, box):
    """Augment resource."""
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    area = '{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'
    box['chartoptions']['chartArea'] = area


def _percentage_of_reads_with_ambiguous_bases(context, box):
    """Augment resource."""
    table = box[PICKLED]
    height = max(len(table['table_data']) * 60, 160)
    box['chartoptions']['height'] = str(height)


def _position(context, box):
    """Augment resource."""
    box['chartoptions']['vAxis'] = "{logScale:true}"
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640

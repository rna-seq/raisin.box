"""Definition of methods augmenting resources."""

import csv
# JSON is needed for Google visualization charts
# It is not needed for resources that are just Python dictionaries
from config import JSON
# PICKLED is only needed when the box needs to work on the Python representation
# in order to augment the box information.
# It is not needed when the JSON resource can be passed through as is
from config import PICKLED
from raisin.box import resources_registry
from gvizapi import gviz_api


class augment_resource(object):
    """This is a decorator that registers methods augmenting resources.

    Use the decorator like this:

        @augment_resource((JSON,PICKLED))
        def project_meta(self, box):

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
        """Register the method in the resources_registry"""
        if wrapped:
            resources_registry.append((wrapped.__name__,
                                       wrapped,
                                       self.formats, ))


def get_lines(box):
    if not 'table_description' in box[PICKLED]:
        raise AttributeError(str(box))
    if not 'table_data' in box[PICKLED]:
        raise AttributeError(str(box))
    table = gviz_api.DataTable(box[PICKLED]['table_description'],
                               box[PICKLED]['table_data'])
    return csv.DictReader(table.ToCsv().split('\n'),
                          delimiter=',',
                          quotechar='"',
                          skipinitialspace=True)


@augment_resource((PICKLED,))
def projects(self, box):
    lines = get_lines(box)
    box['title'] = ''
    box['description'] = lines
    box['description_type'] = 'projectlist'
    return box


@augment_resource((PICKLED,))
def project_about(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'About'
    box['description'] = line.get('Project Description', '')
    box['description_type'] = 'infotext'
    return box


@augment_resource((PICKLED,))
def run_about(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'About'
    box['description'] = line.get('Project Description', '')
    box['description_type'] = 'infotext'
    return box


@augment_resource((PICKLED,))
def project_meta(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = ''
    box['description'] = [{'Species': line.get('Species', '')}]
    box['description_type'] = 'properties'
    return box


@augment_resource((PICKLED,))
def experiment_about(self, box):
    box['title'] = 'About'
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['description'] = line.get('Description', '')
    box['description_type'] = 'infotext'
    return box


@augment_resource((PICKLED,))
def experiments(self, box):
    lines = get_lines(box)
    box['title'] = ''
    box['description'] = lines
    box['description_type'] = 'linklist'
    return box


@augment_resource((JSON, PICKLED))
def project_experimentstable(self, box):
    column_number = len(box[PICKLED]['table_description'])
    js = """
   function makeExperimentLink(dataTable, rowNum){
       return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/' + dataTable.getValue(rowNum, 1) + '/' + dataTable.getValue(rowNum, 2) + '/statistics/experiments' + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 2) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
   }
   view.setColumns([{calc:makeExperimentLink, type:'string', label:'Experiment'},%s]);
""" % str(range(3, column_number))[1:-1]
    # e.g.
    # >>> str(range(2, 4))[1:-1]
    # '2, 3'
    box['javascript'] = js
    return box


@augment_resource((JSON, PICKLED,))
def project_experiment_subset_selection(self, box):
    js = """
   function makeExperimentSubsetLink(dataTable, rowNum){
       return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/experiment/subset/' + dataTable.getValue(rowNum, 1) + '/' + dataTable.getValue(rowNum, 2) + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 4) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
   }
   view.setColumns([3, {calc:makeExperimentSubsetLink, type:'string', label:'Parameter Value'}, 5]);
"""
    box['javascript'] = js
    return box


@augment_resource((JSON, PICKLED))
def project_experiment_subset(self, box):
    column_number = len(box[PICKLED]['table_description'])
    js = """
   function makeExperimentLink(dataTable, rowNum){
       return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/' + dataTable.getValue(rowNum, 1) + '/' + dataTable.getValue(rowNum, 2) + '/statistics/experiments' + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 2) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
   }
   view.setColumns([{calc:makeExperimentLink, type:'string', label:'Experiment'},%s]);
""" % str(range(3, column_number))[1:-1]
    # e.g.
    # >>> str(range(2, 4))[1:-1]
    # '2, 3'
    box['javascript'] = js
    return box


@augment_resource((JSON,))
def project_downloads(self, box):
    js = """
   function makeDownloadLink(dataTable, rowNum){
       return String.fromCharCode('60') + 'a href=\"' + dataTable.getValue(rowNum, 3) + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 0) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
   }
   view.setColumns([1,2,{calc:makeDownloadLink, type:'string', label:'.csv File Download Link'}]);
    """
    box['javascript'] = js
    return box


@augment_resource((JSON,))
def rnadashboard(self, box):
    box['title'] = ''
    return box


@augment_resource((JSON,))
def rnadashboard_results(self, box):
    return box


@augment_resource((PICKLED,))
def experiment_sample_info(self, box):
    return _sample_info(self, box)


@augment_resource((PICKLED,))
def run_sample_info(self, box):
    return _sample_info(self, box)


def _sample_info(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'Sample Information'
    box['description'] = []
    if line:
        if line['Species']:
            box['description'].append({'Species': line['Species']})
        if line['Cell Type']:
            box['description'].append({'Cell Type': line['Cell Type']})
        if line['RNA Type']:
            box['description'].append({'RNA Type': line['RNA Type']})
        if line['Compartment']:
            box['description'].append({'Compartment': line['Compartment']})
        if line['Bio Replicate']:
            box['description'].append({'Bio Replicate': line['Bio Replicate']})
        if line['Date']:
            box['description'].append({'Date': line['Date']})
    box['description_type'] = 'properties'
    return box


@augment_resource((PICKLED,))
def experiment_mapping_info(self, box):
    return _mapping_info(self, box)


@augment_resource((PICKLED,))
def run_mapping_info(self, box):
    return _mapping_info(self, box)


@augment_resource((PICKLED,))
def lane_mapping_info(self, box):
    return _mapping_info(self, box)


def _mapping_info(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'Mapping Information'
    box['description'] = []
    if line:
        add = box['description'].append
        if line.get('Read Length', ''):
            add({'Read Length': line['Read Length']})
        if line.get('Mismatches', ''):
            add({'Mismatches': line['Mismatches']})
        if line.get('Annotation Version', ''):
            add({'Annotation Version': line['Annotation Version']})
        if line.get('Annotation Source', ''):
            add({'Annotation Source': line['Annotation Source']})
        if line.get('Genome Assembly', ''):
            add({'Genome Assembly': line['Genome Assembly']})
        if line.get('Genome Source', ''):
            add({'Genome Source': line['Genome Source']})
        if line.get('Genome Gender', ''):
            add({'Genome Gender': line['Genome Gender']})
        if line.get('UCSC Custom Track', '') != "":
            link = """<a target="_blank" href="%(href)s">%(content)s</a>"""
            parts = {'href': line['UCSC Custom Track'],
                     'content': "Display as a custom track at UCSC"}
            add({'Visualization': link % parts})
    box['description_type'] = 'properties'
    return box


@augment_resource((JSON,))
def experiment_read_summary(self, box):
    pass


@augment_resource((JSON,))
def run_read_summary(self, box):
    pass


@augment_resource((JSON,))
def lane_read_summary(self, box):
    pass


@augment_resource((JSON,))
def experiment_mapping_summary(self, box):
    pass


@augment_resource((JSON,))
def run_mapping_summary(self, box):
    pass


@augment_resource((JSON,))
def lane_mapping_summary(self, box):
    pass


@augment_resource((JSON,))
def experiment_expression_summary(self, box):
    pass


@augment_resource((JSON,))
def run_expression_summary(self, box):
    pass


@augment_resource((JSON,))
def lane_expression_summary(self, box):
    pass


@augment_resource((JSON,))
def experiment_splicing_summary(self, box):
    pass


@augment_resource((JSON,))
def run_splicing_summary(self, box):
    pass


@augment_resource((JSON,))
def lane_splicing_summary(self, box):
    pass


@augment_resource((JSON, PICKLED))
def experiment_reads_containing_ambiguous_nucleotides(self, box):
    return _custom_spaced_chart(self, box)


@augment_resource((JSON, PICKLED))
def run_reads_containing_ambiguous_nucleotides(self, box):
    return _custom_spaced_chart(self, box)


@augment_resource((JSON, PICKLED))
def experiment_reads_containing_only_unambiguous_nucleotides(self, box):
    return _custom_spaced_chart(self, box)


@augment_resource((JSON, PICKLED))
def run_reads_containing_only_unambiguous_nucleotides(self, box):
    return _custom_spaced_chart(self, box)


@augment_resource((JSON, PICKLED))
def experiment_average_percentage_of_unique_reads(self, box):
    return _custom_spaced_chart(self, box)


@augment_resource((JSON, PICKLED))
def run_average_percentage_of_unique_reads(self, box):
    return _custom_spaced_chart(self, box)


@augment_resource((JSON,))
def experiment_total_ambiguous_and_unambiguous_reads(self, box):
    pass


@augment_resource((JSON,))
def run_total_ambiguous_and_unambiguous_reads(self, box):
    pass


@augment_resource((JSON,))
def lane_total_ambiguous_and_unambiguous_reads(self, box):
    pass


@augment_resource((JSON,))
def experiment_average_and_average_unique_reads(self, box):
    pass


@augment_resource((JSON,))
def run_average_and_average_unique_reads(self, box):
    pass


@augment_resource((JSON,))
def lane_average_and_average_unique_reads(self, box):
    pass


@augment_resource((JSON, PICKLED))
def experiment_percentage_of_reads_with_ambiguous_bases(self, box):
    return _percentage_of_reads_with_ambiguous_bases(self, box)


@augment_resource((JSON, PICKLED))
def run_percentage_of_reads_with_ambiguous_bases(self, box):
    return _percentage_of_reads_with_ambiguous_bases(self, box)


@augment_resource((JSON, PICKLED))
def lane_percentage_of_reads_with_ambiguous_bases(self, box):
    return _percentage_of_reads_with_ambiguous_bases(self, box)


@augment_resource((JSON, PICKLED))
def experiment_quality_score_by_position(self, box):
    return _position(self, box)


@augment_resource((JSON, PICKLED))
def run_quality_score_by_position(self, box):
    return _position(self, box)


@augment_resource((JSON, PICKLED))
def lane_quality_score_by_position(self, box):
    return _position(self, box)


@augment_resource((JSON, PICKLED))
def experiment_ambiguous_bases_per_position(self, box):
    return _position(self, box)


@augment_resource((JSON, PICKLED))
def run_ambiguous_bases_per_position(self, box):
    return _position(self, box)


@augment_resource((JSON, PICKLED))
def lane_ambiguous_bases_per_position(self, box):
    return _position(self, box)


@augment_resource((JSON, PICKLED))
def experiment_merged_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def run_merged_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def lane_merged_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def experiment_genome_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def run_genome_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def lane_genome_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def experiment_junction_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def run_junction_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def lane_junction_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def experiment_split_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def run_split_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def lane_split_mapped_reads(self, box):
    return _mapped_reads(self, box)


@augment_resource((JSON, PICKLED))
def experiment_detected_genes(self, box):
    return _detected_genes(self, box)


@augment_resource((JSON, PICKLED))
def run_detected_genes(self, box):
    return _detected_genes(self, box)


@augment_resource((JSON, PICKLED))
def lane_detected_genes(self, box):
    return _detected_genes(self, box)


@augment_resource((JSON,))
def experiment_gene_expression_profile(self, box):
    return _gene_expression_profile(self, box)


@augment_resource((JSON,))
def run_gene_expression_profile(self, box):
    return _gene_expression_profile(self, box)


@augment_resource((JSON,))
def lane_gene_expression_profile(self, box):
    return _gene_expression_profile(self, box)


@augment_resource((JSON,))
def experiment_gene_expression_levels(self, box):
    pass


@augment_resource((JSON,))
def run_gene_expression_levels(self, box):
    pass


@augment_resource((JSON,))
def lane_gene_expression_levels(self, box):
    pass


@augment_resource((JSON, PICKLED))
def experiment_top_genes(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def run_top_genes(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def lane_top_genes(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def experiment_top_transcripts(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def run_top_transcripts(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def lane_top_transcripts(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def experiment_top_exons(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def run_top_exons(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON, PICKLED))
def lane_top_exons(self, box):
    return _thousands_formatter(self, box)


@augment_resource((JSON,))
def experiment_exon_inclusion_profile(self, box):
    return _exon_inclusion_profile(self, box)


@augment_resource((JSON,))
def run_exon_inclusion_profile(self, box):
    return _exon_inclusion_profile(self, box)


@augment_resource((JSON,))
def lane_exon_inclusion_profile(self, box):
    return _exon_inclusion_profile(self, box)


@augment_resource((JSON,))
def experiment_reads_supporting_exon_inclusions(self, box):
    pass


@augment_resource((JSON,))
def run_reads_supporting_exon_inclusions(self, box):
    pass


@augment_resource((JSON,))
def lane_reads_supporting_exon_inclusions(self, box):
    pass


@augment_resource((JSON,))
def experiment_novel_junctions_from_annotated_exons(self, box):
    pass


@augment_resource((JSON,))
def run_novel_junctions_from_annotated_exons(self, box):
    pass


@augment_resource((JSON,))
def lane_novel_junctions_from_annotated_exons(self, box):
    pass


@augment_resource((JSON,))
def experiment_novel_junctions_from_unannotated_exons(self, box):
    pass


@augment_resource((JSON,))
def run_novel_junctions_from_unannotated_exons(self, box):
    pass


@augment_resource((JSON,))
def lane_novel_junctions_from_unannotated_exons(self, box):
    pass


def _exon_inclusion_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box


def _gene_expression_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    hAxis = '''{logScale:true}'''
    box['chartoptions']['hAxis'] = hAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box


def _custom_spaced_chart(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''


def _thousands_formatter(self, box):
    # Need to extract some infos from the table, so load the pickled Python code
    table = box[PICKLED]
    i = 0
    for column, column_type in table['table_description']:
        if column_type == 'number':
            box['javascript'] += """thousandsformatter.format(data, %s);\n""" % i
        i = i + 1
    return box


def _detected_genes(self, box):
    box['javascript'] = ""
    # Need to extract some infos from the table, so load the pickled Python code
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(1, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box


def _mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea


def _percentage_of_reads_with_ambiguous_bases(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 60, 160)
    box['chartoptions']['height'] = str(height)


def _position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640

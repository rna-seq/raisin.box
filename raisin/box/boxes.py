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
    # pylint: disable-msg=C0103
    # This class is used as a decorator, so allow lower case name

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

# pylint: disable-msg=C0103
# XXX method names are too long
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
def replicate_about(context, box):
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
    javascript = """
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
    box['javascript'] = javascript
    return box


@augment((JSON, PICKLED,))
def project_experiment_subset_start(context, box):
    """Augment resource."""
    return box


@augment((JSON, PICKLED,))
def project_experiment_subset_selection(context, box):
    """Augment resource."""
    javascript = """
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
    box['javascript'] = javascript
    return box


@augment((JSON, PICKLED))
def project_experiment_subset(context, box):
    """Augment resource."""
    column_number = len(box[PICKLED]['table_description'])
    javascript = """
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
    box['javascript'] = javascript
    return box


@augment((JSON, PICKLED,))
def project_experiment_subset_pending(context, box):
    """Augment resource."""
    return box


@augment((JSON,))
def project_downloads(context, box):
    """Augment resource."""
    javascript = """
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
    box['javascript'] = javascript
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
def replicate_sample_info(context, box):
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
        if lines['Localization']:
            box['description'].append({'Localization': lines['Localization']})
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
def replicate_mapping_info(context, box):
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
    box['description_type'] = 'properties'
    return box


@augment((JSON,))
def experiment_read_summary(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def replicate_read_summary(context, box):
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
def replicate_mapping_summary(context, box):
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
def replicate_expression_summary(context, box):
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
def replicate_splicing_summary(context, box):
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
def replicate_reads_containing_ambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def experiment_reads_containing_only_unambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def replicate_reads_containing_only_unambiguous_nucleotides(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def experiment_average_percentage_of_unique_reads(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON, PICKLED))
def replicate_average_percentage_of_unique_reads(context, box):
    """Augment resource."""
    return _custom_spaced_chart(context, box)


@augment((JSON,))
def experiment_total_ambiguous_and_unambiguous_reads(context, box):
    """Augment resource."""
    pass


@augment((JSON,))
def replicate_total_ambiguous_and_unambiguous_reads(context, box):
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
def replicate_average_and_average_unique_reads(context, box):
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
def replicate_percentage_of_reads_with_ambiguous_bases(context, box):
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
def replicate_quality_score_by_position(context, box):
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
def replicate_ambiguous_bases_per_position(context, box):
    """Augment resource."""
    return _position(context, box)


@augment((JSON, PICKLED))
def lane_ambiguous_bases_per_position(context, box):
    """Augment resource."""
    return _position(context, box)

@augment((JSON, PICKLED))
def experiment_read_distribution(self, box):
    """
    The sparklines need to be inserted into the HTML table cells of the read distribution table.
    
    For each lane, the read distributions for the different length categories are shown.
    
    There is a div with a specific target id for each Google Charts Data View on the Google Charts
    Data Table.

    This is the target div for the overall distribution of the first lane:
    
    <div id="read_distribution_0_0_div">

    This is the target div for the overall distribution of the second lane:        

    <div id="read_distribution_1_0_div">

    This is the target div for the second range (100-999):
    
    <div id="read_distribution_1_2_div">
    """
    box['javascript'] = ""
     
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    
    # Fetch the lane names from the table        
    lane_names = list(set([item[0] for item in table['table_data']]))
    lane_names.sort()
    
    # Fetch the starts from the table        
    starts = list(set([item[1] for item in table['table_data']]))
    starts.sort()
    
    # Calculate the ranges given the starts        
    ranges = {}
    for pos in range(0, len(starts)):
        if pos == len(starts)-1:
            # The last range goes to infinity
            ranges[starts[pos]] = (str(starts[pos]), 'n')
        else:
            # The range goes until just before the start of the next range
            ranges[starts[pos]] = (str(starts[pos]), str(starts[pos+1] - 1))       

    # Dynamically fill in the table structure in the read distribution HTML div element
    js = ""
    js += """document.getElementById('experiment_read_distribution_div').innerHTML='"""
    js += """<table class="minicharttable"><tr><td>Distribution</td><td>Lane ID</td>"""
    
    # Ignore the first start (0), which is reserved for the overall read distribution
    for start in starts[1:]:
        js += """<td>%s - %s</td>""" % (ranges[start][0], ranges[start][1])
    js +=     """</tr>"""
    # Fill in the rows for each labe        
    for lane_name in lane_names:
        js += """<tr><td><div id="read_distribution_%s_0_div"></div></td><td style="vertical-align: middle;">%s</td>""" % (lane_names.index(lane_name), lane_name)
        # Fill in the cells for the individual read distributions
        for start in starts[1:]:
            js += '<td>'
            js += """<div id="read_distribution_%s_%s_div"></div>""" % (lane_names.index(lane_name), starts.index(start))
            js += '</td>'
        js += '</tr>'
    js += """</table>'"""
    box['javascript'] = js

    # Create the JavaScript code for the div tags that were just dynamically added
    for lane in lane_names:            
        for start in starts:
            # Add a new view for each range of each lane
            box['javascript'] = box['javascript'] + """
var view = new google.visualization.DataView(data);
view.setRows(data.getFilteredRows([{column: 0, value: '%s'}, {column: 1, value: %s}]))
view.setColumns([3])
var chart = new google.visualization.ImageSparkLine(document.getElementById('read_distribution_%s_%s_div'));
chart.draw(view, {width: 100, height: 100, showAxisLines: false,  showValueLabels: false, labelPosition: 'none'});
""" % (lane, # The first filter on the data table is by lane 
   start, # The second filter on the data table is by start
   lane_names.index(lane), # The index of the lane is used for the id of the target div
   starts.index(start)) # The index of the range is also used for the id of the target div

    return box

@augment((JSON, PICKLED))
def run_read_distribution(self, box):
    """
    The sparklines need to be inserted into the HTML table cells of the read distribution table.
    
    For each lane, the read distributions for the different length categories are shown.
    
    There is a div with a specific target id for each Google Charts Data View on the Google Charts
    Data Table.

    This is the target div for the overall distribution of the first lane:
    
    <div id="read_distribution_0_0_div">

    This is the target div for the overall distribution of the second lane:        

    <div id="read_distribution_1_0_div">

    This is the target div for the second range (100-999):
    
    <div id="read_distribution_1_2_div">
    """
    box['javascript'] = ""
     
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    
    # Fetch the lane names from the table        
    lane_names = list(set([item[0] for item in table['table_data']]))
    lane_names.sort()
    
    # Fetch the starts from the table        
    starts = list(set([item[1] for item in table['table_data']]))
    starts.sort()
    
    # Calculate the ranges given the starts        
    ranges = {}
    for pos in range(0, len(starts)):
        if pos == len(starts)-1:
            # The last range goes to infinity
            ranges[starts[pos]] = (str(starts[pos]), 'n')
        else:
            # The range goes until just before the start of the next range
            ranges[starts[pos]] = (str(starts[pos]), str(starts[pos+1] - 1))       

    # Dynamically fill in the table structure in the read distribution HTML div element
    js = ""
    js += """document.getElementById('read_distribution_div').innerHTML='"""
    js += """<table class="minicharttable"><tr><td>Distribution</td><td>Lane ID</td>"""
    
    # Ignore the first start (0), which is reserved for the overall read distribution
    for start in starts[1:]:
        js += """<td>%s - %s</td>""" % (ranges[start][0], ranges[start][1])
    js +=     """</tr>"""
    # Fill in the rows for each labe        
    for lane_name in lane_names:
        js += """<tr><td><div id="read_distribution_%s_0_div"></div></td><td style="vertical-align: middle;">%s</td>""" % (lane_names.index(lane_name), lane_name)
        # Fill in the cells for the individual read distributions
        for start in starts[1:]:
            js += '<td>'
            js += """<div id="read_distribution_%s_%s_div"></div>""" % (lane_names.index(lane_name), starts.index(start))
            js += '</td>'
        js += '</tr>'
    js += """</table>'"""
    box['javascript'] = js

    # Create the JavaScript code for the div tags that were just dynamically added
    for lane in lane_names:            
        for start in starts:
            # Add a new view for each range of each lane
            box['javascript'] = box['javascript'] + """
var view = new google.visualization.DataView(data);
view.setRows(data.getFilteredRows([{column: 0, value: '%s'}, {column: 1, value: %s}]))
view.setColumns([3])
var chart = new google.visualization.ImageSparkLine(document.getElementById('read_distribution_%s_%s_div'));
chart.draw(view, {width: 100, height: 100, showAxisLines: false,  showValueLabels: false, labelPosition: 'none'});
""" % (lane, # The first filter on the data table is by lane 
   start, # The second filter on the data table is by start
   lane_names.index(lane), # The index of the lane is used for the id of the target div
   starts.index(start)) # The index of the range is also used for the id of the target div

    return box

@augment((JSON, PICKLED))
def lane_read_distribution(self, box):
    """
    The sparklines need to be inserted into the HTML table cells of the read distribution table.
    
    For each lane, the read distributions for the different length categories are shown.
    
    There is a div with a specific target id for each Google Charts Data View on the Google Charts
    Data Table.

    This is the target div for the overall distribution of the first lane:
    
    <div id="read_distribution_0_0_div">

    This is the target div for the overall distribution of the second lane:        

    <div id="read_distribution_1_0_div">

    This is the target div for the second range (100-999):
    
    <div id="read_distribution_1_2_div">
    """
    box['javascript'] = ""
     
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    
    # Fetch the lane names from the table        
    lane_names = list(set([item[0] for item in table['table_data']]))
    lane_names.sort()
    
    # Fetch the starts from the table        
    starts = list(set([item[1] for item in table['table_data']]))
    starts.sort()
    
    # Calculate the ranges given the starts        
    ranges = {}
    for pos in range(0, len(starts)):
        if pos == len(starts)-1:
            # The last range goes to infinity
            ranges[starts[pos]] = (str(starts[pos]), 'n')
        else:
            # The range goes until just before the start of the next range
            ranges[starts[pos]] = (str(starts[pos]), str(starts[pos+1] - 1))       

    # Dynamically fill in the table structure in the read distribution HTML div element
    js = ""
    js += """document.getElementById('read_distribution_div').innerHTML='"""
    js += """<table class="minicharttable"><tr><td>Distribution</td><td>Lane ID</td>"""
    
    # Ignore the first start (0), which is reserved for the overall read distribution
    for start in starts[1:]:
        js += """<td>%s - %s</td>""" % (ranges[start][0], ranges[start][1])
    js +=     """</tr>"""
    # Fill in the rows for each labe        
    for lane_name in lane_names:
        js += """<tr><td><div id="read_distribution_%s_0_div"></div></td><td style="vertical-align: middle;">%s</td>""" % (lane_names.index(lane_name), lane_name)
        # Fill in the cells for the individual read distributions
        for start in starts[1:]:
            js += '<td>'
            js += """<div id="read_distribution_%s_%s_div"></div>""" % (lane_names.index(lane_name), starts.index(start))
            js += '</td>'
        js += '</tr>'
    js += """</table>'"""
    box['javascript'] = js

    # Create the JavaScript code for the div tags that were just dynamically added
    for lane in lane_names:            
        for start in starts:
            # Add a new view for each range of each lane
            box['javascript'] = box['javascript'] + """
var view = new google.visualization.DataView(data);
view.setRows(data.getFilteredRows([{column: 0, value: '%s'}, {column: 1, value: %s}]))
view.setColumns([3])
var chart = new google.visualization.ImageSparkLine(document.getElementById('read_distribution_%s_%s_div'));
chart.draw(view, {width: 100, height: 100, showAxisLines: false,  showValueLabels: false, labelPosition: 'none'});
""" % (lane, # The first filter on the data table is by lane 
   start, # The second filter on the data table is by start
   lane_names.index(lane), # The index of the lane is used for the id of the target div
   starts.index(start)) # The index of the range is also used for the id of the target div

    return box

@augment((JSON, PICKLED))
def experiment_merged_mapped_reads(context, box):
    """Augment resource."""
    return _mapped_reads(context, box)


@augment((JSON, PICKLED))
def replicate_merged_mapped_reads(context, box):
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
def replicate_genome_mapped_reads(context, box):
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
def replicate_junction_mapped_reads(context, box):
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
def replicate_split_mapped_reads(context, box):
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
def replicate_detected_genes(context, box):
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
def replicate_gene_expression_profile(context, box):
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
def replicate_gene_expression_levels(context, box):
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
def replicate_top_genes(context, box):
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
def replicate_top_transcripts(context, box):
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
def replicate_top_exons(context, box):
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
def replicate_exon_inclusion_profile(context, box):
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
def replicate_reads_supporting_exon_inclusions(context, box):
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
def replicate_novel_junctions_from_annotated_exons(context, box):
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
def replicate_novel_junctions_from_unannotated_exons(context, box):
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
    index = 0
    column_types = [desc[1] for desc in table['table_description']]
    for column_type in column_types:
        if column_type == 'number':
            box['javascript'] += javascript % index
        index += 1
    return box


def _detected_genes(context, box):
    """Augment resource."""
    box['javascript'] = ""
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for index in range(1, len(table['table_description'])):
        formatter = """thousandsformatter.format(data, %s);\n""" % index
        box['javascript'] += formatter
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

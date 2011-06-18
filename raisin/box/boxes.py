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
    """
    This is a decorator to be used on the methods like this:

    @augment_resource((JSON,PICKLED))
    def project_meta(self, box):

    The list of formats needed during the method are given as the formats parameter.

    * JSON is always needed when a resource is fetched from a remote server
    
    * PICKLED is needed when you need to do some calculations.

    This is how to use the information from the pickled information: 

    box['description'] = [{'Species': box[PICKLED]['species']}]
    """
    
    def __init__(self, formats):
        self.formats = formats

    def __call__(self, wrapped=None):
        if wrapped:
            resources_registry.append( (wrapped.__name__, wrapped, self.formats, ) )

def get_lines(box):
    if not box[PICKLED].has_key('table_description'):
        raise AttributeError, str(box)
    if not box[PICKLED].has_key('table_data'):
        raise AttributeError, str(box)
    table = gviz_api.DataTable( box[PICKLED]['table_description'], box[PICKLED]['table_data'] )
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
       return String.fromCharCode('60') + 'a href=\"/project/' + dataTable.getValue(rowNum, 0) + '/experiment/' + dataTable.getValue(rowNum, 1) + '/statistics/overview' + '\"' + String.fromCharCode('62') + dataTable.getValue(rowNum, 1) + String.fromCharCode('60') + '/a' + String.fromCharCode('62');
   }   
   view.setColumns([{calc:makeExperimentLink, type:'string', label:'Experiment'},%s]);
""" % str(range(2, column_number))[1:-1] 
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

@augment_resource((PICKLED,))
def experiment_sample_info(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'Sample Information'
    box['description'] = []
    if line:
        if line.get('Species',''):
            box['description'].append({'Species': line['Species']})
        if line.get('Cell Type', ''):
            box['description'].append({'Cell Type': line['Cell Type']})
        if line.get('RNA Type', ''):
            box['description'].append({'RNA Type': line['RNA Type']})
        if line.get('Compartment', ''):
            box['description'].append({'Compartment': line['Compartment']})
        if line.get('Bio Replicate', ''):
            box['description'].append({'Bio Replicate': line['Bio Replicate']})
        if line.get('Date', ''):
            box['description'].append({'Date': line['Date']})
    box['description_type'] = 'properties'
    return box            

@augment_resource((PICKLED,))
def run_sample_info(self, box):
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
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'Mapping Information'
    box['description'] = []
    if line:
        if line.get('Read Length', ''):
            box['description'].append({'Read Length': line['Read Length']})
        if line.get('Mismatches', ''):
            box['description'].append({'Mismatches': line['Mismatches']})
        if line.get('Annotation Version', ''):
            box['description'].append({'Annotation Version': line['Annotation Version']})
        if line.get('Annotation Source', ''):
            box['description'].append({'Annotation Source': line['Annotation Source']})
        if line.get('Genome Assembly', ''):
            box['description'].append({'Genome Assembly': line['Genome Assembly']})
        if line.get('Genome Source', ''):
            box['description'].append({'Genome Source': line['Genome Source']})
        if line.get('Genome Gender', ''):
            box['description'].append({'Genome Gender': line['Genome Gender']})
        if line.get('UCSC Custom Track', '') != "":
            link = """<a target="_blank" href="%s">Display as a custom track at UCSC</a>"""
            box['description'].append({'Visualization': link % (line['UCSC Custom Track'])})
    box['description_type'] = 'properties'
    return box            

@augment_resource((PICKLED,))
def run_mapping_info(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'Mapping Information'
    box['description'] = []
    if line:
        if line['Read Length']:
            box['description'].append({'Read Length': line['Read Length']})
        if line['Mismatches']:
            box['description'].append({'Mismatches': line['Mismatches']})
        if line['Annotation Version']:
            box['description'].append({'Annotation Version': line['Annotation Version']})
        if line['Annotation Source']:
            box['description'].append({'Annotation Source': line['Annotation Source']})
        if line['Genome Assembly']:
            box['description'].append({'Genome Assembly': line['Genome Assembly']})
        if line['Genome Source']:
            box['description'].append({'Genome Source': line['Genome Source']})
        if line['Genome Gender']:
            box['description'].append({'Genome Gender': line['Genome Gender']})
        if line['UCSC Custom Track'] != "":
            link = """<a target="_blank" href="%s">Display as a custom track at UCSC</a>"""
            box['description'].append({'Visualization': link % (line['UCSC Custom Track'])})
    box['description_type'] = 'properties'
    return box            

@augment_resource((PICKLED,))
def lane_mapping_info(self, box):
    lines = get_lines(box)
    line = {}
    try:
        line = lines.next()
    except StopIteration:
        pass
    box['title'] = 'Mapping Information'
    box['description'] = []
    if line:
        if line['Read Length']:
            box['description'].append({'Read Length': line['Read Length']})
        if line['Mismatches']:
            box['description'].append({'Mismatches': line['Mismatches']})
        if line['Annotation Version']:
            box['description'].append({'Annotation Version': line['Annotation Version']})
        if line['Annotation Source']:
            box['description'].append({'Annotation Source': line['Annotation Source']})
        if line['Genome Assembly']:
            box['description'].append({'Genome Assembly': line['Genome Assembly']})
        if line['Genome Source']:
            box['description'].append({'Genome Source': line['Genome Source']})
        if line['Genome Gender']:
            box['description'].append({'Genome Gender': line['Genome Gender']})
        if line['UCSC Custom Track'] != "":
            link = """<a target="_blank" href="%s">Display as a custom track at UCSC</a>"""
            box['description'].append({'Visualization': link % (line['UCSC Custom Track'])})
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
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''
    
@augment_resource((JSON, PICKLED))
def run_reads_containing_ambiguous_nucleotides(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''



@augment_resource((JSON, PICKLED))
def experiment_reads_containing_only_unambiguous_nucleotides(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''
    
@augment_resource((JSON, PICKLED))
def run_reads_containing_only_unambiguous_nucleotides(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''


@augment_resource((JSON, PICKLED))
def experiment_average_percentage_of_unique_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''

@augment_resource((JSON, PICKLED))
def run_average_percentage_of_unique_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"60%"}'''
    box['chartoptions']['chartArea'] = chartArea
    box['chartoptions']['hAxis'] = '''{minValue:"0"}'''

    
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
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 30, 160)
    box['chartoptions']['height'] = str(height)

@augment_resource((JSON, PICKLED))
def run_percentage_of_reads_with_ambiguous_bases(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 60, 160)
    box['chartoptions']['height'] = str(height)

@augment_resource((JSON, PICKLED))
def lane_percentage_of_reads_with_ambiguous_bases(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 60, 160)
    box['chartoptions']['height'] = str(height)
        
@augment_resource((JSON, PICKLED))
def experiment_quality_score_by_position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640

@augment_resource((JSON, PICKLED))
def run_quality_score_by_position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    
@augment_resource((JSON, PICKLED))
def lane_quality_score_by_position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    
    
@augment_resource((JSON, PICKLED))
def experiment_ambiguous_bases_per_position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640

@augment_resource((JSON, PICKLED))
def run_ambiguous_bases_per_position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640

@augment_resource((JSON, PICKLED))
def lane_ambiguous_bases_per_position(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640

@augment_resource((JSON, PICKLED))
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

@augment_resource((JSON, PICKLED))
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

@augment_resource((JSON, PICKLED))
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


        

        

@augment_resource((JSON, PICKLED))
def experiment_merged_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def run_merged_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def lane_merged_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea
                
@augment_resource((JSON, PICKLED))
def experiment_genome_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def run_genome_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def lane_genome_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea
        
@augment_resource((JSON, PICKLED))
def experiment_junction_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def run_junction_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def lane_junction_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea
        
@augment_resource((JSON, PICKLED))
def experiment_split_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def run_split_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea

@augment_resource((JSON, PICKLED))
def lane_split_mapped_reads(self, box):
    # Need to extract some infos from the table, so load the pickled dictionary
    table = box[PICKLED]
    height = max(len(table['table_data']) * 40, 100)
    box['chartoptions']['height'] = str(height)
    chartArea = '''{left:"20%", right:"20%", top:"5%",width:"60%",height:"90%"}'''
    box['chartoptions']['chartArea'] = chartArea
        
@augment_resource((JSON, PICKLED))                        
def experiment_detected_genes(self, box):
    box['javascript'] = ""
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(1, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))
def run_detected_genes(self, box):
    box['javascript'] = ""
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(1, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box
    
@augment_resource((JSON, PICKLED))
def lane_detected_genes(self, box):
    box['javascript'] = ""
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(1, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON,))                        
def experiment_gene_expression_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    hAxis = '''{logScale:true}'''
    box['chartoptions']['hAxis'] = hAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box

@augment_resource((JSON,))                        
def run_gene_expression_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    hAxis = '''{logScale:true}'''
    box['chartoptions']['hAxis'] = hAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box

@augment_resource((JSON,))                        
def lane_gene_expression_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    hAxis = '''{logScale:true}'''
    box['chartoptions']['hAxis'] = hAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box
    
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
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(6, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def run_top_genes(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(6, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def lane_top_genes(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(6, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def experiment_top_transcripts(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(5, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def run_top_transcripts(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(5, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def lane_top_transcripts(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(5, len(table['table_description'])):
        box['javascript'] = box['javascript'] + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def experiment_top_exons(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(4, len(table['table_description'])):
        box['javascript'] = box.get('javascript', '') + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def run_top_exons(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(4, len(table['table_description'])):
        box['javascript'] = box.get('javascript', '') + """thousandsformatter.format(data, %s);\n""" % i
    return box

@augment_resource((JSON, PICKLED))                        
def lane_top_exons(self, box):
    # Need to extract some infos from the table, so load the pickled Python code       
    table = box[PICKLED]
    # Add formatting for expression values of lanes
    for i in range(4, len(table['table_description'])):
        box['javascript'] = box.get('javascript', '') + """thousandsformatter.format(data, %s);\n""" % i
    return box


@augment_resource((JSON,))                        
def experiment_exon_inclusion_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box

@augment_resource((JSON,))                        
def run_exon_inclusion_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box

@augment_resource((JSON,))                        
def lane_exon_inclusion_profile(self, box):
    vAxis = '''{logScale:true}'''
    box['chartoptions']['vAxis'] = vAxis
    box['chartoptions']['width'] = 900
    box['chartoptions']['height'] = 640
    chartArea = '''{left:"10%", right:"10%",width:"60%",top:20,height:540}'''
    box['chartoptions']['chartArea'] = chartArea
    return box
    
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

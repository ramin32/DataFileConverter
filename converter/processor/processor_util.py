import re
from lxml import etree
import processor

namespace_re = re.compile('{.*}')

processor_mapping = {processor.XmlProcessor.ID: processor.XmlProcessor, 
                     processor.CsvProcessor.ID: processor.CsvProcessor}


def clean_namespace(string):
    return namespace_re.sub('',string)

def prefix_dictionary_keys(old_d, prefix, separator='_'):
    new_d = {}
    for old_k in old_d:
        new_k = '%s%s%s' % (prefix,separator, old_k)
        new_d[new_k] = old_d[old_k]
    return new_d

    

def element_to_dict_list(element, shareable_siblings, d=None):
    '''returns dict if root_element is in shareable siblings,
    otherwise a dict list is returned of all the dfs traversals.'''

    if d is None:
        d = {}

    root_tag = clean_namespace(element.tag) 

    element_dict = prefix_dictionary_keys(element.attrib, root_tag)
    d.update(element_dict)

    if len(element) is 0:
        return [d]

    child_dict_list=[]
    shareable_dict={}
    dict_count = {}.fromkeys(shareable_siblings, 1)
    for child in element.iterchildren():
        child_tag = clean_namespace(child.tag)
        if child_tag in shareable_siblings:
            index_separator = '_%s_' % dict_count[child_tag]
            shareable_dict.update(prefix_dictionary_keys(child.attrib, child_tag, separator=index_separator))
            dict_count[child_tag] += 1
        else:
            new_d = d.copy()
            child_dict_list += element_to_dict_list(child, shareable_siblings, new_d)

    if len(child_dict_list) is 0:
        d.update(shareable_dict)
        return [d]
    else:
        for c in child_dict_list:
            c.update(shareable_dict)

    return child_dict_list


field_prefix_re = re.compile('^[a-zA-Z1-9]+_') #includes shareable
def get_prefix(string):
    return field_prefix_re.match(string).group()
def remove_prefix(string):
    return field_prefix_re.sub('', string)

def group_by_elements(node_name, child_node, dict_list, matching_fields, shareable_siblings):
    elements = []
    field_mapping = {f:remove_prefix(f) for f in  matching_fields}

    for d in dict_list:
        d_attrib = {field_mapping[f]:d[f].strip() for f in matching_fields}

        if node_name in shareable_siblings:
            ## initialize dicts for each shareable attrib
            shareable_attrib = {get_prefix(a):{} for a in d_attrib}
            for a in d_attrib:
                shareable_attrib[get_prefix(a)][remove_prefix(a)] = d_attrib[a]   
            d_attrib_list = shareable_attrib.values()
        else:
            d_attrib_list = [d_attrib]
#
        #for d_attrib in d_attrib_list:
        # add if a child node exists or leaf node has attributes set

        for d_a_l  in d_attrib_list:
            if any(d_a_l.values()) or child_node:
                added = False
                for (elem, sublist) in elements:
                    if elem.attrib == d_a_l:
                        sublist.append(d)
                        added = True
                if not added:
                    elem = etree.Element(node_name)
                    elem.attrib.update(d_a_l)
                    elements.append((elem, [d]))

    return elements


def dict_list_to_elements(dict_list,field_names, hierachy, shareable_siblings):
    elements = []
    if not dict_list or not hierachy:
        return elements

    for node_name in hierachy:
        if node_name:
            matching_fields = [field for field in field_names if field.startswith(node_name)]
            for (elem, dict_sublist) in group_by_elements(node_name, hierachy[node_name], dict_list, matching_fields, shareable_siblings):
                elements.append(elem)
                for child_elem in dict_list_to_elements(dict_sublist, field_names, hierachy[node_name], shareable_siblings):
                    elem.append(child_elem)

    return elements

class InvalidFormatTypeError(KeyError):
    pass

def create_processor(processor_type, format_file, config):
    try:
        return processor_mapping[processor_type](format_file, config)
    except KeyError as k:
        raise InvalidFormatTypeError(k)




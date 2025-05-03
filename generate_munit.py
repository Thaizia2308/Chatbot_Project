import os
from lxml import etree
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

def parse_flow(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()
    
    ns = {'mule': 'http://www.mulesoft.org/schema/mule/core'}

    flow_elem = root.xpath('//mule:flow', namespaces=ns)[0]
    flow_name = flow_elem.attrib['name']
    
    components = flow_elem.getchildren()
    mocks = []

    for c in components:
        tag = etree.QName(c.tag).localname
        if 'db:select' in c.tag:
            mocks.append({
                'processor': 'db:select',
                'config_ref': c.attrib.get('config-ref', ''),
                'payload': """
[
  { "id": 1, "name": "Alice" },
  { "id": 2, "name": "Bob" }
]
"""
            })
        elif 'file:write' in c.tag:
            mocks.append({
                'processor': 'file:write',
                'config_ref': '',
                'payload': None
            })

    return flow_name, mocks

def generate_munit_test(flow_path, output_path):
    flow_name, mocks = parse_flow(flow_path)
    template = env.get_template('munit_test_template.xml')
    
    munit_xml = template.render(
        test_name=f"{flow_name}-Test",
        flow_name=flow_name,
        mocks=mocks
    )

    with open(output_path, 'w') as f:
        f.write(munit_xml)

    print(f"MUnit test generated at: {output_path}")
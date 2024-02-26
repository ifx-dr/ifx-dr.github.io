from Extract_class import parse_html, extract_div_from_file, set_div_order, reformat_class_toc
from Op import reformat_properties

html_file = 'C:/Users/LinBoH/myDocumentation/doc/index-en.html'
DR_file = "C:/Users/LinBoH/Desktop/DR_TTL/ifx-dr.github.io/template.html"
lobe_list = ['Cloud_Lobe', 'Organization_Lobe', 'Planning_Lobe', 'Power_Lobe',
            'Process_Lobe', 'Product_Lobe', 'Semiconductor_Development_Lobe',
            'Semiconductor_Production_Lobe', 'Sensor_Lobe', 'Supply_Chain_Lobe',
            'Sustainability_Lobe', 'System_Lobe', 'Time_Lobe', 'Wired_Communication_Lobe']
DR_soup = parse_html(html_file)
extracted_div = dict(extract_div_from_file(DR_soup, lobe_list))
extracted_div = set_div_order(extracted_div, lobe_list)

class_soup, toc_soup, new_namespaces = reformat_class_toc(extracted_div, lobe_list)
op_soup = reformat_properties(DR_soup, 'op')
dp_soup = reformat_properties(DR_soup, 'dp')

template_soup = parse_html(DR_file)

# check namespaces
namespaces = []
namespaces_div = template_soup.find('div', id='namespaces')
iri_codes = namespaces_div.find_all('code')
for iri_code in iri_codes:
    a_tag = iri_code.find('a')
    namespaces.append(a_tag.text.split('#')[0])

diff = list(set(new_namespaces) - set(namespaces))

# insert new classes
classes_div = template_soup.find('div', id='classes')
class_h2_tag = classes_div.find('h2')
class_h2_tag.insert_after(class_soup)
op_div = template_soup.find('div', id='objectproperties')
op_h2_tag = op_div.find('h2')
op_h2_tag.insert_after(op_soup)
dp_div = template_soup.find('div', id='datatypeproperties')
dp_h2_tag = dp_div.find('h2')
dp_h2_tag.insert_after(dp_soup)

ul_div = template_soup.find('ul', class_='second')
ul_div.append(toc_soup)
with open("C:/Users/LinBoH/Desktop/DR_TTL/ifx-dr.github.io/index.html", "w", encoding='utf-8') as file:
    file.write(str(template_soup.prettify()))


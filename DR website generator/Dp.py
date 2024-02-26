from bs4 import BeautifulSoup
from collections import defaultdict

def parse_html(file_path):
    with open(file_path, 'rb') as file:
        return BeautifulSoup(file.read(), 'html.parser')


second_html_file = 'C:/Users/LinBoH/myDocumentation/doc/index-en.html'
soup = parse_html(second_html_file)
new_soup = BeautifulSoup("", 'html.parser')
for div in soup.find_all("div", class_="entity"):
    h3 = div.find('h3')
    if h3 and h3.find('sup', text='dp'):  # Check if h3 and 'sup' with text 'op' exist
        div['class'] = 'property entity'
        div['id'] = div['id'].split('#')[-1]
        span_to_remove = h3.find('span')
        sup_to_remove = h3.find('sup')
        if span_to_remove and sup_to_remove:
            span_to_remove.decompose()
            sup_to_remove.decompose()
        table = soup.new_tag("table")
        div.insert(2, table)  # Insert the table just after the <h3> tag

        # Locate the <p> tag containing the IRI and move it into a <tr>/<td> structure
        iri_paragraph = div.find("p")
        iri_code = iri_paragraph.strong.extract().get_text()
        iri_value = iri_paragraph.extract().get_text().replace(iri_code, '').strip()

        # Create the IRI row
        tr_iri = soup.new_tag("tr")
        table.append(tr_iri)
        th_iri = soup.new_tag("dt")
        th_iri.string = iri_code
        tr_iri.append(th_iri)
        td_iri = soup.new_tag("dd")
        code_iri = soup.new_tag("code")
        code_iri.string = iri_value
        td_iri.append(code_iri)
        tr_iri.append(td_iri)
        tr_dl = soup.new_tag("tr")
        table.append(tr_dl)
        # Locate the <div class="description"> and move its content into the table
        description_div = div.find("div", class_="description")
        try:
            dl = div.find("dl").extract()
            tr_dl.append(dl)


            # Now we must correct the <a> tags' href attribute
            for a_tag in dl.find_all("a"):
                old_href = a_tag['href']
                new_href = old_href.split("#")[-1]
                target_bool = a_tag.get('target')
                if target_bool and a_tag['target'] == '_blank':
                    pass
                else:
                    a_tag['href'] = f"#{new_href}"
                sup_to_remove = a_tag.find_next_sibling('sup')
                if sup_to_remove:
                    if sup_to_remove.text == 'c':
                        a_tag['onclick'] = "opentab(event, 1,2)"
                    elif sup_to_remove.text == 'op':
                        a_tag['onclick'] = "opentab(event, 2,2)"
                    sup_to_remove.decompose()

                # Also remove any remaining commas
                if a_tag.next_sibling.string == ', ':
                    a_tag.next_sibling.extract()

            # Remove the now-empty description div
            description_div.decompose()
        except:
            pass
        new_soup.append(div)
print(new_soup.prettify())
with open("output_dp.html", "w", encoding='utf-8') as file:
    file.write(str(new_soup))

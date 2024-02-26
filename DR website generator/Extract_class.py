import copy

from bs4 import BeautifulSoup
from collections import defaultdict


def parse_html(file_path):
    with open(file_path, 'rb') as file:
        return BeautifulSoup(file.read(), 'html.parser')


def extract_div_from_file(soup, lobe_list):
    div_tags = soup.find_all('div', class_='entity')
    select_div = defaultdict(list)
    for div in div_tags:
        for lobe_name in lobe_list:
            if div.get('id') is not None:
                if lobe_name in div.get('id'):
                    select_div[lobe_name].append(div)
        dt_tags = div.find_all('dt')
        for dt in dt_tags:
            if dt.text == 'has super-classes':
                dd = dt.find_next_sibling('dd')
                for lobe_name in lobe_list:
                    if lobe_name in str(dd):
                        select_div[lobe_name].append(div)
    return select_div


def set_div_order(select_div, lobe_list):
    for lobe in lobe_list:
        for div in select_div[lobe]:
            if lobe in div.get('id'):
                select_div[lobe].remove(div)
                select_div[lobe].insert(0, div)
    return select_div


def reformat_class_toc(select_div, lobe_list):
    soup = BeautifulSoup("", 'html.parser')
    toc_soup = BeautifulSoup("", 'html.parser')
    namespace_list = []
    for lobe in lobe_list:
        detail = toc_soup.new_tag('details')
        toc_soup.append(detail)
        for div in select_div[lobe]:
            namspace = div.get('id').split("#")[0]
            namespace_list.append(namspace)
            if lobe == div.get('id').split("#")[-1]:
                # Create the dl tag with 'id' attribute
                main_div = soup.new_tag("div", title=lobe)
                dl_tag = soup.new_tag("dl", id=lobe)
                main_div.append(dl_tag)

                new_h3 = div.find('h3')
                span_to_remove = new_h3.find('span')
                sup_to_remove = new_h3.find('sup')
                if span_to_remove and sup_to_remove:
                    span_to_remove.decompose()
                    sup_to_remove.decompose()
                dl_tag.append(new_h3)

                # Nested dl tag
                nested_dl = soup.new_tag("dl")
                dl_tag.append(nested_dl)

                # IRI
                iri_tr_tag = soup.new_tag("tr")
                nested_dl.append(iri_tr_tag)
                dt_tag = soup.new_tag("dt")
                iri_tr_tag.append(dt_tag)
                dt_tag.string = "IRI"
                dd_tag = soup.new_tag("dd")
                iri_tr_tag.append(dd_tag)
                code_tag = soup.new_tag("code")
                code_tag.string = div.get('id')
                dd_tag.append(code_tag)
                # Superclass List
                superclass_tr_tag = soup.new_tag("tr")
                nested_dl.append(superclass_tr_tag)
                superclass_dt_tag = soup.new_tag("dt")
                superclass_dt_tag.string = "Super Class Of"
                superclass_tr_tag.append(superclass_dt_tag)
                dd_tag = soup.new_tag("dd")
                superclass_tr_tag.append(dd_tag)
                ul_tag = soup.new_tag("ul")
                dd_tag.append(ul_tag)

                for i in div.find('dd').find_all(['a']):
                    li_tag = soup.new_tag("li")
                    span_tag = soup.new_tag("span")
                    li_tag.append(span_tag)
                    old_href = i['href']
                    old_title = i['title']
                    i['href'] = '#' + old_href.split('#')[-1]
                    i['title'] = old_title
                    span_tag.append(i)
                    ul_tag.append(li_tag)
                # Description
                description_tr_tag = soup.new_tag("tr")
                nested_dl.append(description_tr_tag)
                description_dt_tag = soup.new_tag("dt")
                description_dt_tag.string = "Description"
                description_tr_tag.append(description_dt_tag)
                description_td_tag = soup.new_tag("td")
                description_p_tag = soup.new_tag("p")
                description_p_tag.string = div.find('span', class_='markdown').text
                description_td_tag.append(description_p_tag)
                description_tr_tag.append(description_td_tag)

                soup.append(main_div)

                # TOC
                summary = soup.new_tag('summary')
                lobe_string = copy.deepcopy(lobe)
                if 'Development' in lobe_string.replace('_Lobe', '').replace('_', ' '):
                    summary.string = 'Semiconductor Dev.'
                elif 'Semiconductor Production' in lobe_string.replace('_Lobe', '').replace('_', ' '):
                    summary.string = 'Semiconductor Prod.'
                else:
                    summary.string = lobe_string.replace('_Lobe', '').replace('_', ' ')
                detail.append(summary)
                ul = toc_soup.new_tag('ul', attrs={'class': 'third'})
                detail.append(ul)
                dd = toc_soup.new_tag('dd')
                ul.append(dd)
                li = toc_soup.new_tag('li')
                dd.append(li)
                new_a_tag = soup.new_tag('a')
                new_a_tag['href'] = f'#{lobe}'
                new_a_tag['onclick'] = "opentab(event, 1,2)"
                new_a_tag.string = lobe.replace('_', ' ')
                li.append(new_a_tag)
            else:
                class_div = soup.new_tag("div", attrs={"class": "property entity", "id": div.get('id').split("#")[-1]})
                new_h3 = div.find('h3')
                span_to_remove = new_h3.find('span')
                sup_to_remove = new_h3.find('sup')
                if span_to_remove and sup_to_remove:
                    span_to_remove.decompose()
                    sup_to_remove.decompose()
                class_div.append(new_h3)
                table = soup.new_tag("table")
                class_div.append(table)
                # IRI
                iri_tr_tag = soup.new_tag("tr")
                table.append(iri_tr_tag)
                th_tag = soup.new_tag("th")
                iri_tr_tag.append(th_tag)
                th_tag.string = "IRI"
                td_tag = soup.new_tag("td")
                iri_tr_tag.append(td_tag)
                code_tag = soup.new_tag("code")
                code_tag.string = div.get('id')
                td_tag.append(code_tag)
                # Description
                description_tr_tag = soup.new_tag("tr")
                table.append(description_tr_tag)
                description_th_tag = soup.new_tag("th")
                description_th_tag.string = "Description"
                description_tr_tag.append(description_th_tag)
                description_td_tag = soup.new_tag("td")
                description_p_tag = soup.new_tag("p")
                try:
                    description_p_tag.string = div.find('span', class_='markdown').text
                except:
                    pass
                description_td_tag.append(description_p_tag)
                description_tr_tag.append(description_td_tag)
                # Classes
                dt_all = div.find_all('dt')
                if dt_all:
                    op_list = []
                    dp_list = []
                    for dt in dt_all:
                        if dt.text != 'has super-classes':
                            if dt.text == 'is in range of' or dt.text == 'is in domain of':
                                dd_tag = dt.find_next_sibling('dd')
                                a_tags = dd_tag.find_all('a')
                                for a_tag in a_tags:
                                    old_title = a_tag['title']
                                    new_href = "#" + a_tag.get('href').split('#')[-1]
                                    sup_tag = a_tag.find_next_sibling('sup')
                                    if sup_tag:
                                        if sup_tag.text == 'op':
                                            new_a = soup.new_tag("a", onclick="opentab(event, 2,2)",
                                                                 href=new_href, title=old_title)
                                            new_a.string = a_tag.string
                                            op_list.append(new_a)
                                        elif sup_tag.text == 'dp':
                                            new_a = soup.new_tag("a", onclick="opentab(event, 3,2)",
                                                                 href=new_href, title=old_title)
                                            new_a.string = a_tag.string
                                            dp_list.append(new_a)

                            else:
                                class_p_tag = soup.new_tag('p')
                                class_div.append(class_p_tag)
                                class_p_tag.string = dt.text + ": "
                                dd_tag = dt.find_next_sibling('dd')
                                a_tags = dd_tag.find_all('a')
                                for idx, a_tag in enumerate(a_tags):
                                    try:
                                        old_title = a_tag['title']
                                    except:
                                        old_title = a_tag.get('href')
                                    new_href = "#" + a_tag.get('href').split('#')[-1]
                                    new_a = soup.new_tag("a", href=new_href, title=old_title)
                                    new_a.string = a_tag.string
                                    class_p_tag.append(new_a)
                                    if idx < len(a_tags) - 1:
                                        class_p_tag.append(", ")
                    if op_list:
                        class_p_tag = soup.new_tag('p')
                        class_div.append(class_p_tag)
                        class_p_tag.string = "has object properties: "
                        for idx, op_tag in enumerate(op_list):
                            class_p_tag.append(op_tag)
                            if idx < len(op_list) - 1:
                                class_p_tag.append(", ")
                    if dp_list:
                        class_p_tag = soup.new_tag('p')
                        class_div.append(class_p_tag)
                        class_p_tag.string = "has datatype properties: "
                        for idx, dp_tag in enumerate(dp_list):
                            class_p_tag.append(dp_tag)
                            if idx < len(dp_list) - 1:
                                class_p_tag.append(", ")

                lobe_p = soup.new_tag("p", align="right")
                class_div.append(lobe_p)
                lobe_a = soup.new_tag("a", href="#" + lobe)
                lobe_p.append(lobe_a)
                lobe_a.string = 'back to ' + lobe.replace('_', ' ')
                main_div.append(class_div)


                # toc
                li = toc_soup.new_tag("li")
                dd.append(li)
                new_a_tag = soup.new_tag("a")
                id = class_div.get('id')
                new_a_tag['href'] = f'#{id}'
                new_a_tag['onclick'] = "opentab(event, 1,2)"
                new_a_tag.string = new_h3.text
                li.append(new_a_tag)

    return soup, toc_soup, list(set(namespace_list))

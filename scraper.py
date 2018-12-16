import requests
from bs4 import BeautifulSoup
import json
import numpy as np

url1 = "http://bible.wikia.com/wiki/Category:Persons"
url2 = "http://bible.wikia.com/wiki/Category:Persons?from=Herod+Archelaus"
root = "http://bible.wikia.com"

oldurl1 = "http://bible.wikia.com/wiki/Category:Old_Testament_People"
oldurl2 = "http://bible.wikia.com/wiki/Category:Old_Testament_People?from=Jonathan+%28Son+of+Saul%29"
newurl = "http://bible.wikia.com/wiki/Category:New_Testament_People"

place_url = "http://bible.wikia.com/wiki/Category:Places"

insight_url = "http://bible.wikia.com/wiki/Special:Insights/popularpages?sort=pv28"


def get_all_person_links():
    # first pull the HTML from the Old Testament pages that links to all of the pages with the links.
    html1 = requests.get(oldurl1)
    html2 = requests.get(oldurl2)
    # next pull the HTML from the New Testament pages that links to all of the pages with the links.
    html3 = requests.get(newurl)
    # turn the HTML into a beautiful soup text object
    soup1 = BeautifulSoup(html1.text, 'lxml')
    soup2 = BeautifulSoup(html2.text, 'lxml')
    soup3 = BeautifulSoup(html3.text, 'lxml')

    old_links = []
    new_links = []
    all_links = []
    for link in soup1.find_all("a", class_="category-page__member-link"):
        old_links.append(link['href'])
        all_links.append(link['href'])
    for link in soup2.find_all("a", class_="category-page__member-link"):
        old_links.append(link['href'])
        all_links.append(link['href'])
    for link in soup3.find_all("a", class_="category-page__member-link"):
        new_links.append(link['href'])
        all_links.append(link['href'])

    print("all links count:")
    print(len(all_links))
    print("old links count:")
    print(len(old_links))
    print(old_links)
    print("new links count:")
    print(len(new_links))
    print(new_links)
    return old_links, new_links, all_links


def get_shorthand(person_links):
    shortlinks = []
    for link in person_links:
        idx = link.find('_')
        if idx != -1:
            shortlinks.append(link[0:idx])
        else:
            shortlinks.append(link)
    return shortlinks

def get_all_place_links():
    # first pull the HTML from the page that links to all of the pages with the links.
    html = requests.get(place_url)
    # turn the HTML into a beautiful soup text object
    soup = BeautifulSoup(html.text, 'lxml')

    links = []
    for link in soup.find_all("a", class_="category-page__member-link"):
        links.append(link['href'])

    print(links)
    print(len(links))
    return links


def get_html(link):
    html = requests.get(root + link)
    soup = BeautifulSoup(html.text, 'lxml')

    return soup


def get_connections(all_person_links, shorthand, soup):
    connection_indices = []
    connections = []
    for link in soup.find_all("a"):
        if link.has_attr('href') and not link.has_attr('data-tracking'):
            if link['href'][6:] not in connections:
                if link['href'] in all_person_links:
                    connection_indices.append(all_person_links.index(link['href']))
                    connections.append(link['href'][6:])
                elif link['href'] in shorthand:
                    connection_indices.append(shorthand.index(link['href']))
                    connections.append(link['href'][6:])
    return connections, connection_indices


def iterate_info_category(category):
    category_list = []
    if category is not None:
        #print(category.previous_element.previous_element.previous_element)

        category_html = category.previous_element.previous_element.previous_element
        div = category_html.find("div")
        #print(div)
        category_li = div.find_all("li")
        if category_li:
            for list_option in category_li:
                link = list_option.find("a")
                if link is not None:
                    category_list.append(link.text)
        else:
            category_list.append(div.text)
    print(category_list)
    return category_list


def extract_info_box(infobox):
    info_dict = {}
    image = infobox.find("a", class_="image image-thumbnail")
    if image is not None:
        info_dict["image_url"] = image['href']
    lifespan = infobox.find("b", text="Life-span")
    #if lifespan is not None:
    #    print(lifespan.next_element.next_element.next_element.text)
    #    info_dict["lifespan"] = lifespan.next_element.next_element.next_element.text
    parents = infobox.find("b", text="Parents")
    parents_list = iterate_info_category(parents)
    info_dict["parents"] = parents_list
    spouses = infobox.find("b", text="Spouse(s)")
    spouse_list = iterate_info_category(spouses)
    info_dict["spouse"] = spouse_list
    offspring = infobox.find("b", text="Offspring")
    offspring_list = iterate_info_category(offspring)
    info_dict["offspring"] = offspring_list

    return info_dict


def get_description(person_soup):
    info_dict = {"note": "There is not enough information on this person."}
    description = person_soup.find("meta", {"name": "description"})
    #print(description)
    if description is not None:
        info_dict["description"] = description['content']

    return info_dict


def get_person_info(person_soup):
    infobox = person_soup.find("aside", class_="portable-infobox pi-background pi-europa pi-theme-wikia pi-layout-default")
    if infobox is not None:
        person_info = extract_info_box(infobox)
    else:
        person_info = get_description(person_soup)

    print(person_info)
    return person_info


def data_to_json(personlinks, groupnum, filename):
    data = {
        "nodes":[],
        "edges":[]
    }
    index = 0
    short_all = get_shorthand(personlinks)
    for person in personlinks:
        personhtml = get_html(person)
        personconnections, connection_indices = get_connections(all_person_links, short_all, personhtml)
        #info = get_person_info(personhtml)
        #if "parents" in info.keys():
         #   data["nodes"].append({"id": index, "label": person[6:], "group": 1, "title": str(info["parents"])})
        #else:
        data["nodes"].append({"id": index, "label": person[6:], "group": groupnum, "info": get_person_info(personhtml)})
        for i in range(0, len(connection_indices)):
            data["edges"].append({"from": index, "to": connection_indices[i], "title": str(person[6:]) + " to " + str(personconnections[i])})
        index += 1
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def get_connection_rankings(personlinks):
    short_all = get_shorthand(personlinks)
    num_connections = []
    for person in personlinks:
        personhtml = get_html(person)
        personconnections, connection_indices = get_connections(all_person_links, short_all, personhtml)
        num_connections.append(len(personconnections))
    ranking_indices, topCounts = sort_rankings(num_connections)
    print(ranking_indices)
    rankings = []
    for i in ranking_indices:
        rankings.append(personlinks[i])
    print("counts")
    print(topCounts)
    print("connection rankings")
    print(rankings)

    return topCounts, rankings


def sort_rankings(num_connections):
    connectionscount = np.array(num_connections)
    ind = np.argpartition(connectionscount, -4)[-50:]
    print(ind)
    print(connectionscount[ind])
    sortedind = ind[np.argsort(connectionscount[ind])]
    print(sortedind)
    print(connectionscount[sortedind])
    return sortedind, connectionscount[sortedind]


def get_insight_rankings(personlinks):
    # first pull the HTML from the Old Testament pages that links to all of the pages with the links.
    html1 = requests.get(insight_url)
    # turn the HTML into a beautiful soup text object
    soup1 = BeautifulSoup(html1.text, 'lxml')

    views = []
    person_list = []
    for link in soup1.find_all("td"):
        entry = link.find("a", class_="insights-list-item-title ")
        if entry is not None:
            if entry['href'][22:] in personlinks:
                person_list.append(entry['href'][22:])
        else:
            views.append(int(link.text.strip()))
    print(views)
    print(person_list)
    return views, person_list

OT_person_links, NT_person_links, all_person_links = get_all_person_links()

counts, connect_ranks = get_connection_rankings(all_person_links)
views, insight_ranks = get_insight_rankings(all_person_links)
data_to_json(OT_person_links, 1, "OT_data.json")
data_to_json(NT_person_links, 2, "NT_data.json")




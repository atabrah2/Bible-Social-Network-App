import unittest
import scraper as scr


class ScraperParserTest(unittest.TestCase):
    def test_person_get_connections(self):
        person_links = scr.get_all_person_links()
        person_html = scr.get_html(person_links[0])

        person_connections = scr.get_connections(person_links, person_html)
        self.assertIn('/wiki/Moses', person_connections)
        self.assertIn('/wiki/Jesus_Christ', person_connections)
        self.assertNotIn('/wiki/Noah', person_connections)

    def test_place_get_connections(self):
        person_links = scr.get_all_person_links()
        place_links = scr.get_all_place_links()
        place_html = scr.get_html(place_links[6])

        place_connections = scr.get_connections(person_links, place_html)
        self.assertIn('/wiki/Shem', place_connections)
        self.assertIn('/wiki/Jesus_Christ', place_connections)
        self.assertNotIn('/wiki/Michael', place_connections)

    def test_iterate_info_category(self):
        person_links = scr.get_all_person_links()
        person_html = scr.get_html(person_links[6])

        infobox = person_html.find("aside", class_="portable-infobox pi-background pi-europa pi-theme-wikia pi-layout-default")
        parents = infobox.find("b", text="Parents")

        parents_list = scr.iterate_info_category(parents)
        self.assertNotIn("Moses", parents_list)
        self.assertIn("Adam", parents_list)
        self.assertIn("Eve", parents_list)

    def test_extract_info_box(self):
        person_links = scr.get_all_person_links()
        person_html = scr.get_html(person_links[0])

        infobox = person_html.find("aside",
                                   class_="portable-infobox pi-background pi-europa pi-theme-wikia pi-layout-default")
        info_dict = scr.extract_info_box(infobox)
        self.assertEqual(info_dict['image_url'], 'https://vignette.wikia.nocookie.net/biblestudy/images/a/a4/Aaron.jpg/revision/latest?cb=20160707133506')
        self.assertEqual(info_dict['parents'], ['Amram', 'Jochebed'])
        self.assertEqual(info_dict['spouse'],  ['Elisheba'])
        self.assertEqual(info_dict['offspring'],  ['Eleazar', 'Nadab', 'Ithamar', 'Abihu'])

    def test_get_description(self):
        person_links = scr.get_all_person_links()

        person_html = scr.get_html(person_links[1])
        info_dict = scr.get_description(person_html)

        self.assertEqual(info_dict['note'], "There is not enough information on this person.")
        self.assertEqual(info_dict['description'], "This article is about Ethan's grandfather. You may be looking for Kish's father or the Jew. Abdi (meaning: &quot;My Servant&quot;) was the grandfather of Ethan, the musician. Verses This article is a stub. You can help Bible Wiki by expanding it.")

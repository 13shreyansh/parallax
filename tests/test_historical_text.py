import unittest
from pipeline.text import historical_passage
class HistoricalText(unittest.TestCase):
    def test_numeric_change_shows_the_actual_older_sentence(self):
        text='The war began in 1939. The division contained 120 tanks. It withdrew in March.'
        result=historical_passage('The division contained 140 tanks.',text)
        self.assertEqual(result,'The division contained 120 tanks.')
    def test_a_substantive_new_sentence_is_not_mapped_to_generic_army_text(self):
        old='Puna-armeijalla oli puolellaan musertava kalusto- ja miesylivoima. Tukeuduttiin aukeille ja teihin.'
        claim='Puna-armeijan mekanisoitu kalusto oli osin soveltumatonta metsäsodankäyntiin, toimi vain aukeilla ja teillä eikä useinkaan kestänyt kovia pakkasia.'
        self.assertIsNone(historical_passage(claim,old))
    def test_wiki_markup_and_minor_rewording_are_matched(self):
        old='[[Finland]] had 114 combat aircraft fit for duty. They defended the capital.'
        self.assertEqual(historical_passage('Finland had 114 combat aircraft ready for duty.',old),'Finland had 114 combat aircraft fit for duty.')

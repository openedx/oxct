import unittest

from oxct.server import community


class CommunityTests(unittest.TestCase):
    def test_parse_hashtags(self):
        tags = community.parse_hashtags("#tag2 #tag1 some other text")
        self.assertEqual(["tag1", "tag2"], tags)

    def test_parse_duplicate_tags(self):
        tags = community.parse_hashtags("#tag1 #tag2 #tag1")
        self.assertEqual(["tag1", "tag2"], tags)

    def test_parse_hashtags_lowe_case(self):
        tags = community.parse_hashtags("#Tag1")
        self.assertEqual(["tag1"], tags)

import unittest
from hybrid.hybrid_retriever import hybrid_retrieve

class TestHybridRetrieval(unittest.TestCase):

    def test_named_query(self):
        query = "Andre Achtar-Zadeh"
        results = hybrid_retrieve(query)
        
        # Check keys exist
        self.assertIn("vector_results", results)
        self.assertIn("graph_results", results)

        # Check at least one result returned
        self.assertGreater(len(results["vector_results"]), 0)
        self.assertGreater(len(results["graph_results"]), 0)

    def test_empty_query(self):
        query = ""
        results = hybrid_retrieve(query)
        self.assertTrue("vector_results" in results or "graph_results" in results)

if __name__ == '__main__':
    unittest.main()

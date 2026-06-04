import os
import json
import subprocess

class GraphService:
    @staticmethod
    def query_knowledge(question):
        """
        Queries the Graphify knowledge graph for context related to a question.
        Returns a string of relevant context or an empty string.
        """
        graph_path = os.path.join(os.getcwd(), 'graphify-out', 'graph.json')
        
        if not os.path.exists(graph_path):
            print("Knowledge graph not found. Skipping graph retrieval.")
            return ""
            
        try:
            # Use the graphify CLI to query the local graph
            # graphify query "<question>" --budget 1000
            result = subprocess.run(
                ['graphify', 'query', question, '--budget', '1000'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error querying knowledge graph: {e}")
            return ""

    @staticmethod
    def get_drought_context():
        """
        Fetches general drought risk context from the graph.
        """
        return GraphService.query_knowledge("What are the key factors and indices for assessing drought risk?")

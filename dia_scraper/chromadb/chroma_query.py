from typing import Any, List
import chromadb
import json
import 

def query_data(name:str, query_date:str, data: dict, where=None, n_results: int =3) -> Any:

    # Create Simple ChromaDB to store and query text data
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name=name, 
                                                metadata={
                                                "created":query_date,
                                                })
    collection.add(
        ids=data.keys(), # unique ids
        documents=[
            "Russian submarine attack that sank a ship in the Black Sea. The ship was a cargo vessel. It was carrying grain. The submarine was a diesel-electric submarine of class Kilo.",
            "Cats and dogs are great pets. I love my cat. My cat is very playful and loves to chase laser pointers.",
            "A Chinese ship was spotted of the coast of Austrailia.",
            "Cats are curious creatures. They love to explore their surroundings and can often be found investigating new objects or areas in the home."
        ],
        metadatas=[
            {"source": "https://www.defense.gov/News/Releases/Release/Article/3532966/russian-submarine-attacks-ukrainian-ship-in-black-sea/",
             'date': '2025-09-28'},
            {"source": "https://en.wikipedia.org/wiki/Cat",
             'date': '2025-06-28'},
            {"source": "https://en.wikipedia.org/wiki/China_Australia_relations",
             'date': '2024-09-28'},
            {"source": "https://en.wikipedia.org/wiki/Cat",
             'date': '2025-07-30'}
        ])
    results = collection.query(
        query_texts=query_texts, # Chroma will embed this for you
        where=where, # metadata filter
        n_results=n_results, # how many results to return
        include=["metadatas", 'documents', 'distances', "data"] # what to return
    )
    return results

if __name__ == "__main__":
    # Example usage
    data = {'id1': ['url1'],}
    query_data("promare_search", "202509", data, where={"date": "2025-09-28"}, n_results=3)
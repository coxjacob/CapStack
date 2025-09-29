from typing import Any, List
import chromadb
import json

def query_data(name:str, query_date:str, data: dict, queries: list, where=None, n_results: int =3) -> Any:

    # Create Simple ChromaDB to store and query text data
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name=name, 
                                                metadata={
                                                "created":query_date,}
                                                )
    print (data.keys())
    collection.add(
        ids=list(data.keys()), # unique ids
        documents=[data[key_id][2] for key_id in data.keys()], # documents
        metadatas=[{"source": data[key_id][0],
                    'title': data[key_id][1],} for key_id in data.keys()] # metadatas
        )

    results = collection.query(
        query_texts= queries, # Chroma will embed this for you
        where=where, #{"date": "2025-09-28", }, # metadata filter
        n_results=n_results, # how many results to return
        include=["metadatas", 'documents', 'distances',] # what to return
        )   
    return results

if __name__ == "__main__":
    # Example usage
    text1 = "Russian submarine attack that sank a ship in the Black Sea. The ship was a cargo vessel. It was carrying grain. The submarine was a diesel-electric submarine of class Kilo."
    text2 = "Cats and dogs are great pets. I love my cat. My cat is very playful and loves to chase laser pointers."
    text3 = "A Chinese ship was spotted of the coast of Austrailia."
    text4 = "Cats are curious creatures. They love to explore their surroundings and can often be found investigating new objects or areas in the home."
    text5 = "The Russian submarine fleet has been very active in the Black Sea recently, with several patrols and exercises being conducted."
    
    data = {'id1': ['url1', 'title1', text1], 'id2': ['url2', 'title2', text2], 'id3': ['url3', 'title3', text3],
            'id4': ['url4', 'title4', text4], 'id5': ['url5', 'title5', text5],}
    search_topic = "Russian submarine"
    queries = [f"Does this article talk about {search_topic}?",]
    results = query_data("promare_search", "202509", data, queries, n_results=3)
    print(type(results))
    print(json.dumps(results, indent=4))


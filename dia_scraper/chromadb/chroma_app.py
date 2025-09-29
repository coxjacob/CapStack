import chromadb
import json

# Simple example of using ChromaDB to store and query text data
# https://docs.trychroma.com/docs/run-chroma/client-server
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="promare_search", 
                                             metadata={
                                                "created":"202509"
                                                })

# Using title_hash: [href, title, text] as documents, use title_hash as ids
# For result in search_results.keys(), use result[key]:text as documents
#  
collection.add(
    ids=["id1", "id2", "id3", "id4"], # unique ids
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
    query_texts=["Cat and Dogs as pets"
                 "What activity has been observed on Russian submarines?",
                 "Russian submarine attack that sank a ship in the Black Sea. The ship was a cargo vessel. It was carrying grain. The submarine was a diesel-electric submarine of class Kilo."], # Chroma will embed this for you
    where={"date": "2025-09-28", }, # metadata filter
    n_results=3, # how many results to return
    include=["metadatas", 'documents', 'distances', "data"] # what to return
)
print(type(results))
print(json.dumps(results, indent=4))

# Implement an imput method to ask multiple questions. 


# collection.get(
#     where={
#        "author": {"$in": ["Rowling", "Fitzgerald", "Herbert"]}
#     }
# )
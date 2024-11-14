from langchain.document_loaders import PyPDFLoader
import openai
import chromadb

# Initialize Chroma client and create collection
client = chromadb.Client()
collection = client.create_collection(name="pdf_embeddings_collection")

# Load PDF files
pdf_paths = ["/home/evanholo/Downloads/automation/Rubrics/Project1Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project2Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project3Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project4Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project5Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project6Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project7Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project8Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project9Rubric.pdf", "/home/evanholo/Downloads/automation/Rubrics/Project10Rubric.pdf", "/home/evanholo/Downloads/automation/General/General-Information.pdf", "/home/evanholo/Downloads/automation/General/.JUnitGradingpdf"]
documents = []

# Load all PDFs into a list of documents
for pdf_path in pdf_paths:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()  # Load returns a list of LangChain documents
    documents.extend(docs)

# Function to generate OpenAI embeddings
def generate_embeddings(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Generate embeddings for each document
embeddings = []
for doc in documents:
    embedding = generate_embeddings(doc.page_content)
    embeddings.append(embedding)

# Get the IDs and metadata (optional)
ids = [f"doc_{i}" for i in range(len(embeddings))]
metadatas = [{"source": doc.metadata.get("source")} for doc in documents]

# Add embeddings, IDs, and metadata to the collection
collection.add(embeddings=embeddings, ids=ids, metadatas=metadatas)






# Query the collection
query_vector = generate_embeddings("search query text")
results = collection.query(query_embeddings=[query_vector], n_results=3)

print("Search Results:", results)


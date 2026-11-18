from openai import OpenAI
client = OpenAI()

client.embeddings.create(
  model="text-embedding-3-small",
  input="Hello world",
  encoding_format="float",
  dimensions=3
)

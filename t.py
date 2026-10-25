from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

# 1. Define the exact shape of the data you want back using Pydantic
class IceCreamReview(BaseModel):
    flavor: str = Field(description="The flavor of the ice cream being reviewed")
    rating: int = Field(description="Rating score from 1 to 10")
    review_summary: str = Field(description="A short one-sentence summary of why it got that rating")

# 2. Initialize ChatOllama
model = ChatOllama(model="llama3.1", temperature=0)

# 3. Tell the model to use this structured output schema
structured_model = model.with_structured_output(IceCreamReview)

# 4. Invoke it with a normal sentence
result = structured_model.invoke("I recently tried a scoop of salted caramel swirl and it was absolute heaven, easily a 10 out of 10.")

# 5. The result is a clean Python object matching your schema!
print(type(result))          # <class '__main__.IceCreamReview'>
print(result.flavor)         # salted caramel swirl
print(result.rating)         # 10
print(result.review_summary) # Absolute heaven!
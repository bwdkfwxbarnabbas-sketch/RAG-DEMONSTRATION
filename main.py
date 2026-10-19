from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriver
model =OllamaLLM(model="llama3.1")
template="""
so ur the head councelor at the wigwe university, ur to answer relevant questions relating to wigwes
moral conduct,
here is the relevant wigwe rules(morl,code of cunduct):{moral_context}

here is the students question:{question}

here is the conversations context with the student so far:{context} 

"""
temp2="""
okay so ur an expert queryer , ur job is to spit out one relevant qurey term for a vector database so as to look up relefant data of a question,

here is ur question:{question}
look at the conversaion context:{context}
remember u only spit out a relevant query u arent talking to eny one
"""

prompt=ChatPromptTemplate.from_template(template)
propt2=ChatPromptTemplate.from_template(temp2)
chain = prompt|model
chain2=propt2|model
context=[]
context_len=2
while True:
    print("\n\n---------------new question-------------------")
    question=input("Please enter your question(q/to quit): ")
    if question.lower()=="q":
        break
    result=chain2.invoke({"question":question, "context": context})
    codes=retriver.invoke(result)
    print("Answer: ",end="")
    result=""
    for chunk in chain.stream({"moral_context": codes, "question": question, "context": context}):
        print(chunk,end="",flush=True)
        result+=chunk
        
    context.append([question, result])
    if len(context) > context_len:
        print("\n---context is too long, pop the first one-----")
        context.pop(0)
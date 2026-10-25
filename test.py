import asyncio
from client import main
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
template = """
You are a pro python coder.
Someone asks you to code something in python with minimal external libraries.
Their question: {question}

Here is the conversation history of past turns (including tool results and agent actions):
{context}

You handed the job to another coding agent and your job is to talk about what you coded if your assistant coded anything.
Current assistant's response and tool data to the coding task: {current_data}
"""
prompt = ChatPromptTemplate.from_template(template)
speaker_model = ChatOllama(model="llama3.1", temperature=0.7)
chain= prompt|speaker_model 
max_context_len=3
async def maint(prompt: str,past):
    response=""
    # One clean line to get your action context and tool execution!
    content, tool_result = await main(mcp_server_path="C:/Users/BILL/Desktop/aiagents/mcp_server.py",user_prompt=prompt)

    # Stream the speaker model response
    

    print("\nAI Response: ", end="")
    async for chunk in chain.astream({"question":prompt,"context":past,"current_data":[content,tool_result]}):
        print(chunk.content, end="", flush=True)
        response+=chunk.content
    return {
        "user_question": prompt,
        "planner_content": content,
        "tool_result": tool_result,
        "ai_response": response
    }
        

async def main_loop():
    context = []
    while True:
        print("\n\n------------next_question--------------")
        question = input("pitch what u want to build (or 'q' to quit): ")
        if question.strip().lower() in ["q", "quit"]:
            break
        else:    
            cont = await maint(prompt=question, past=context)
            context.append(cont)
            if len(context) > max_context_len:
                context.pop(0)

if __name__ == "__main__":
    # Run the entire interactive chat session inside a single persistent event loop
    asyncio.run(main_loop())
            
import asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient

class MCPPlug:
    def __init__(self, mcp_server_path: str, model_name: str = "llama3.1"):
        self.mcp_server_path = mcp_server_path
        self.model_name = model_name
        
        self.client = MultiServerMCPClient({
            "counselor_tools": {
                "transport": "stdio",
                "command": "python",
                "args": [self.mcp_server_path],
            }
        })
        self.tools = []
        self.model_with_tools = None

    async def initialize(self):
        print("[MCPPlug] Connecting to MCP server...")
        # Get tools directly as of langchain-mcp-adapters 0.1.0+
        self.tools = await self.client.get_tools()
        print(f"[MCPPlug] Loaded tools: {[t.name for t in self.tools]}")

        model = ChatOllama(model=self.model_name, temperature=0)
        self.model_with_tools = model.bind_tools(self.tools)

    async def get_action_context(self, user_prompt: str):
        """
        Non-streaming method. Invokes the model once to extract 
        either tool calls or raw text context for the next model.
        """
        print(f"\n[Planner] Processing prompt for actions: '{user_prompt}'")
        
        # 1. Use ainvoke instead of astream to get the whole response instantly
        response = await self.model_with_tools.ainvoke([("user", user_prompt)])
        
        # 2. Package the result for your second model / execution engine
        action_context = {
            "content": response.content,
            "tool_calls": response.tool_calls
        }
        
        return action_context

# --- HOW TO PLUG IT INTO YOUR MULTI-MODEL PIPELINE ---
async def main(user_prompt: str,mcp_server_path: str):
        plug = MCPPlug(mcp_server_path=mcp_server_path)
        await plug.initialize()
        # Get the raw action context without any streaming UI delay
        context = await plug.get_action_context(user_prompt)
        
        print("\n--- Handing this Context to the Executor / Next Model ---")
        print(f"Content: {context['content']}")
        print(f"Tool Calls Found: {context['tool_calls']}")
        
        tool_result = None
        # If the model requested a tool, execute it via LangChain tool mapping
        if context["tool_calls"]:
         tool_map = {t.name: t for t in plug.tools}
         for tool_call in context["tool_calls"]:
             tool_name = tool_call["name"]
             tool_args = tool_call["args"]
             if tool_name in tool_map:
                print(f"[Executor] Running tool '{tool_name}' with args: {tool_args}")
                tool_result = await tool_map[tool_name].ainvoke(tool_args)
             else:
                tool_result = f"Error: Tool '{tool_name}' not found."
        return context["content"], tool_result

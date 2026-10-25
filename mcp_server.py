from mcp.server.fastmcp import FastMCP
import os
import subprocess

# 1. Initialize the FastMCP server instance
mcp = FastMCP("PongGameServer")

# Workspace path where the AI is permitted to save and execute files
WORKSPACE_DIR = r"C:/Users/BILL/Desktop/aiagents"

@mcp.tool()
def save_code_file(filename: str, code_content: str) -> str:
    """USE THIS FIRST whenever the user asks to write, create, code, or make a Python script or game. 
    Saves the provided Python code content into a file.
    """
    if not filename.endswith(".py"):
        filename += ".py"
        
    file_path = os.path.join(WORKSPACE_DIR, filename)
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code_content)
        
    return f"Successfully saved code to {file_path}"

@mcp.tool()
def run_python_script(filename: str) -> str:
    """USE THIS ONLY AFTER a file has already been created. Runs an existing Python script 
    in the background (ideal for games and GUI apps) and returns status.
    """
    file_path = os.path.join(WORKSPACE_DIR, filename)
    
    if not os.path.exists(file_path):
        return f"Error: The file {filename} does not exist in {WORKSPACE_DIR}."
        
    try:
        # Use Popen to launch the game window independently without blocking
        subprocess.Popen(["python", file_path])
        return f"Started {filename} successfully! The game window should now be open."
    except Exception as e:
        return f"Failed to execute script: {str(e)}"

# 2. Start the server over stdio pipes
if __name__ == "__main__":
    mcp.run()
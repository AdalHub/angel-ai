"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server
mcp = FastMCP("User's Notes")
myNotesFile= os.path.join(os.path.dirname(__file__),"MY_NOTES.txt")

def ensureFile():
    if not os.path.exists(myNotesFile):
        with open(myNotesFile, "w") as f:
            f.write("")

# Add user's Notes
@mcp.tool()
def addNote(message: str) -> str:
    """
    Append a new note to the notes files
    
    args: 
        message (str): the note content to be added to our user's notes
    returns:
        str: confirmation of the note being saved
    """
    ensureFile()
    with open(myNotesFile, "a") as f:
        f.write(message + "\n")
    return "Note has ben saved successfully!"


@mcp.tool()
def readNotes() -> str:
    """
    Read the users current note file
    
    returns:
        str: contents of our note so far
    """
    ensureFile()
    with open(myNotesFile, "r") as f:
        #we read the content inside the notes files and remove white spaces
        content = f.read().strip()
    return content or "No note found!"

@mcp.resource("mynotes://local/latest")
def getLatestNote():
    """
    get the most recent note added
    
    returns:
        str: contents of the latest note
    """
    ensureFile()
    with open(myNotesFile, "r") as f:
        lines = f.readlines()
    #we return the last line added(aka the last note)
    return lines[-1] if lines else "No notes found"


@mcp.prompt()
def noteSummary()->str:
    """
    Read the users current note file, and create a summary out of it
    
    returns:
        str: summary of notes according to prompt. if the note does not exists a placeholder message will be returned
    """
    ensureFile()
    with open(myNotesFile, "r") as f:
        #we read the content inside the notes files and remove white spaces
        content = f.read().strip()
        if not content:
            return "No note found!"    
    return f"Summarize the major points on these notes, and don't leave anything important out. Notes: {content}"


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."
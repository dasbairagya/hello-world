"""
STEP 4: Agent with Tools & Actions
Now the agent can use external tools to perform tasks.
Tools extend agent capabilities beyond just conversation.

This step adds:
- A tool registry system
- Built-in tools: calculator, web search, file operations
- Tool calling mechanism
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ToolRegistry:
    """Manages available tools for the agent."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools."""
        # Calculator tool
        self.register_tool(
            name="calculator",
            description="Perform basic arithmetic operations",
            func=self.calculator,
            params={
                "operation": "add, subtract, multiply, divide",
                "a": "First number",
                "b": "Second number"
            }
        )
        
        # Get current time tool
        self.register_tool(
            name="get_current_time",
            description="Get the current date and time",
            func=self.get_current_time,
            params={}
        )
        
        # File reader tool
        self.register_tool(
            name="read_file",
            description="Read contents of a text file",
            func=self.read_file,
            params={
                "filepath": "Path to the file to read"
            }
        )
    
    def register_tool(self, name, description, func, params):
        """
        Register a new tool.
        
        Args:
            name: Tool name
            description: What the tool does
            func: The function to call
            params: Parameters the tool accepts
        """
        self.tools[name] = {
            "description": description,
            "func": func,
            "params": params
        }
        print(f"✓ Tool registered: {name}")
    
    def get_tools_for_api(self):
        """Get tools in OpenAI API format."""
        tools = []
        for name, tool_info in self.tools.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool_info["description"],
                    "parameters": {
                        "type": "object",
                        "properties": tool_info["params"]
                    }
                }
            })
        return tools
    
    def execute_tool(self, tool_name, **kwargs):
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Arguments for the tool
            
        Returns:
            Result of tool execution
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        try:
            func = self.tools[tool_name]["func"]
            result = func(**kwargs)
            return result
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    # Built-in tool implementations
    @staticmethod
    def calculator(operation, a, b):
        """Perform arithmetic operations."""
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
        }
        
        if operation not in operations:
            return f"Unknown operation: {operation}"
        
        result = operations[operation](float(a), float(b))
        return f"{a} {operation} {b} = {result}"
    
    @staticmethod
    def get_current_time():
        """Get current date and time."""
        from datetime import datetime
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    @staticmethod
    def read_file(filepath):
        """Read file contents."""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File '{filepath}' not found"


class ToolUsingAgent:
    """An agent that can use tools to perform tasks."""
    
    def __init__(self, name, model="gpt-3.5-turbo"):
        """
        Initialize the tool-using agent.
        
        Args:
            name: Agent name
            model: LLM model to use
        """
        self.name = name
        self.model = model
        self.conversation_history = []
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found!")
        
        self.client = OpenAI(api_key=api_key)
        
        # Initialize tool registry
        self.tool_registry = ToolRegistry()
        
        self.system_prompt = f"""You are {name}, an AI assistant with access to tools.
When you need to:
- Do calculations: use the calculator tool
- Check time: use the get_current_time tool
- Read files: use the read_file tool

Always inform the user what tool you're using and why."""
        
        print(f"✓ Tool-using agent '{self.name}' initialized!")
        print(f"✓ Available tools: {', '.join(self.tool_registry.tools.keys())}")
    
    def perceive(self, user_input):
        """Receive and store user input."""
        print(f"\n[PERCEIVE] User: {user_input}")
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        return user_input
    
    def think(self, user_input):
        """
        Use LLM to think and potentially decide to use tools.
        """
        print(f"[THINK] Processing with {self.model}...")
        
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history
            
            # Call LLM with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tool_registry.get_tools_for_api(),
                tool_choice="auto"
            )
            
            return response
            
        except Exception as e:
            print(f"[ERROR] LLM call failed: {e}")
            return None
    
    def use_tools(self, response):
        """
        Process tool calls from LLM response.
        
        Args:
            response: The LLM response object
        """
        tool_results = []
        
        # Check if LLM wants to call tools
        for call in response.choices[0].message.tool_calls or []:
            tool_name = call.function.name
            tool_args = json.loads(call.function.arguments)
            
            print(f"[TOOL] Using tool: {tool_name}")
            print(f"[TOOL] Arguments: {tool_args}")
            
            # Execute the tool
            result = self.tool_registry.execute_tool(tool_name, **tool_args)
            print(f"[TOOL] Result: {result}")
            
            tool_results.append({
                "tool_use_id": call.id,
                "tool_name": tool_name,
                "result": result
            })
        
        return tool_results
    
    def act(self, response, tool_results=None):
        """
        Generate final response for user.
        
        Args:
            response: The LLM response
            tool_results: Results from tool calls
        """
        # If tools were used, get final response from LLM
        if tool_results:
            # Add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.choices[0].message.content or ""
            })
            
            # Add tool results
            for result in tool_results:
                self.conversation_history.append({
                    "role": "user",
                    "content": f"Tool {result['tool_name']} result: {result['result']}"
                })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt}
                ] + self.conversation_history
            )
            
            final_text = final_response.choices[0].message.content
        else:
            final_text = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": final_text
            })
        
        print(f"[ACT] Agent: {final_text}")
        return final_text
    
    def run(self, user_input):
        """
        Complete agent cycle with tool usage.
        
        Args:
            user_input: User's input
        """
        print(f"\n{'='*60}")
        print(f"Agent '{self.name}' - With Tools")
        print(f"{'='*60}")
        
        # Step 1: Perceive
        self.perceive(user_input)
        
        # Step 2: Think (LLM decides if tools are needed)
        response = self.think(user_input)
        
        # Step 3: Use tools if LLM decides to
        tool_results = self.use_tools(response)
        
        # Step 4: Act (generate final response)
        final_response = self.act(response, tool_results if tool_results else None)
        
        return final_response


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    try:
        agent = ToolUsingAgent("ToolBot", model="gpt-3.5-turbo")
        
        print("\n" + "="*60)
        print("AGENT WITH TOOLS")
        print("="*60)
        
        # Test 1: Calculator
        agent.run("What is 25 * 4?")
        
        # Test 2: Time query
        agent.run("What's the current time?")
        
        # Test 3: Math word problem
        agent.run("If I have 100 apples and give away 30, how many do I have left?")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nSetup: pip install openai python-dotenv")
        print("Add OPENAI_API_KEY to .env file")

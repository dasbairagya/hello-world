"""
STEP 5: Complete Intelligent Agent
This is the final step combining everything:
- Basic structure (Perceive, Think, Act)
- Memory management
- LLM integration
- Tool usage
- Interactive conversation loop

This creates a fully-functional AI agent!
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class CompleteIntelligentAgent:
    """A complete, production-ready AI agent with all features."""
    
    def __init__(self, name, model="gpt-3.5-turbo", temperature=0.7, max_memory=20):
        """
        Initialize the complete intelligent agent.
        
        Args:
            name: Agent name
            model: LLM model
            temperature: Creativity level (0-1)
            max_memory: Max conversation turns to remember
        """
        self.name = name
        self.model = model
        self.temperature = temperature
        self.max_memory = max_memory
        self.conversation_history = []
        self.long_term_memory = {}
        self.tool_usage_count = 0
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found!")
        
        self.client = OpenAI(api_key=api_key)
        
        # Setup system prompt
        self.system_prompt = f"""You are {name}, an intelligent AI assistant.

Your characteristics:
- You are helpful, harmless, and honest
- You remember the conversation context
- You use tools when needed
- You explain your reasoning clearly
- You ask clarifying questions when needed

Tools available:
1. calculator: Perform math operations (add, subtract, multiply, divide)
2. get_time: Get current date and time
3. save_memory: Remember important information
4. recall_memory: Access remembered information

When using tools, inform the user what you're doing."""
        
        self.tools = self._setup_tools()
        
        print(f"✓ Complete Intelligent Agent '{self.name}' initialized!")
        print(f"  Model: {self.model}")
        print(f"  Temperature: {self.temperature}")
        print(f"  Memory capacity: {self.max_memory} turns")
        print(f"  Available tools: {', '.join(t['function']['name'] for t in self.tools)}")
    
    def _setup_tools(self):
        """Setup available tools for the agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Perform arithmetic operations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "description": "Operation: add, subtract, multiply, or divide"
                            },
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["operation", "a", "b"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_time",
                    "description": "Get current date and time",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_memory",
                    "description": "Save important information to long-term memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string", "description": "Memory key"},
                            "value": {"type": "string", "description": "Value to remember"}
                        },
                        "required": ["key", "value"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "recall_memory",
                    "description": "Recall information from long-term memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string", "description": "Memory key to recall"}
                        },
                        "required": ["key"]
                    }
                }
            }
        ]
    
    def _execute_tool(self, tool_name, tool_input):
        """Execute a tool and return result."""
        if tool_name == "calculator":
            operations = {
                "add": lambda a, b: a + b,
                "subtract": lambda a, b: a - b,
                "multiply": lambda a, b: a * b,
                "divide": lambda a, b: a / b if b != 0 else "Error: Division by zero"
            }
            op = tool_input.get("operation", "add")
            a = float(tool_input.get("a", 0))
            b = float(tool_input.get("b", 0))
            result = operations.get(op, lambda x, y: "Unknown operation")(a, b)
            return f"{a} {op} {b} = {result}"
        
        elif tool_name == "get_time":
            return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        elif tool_name == "save_memory":
            key = tool_input.get("key")
            value = tool_input.get("value")
            self.long_term_memory[key] = value
            return f"Saved to memory: {key} = {value}"
        
        elif tool_name == "recall_memory":
            key = tool_input.get("key")
            value = self.long_term_memory.get(key, "Not found in memory")
            return f"Memory recall: {key} = {value}"
        
        return "Tool not found"
    
    def perceive(self, user_input):
        """
        PERCEIVE: Receive and understand user input.
        """
        print(f"\n[PERCEIVE] User: {user_input}")
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Maintain memory limit
        if len(self.conversation_history) > self.max_memory * 2:
            self.conversation_history = self.conversation_history[-self.max_memory * 2:]
        
        return user_input
    
    def think(self):
        """
        THINK: Use LLM to process and decide on response/tools.
        """
        print(f"[THINK] Querying {self.model} LLM...")
        
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=self.temperature,
                max_tokens=1000
            )
            
            print(f"[THINK] LLM processed successfully")
            return response
            
        except Exception as e:
            print(f"[ERROR] LLM error: {e}")
            return None
    
    def use_tools(self, response):
        """
        Process and execute any tool calls from the LLM.
        """
        if not response or not response.choices[0].message.tool_calls:
            return None
        
        tool_results = []
        
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            
            print(f"[TOOL] Using: {tool_name} with args {tool_input}")
            
            # Execute the tool
            result = self._execute_tool(tool_name, tool_input)
            print(f"[TOOL] Result: {result}")
            
            self.tool_usage_count += 1
            tool_results.append({
                "tool_call_id": tool_call.id,
                "tool_name": tool_name,
                "result": result
            })
        
        return tool_results if tool_results else None
    
    def act(self, response, tool_results=None):
        """
        ACT: Generate and deliver final response to user.
        """
        # If tools were used, get final response from LLM
        if tool_results:
            # Add assistant's initial response
            self.conversation_history.append({
                "role": "assistant",
                "content": response.choices[0].message.content or ""
            })
            
            # Add tool results
            for result in tool_results:
                self.conversation_history.append({
                    "role": "user",
                    "content": f"Tool {result['tool_name']} returned: {result['result']}"
                })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt}
                ] + self.conversation_history,
                temperature=self.temperature,
                max_tokens=500
            )
            
            final_text = final_response.choices[0].message.content
        else:
            # No tools used, use LLM response directly
            final_text = response.choices[0].message.content if response else "I encountered an error processing your request."
            self.conversation_history.append({
                "role": "assistant",
                "content": final_text
            })
        
        print(f"[ACT] Agent: {final_text}")
        return final_text
    
    def run(self, user_input):
        """
        Complete agent cycle: PERCEIVE -> THINK -> (USE TOOLS) -> ACT
        """
        print(f"\n{'='*70}")
        print(f"Agent '{self.name}' - Complete Cycle")
        print(f"{'='*70}")
        
        # PERCEIVE
        self.perceive(user_input)
        
        # THINK
        response = self.think()
        if not response:
            return "I apologize, I encountered an error."
        
        # USE TOOLS (if needed)
        tool_results = self.use_tools(response)
        
        # ACT
        final_response = self.act(response, tool_results)
        
        return final_response
    
    def interactive_mode(self):
        """
        Start an interactive conversation loop.
        Type 'exit' to quit, 'history' to see conversation, 'memory' to see saved facts.
        """
        print(f"\n{'='*70}")
        print(f"Welcome to {self.name}!")
        print(f"Type 'exit' to quit | 'history' for conversation | 'memory' for saved facts")
        print(f"{'='*70}\n")
        
        while True:
            try:
                user_input = input(f"\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print(f"\n{self.name}: Goodbye! Thanks for chatting!")
                    break
                
                elif user_input.lower() == "history":
                    self._print_history()
                    continue
                
                elif user_input.lower() == "memory":
                    self._print_memory()
                    continue
                
                else:
                    response = self.run(user_input)
                    print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _print_history(self):
        """Print conversation history."""
        print(f"\n{'='*70}")
        print("CONVERSATION HISTORY")
        print(f"{'='*70}")
        for i, msg in enumerate(self.conversation_history, 1):
            role = msg['role'].upper()
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"{i}. {role}: {content}")
    
    def _print_memory(self):
        """Print long-term memory."""
        print(f"\n{'='*70}")
        print("LONG-TERM MEMORY")
        print(f"{'='*70}")
        if not self.long_term_memory:
            print("No memories stored yet.")
        else:
            for key, value in self.long_term_memory.items():
                print(f"  {key}: {value}")
        print(f"Tools used: {self.tool_usage_count} times")
    
    def get_stats(self):
        """Get agent statistics."""
        return {
            "name": self.name,
            "model": self.model,
            "conversation_turns": len(self.conversation_history),
            "long_term_memories": len(self.long_term_memory),
            "tools_used": self.tool_usage_count
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    try:
        # Create the complete agent
        agent = CompleteIntelligentAgent(
            name="IntelliBot",
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_memory=20
        )
        
        print("\n" + "="*70)
        print("COMPLETE INTELLIGENT AGENT DEMO")
        print("="*70)
        
        # Demo 1: Simple conversation
        print("\n--- Demo 1: Simple Conversation ---")
        agent.run("Hello! My name is Alice and I work in Data Science.")
        
        # Demo 2: Save memory
        print("\n--- Demo 2: Save Information to Memory ---")
        agent.run("Please remember that my favorite programming language is Python")
        
        # Demo 3: Use tool
        print("\n--- Demo 3: Math Calculation ---")
        agent.run("What is 456 multiplied by 789?")
        
        # Demo 4: Recall memory
        print("\n--- Demo 4: Recall Memory ---")
        agent.run("What did you remember about me earlier?")
        
        # Demo 5: Complex query
        print("\n--- Demo 5: Complex Query ---")
        agent.run("Calculate 100 + 50, multiply by 2, and tell me the current time")
        
        # Display agent statistics
        print("\n" + "="*70)
        print("AGENT STATISTICS")
        print("="*70)
        stats = agent.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Uncomment line below to start interactive mode
        # agent.interactive_mode()
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nSetup Instructions:")
        print("1. Install: pip install openai python-dotenv")
        print("2. Get API key: https://platform.openai.com/api-keys")
        print("3. Create .env file with: OPENAI_API_KEY=your_key_here")

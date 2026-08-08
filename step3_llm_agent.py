"""
STEP 3: Connect Agent to an LLM (Large Language Model)
This step integrates the agent with OpenAI's GPT API.
The agent now uses a real language model for intelligent responses.

Requirements:
    pip install openai python-dotenv

Setup:
    1. Get API key from https://platform.openai.com/api-keys
    2. Create a .env file with: OPENAI_API_KEY=your_key_here
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class LLMAgent:
    """An agent powered by a Large Language Model (LLM)."""
    
    def __init__(self, name, model="gpt-3.5-turbo", temperature=0.7):
        """
        Initialize the agent with LLM capability.
        
        Args:
            name: The name of the agent
            model: The LLM model to use (gpt-3.5-turbo, gpt-4, etc.)
            temperature: Controls creativity (0=deterministic, 1=creative)
        """
        self.name = name
        self.model = model
        self.temperature = temperature
        self.conversation_history = []
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables!")
        
        self.client = OpenAI(api_key=api_key)
        
        # System prompt - defines agent behavior
        self.system_prompt = f"""You are {name}, a helpful and intelligent AI assistant.
You are designed to:
- Answer questions accurately
- Remember context from the conversation
- Be friendly and professional
- Provide clear explanations"""
        
        print(f"✓ Agent '{self.name}' initialized with {self.model} LLM!")
        print(f"✓ Temperature: {self.temperature} (0=precise, 1=creative)")
    
    def perceive(self, user_input):
        """
        Step 1: PERCEIVE - Receive input from user.
        
        Args:
            user_input: What the user says/asks
        """
        print(f"\n[PERCEIVE] User: {user_input}")
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        return user_input
    
    def think(self, user_input):
        """
        Step 2: THINK - Use LLM to generate intelligent response.
        
        Args:
            user_input: The perceived input
            
        Returns:
            The LLM's response
        """
        print(f"[THINK] Querying {self.model} LLM...")
        
        try:
            # Prepare messages for API
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=500
            )
            
            # Extract response text
            llm_response = response.choices[0].message.content
            
            # Print token usage
            print(f"[THINK] Tokens used - Input: {response.usage.prompt_tokens}, Output: {response.usage.completion_tokens}")
            
            return llm_response
            
        except Exception as e:
            print(f"[ERROR] LLM API call failed: {e}")
            return "I apologize, but I encountered an error processing your request."
    
    def act(self, response):
        """
        Step 3: ACT - Output the response and store in history.
        
        Args:
            response: The LLM's response
        """
        print(f"[ACT] Agent: {response}")
        
        # Store assistant response in history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def run(self, user_input):
        """
        Complete agent cycle: Perceive -> Think (via LLM) -> Act
        
        Args:
            user_input: Input from the user
        """
        print(f"\n{'='*60}")
        print(f"Agent '{self.name}' Processing Request")
        print(f"{'='*60}")
        
        # Step 1: Perceive
        perceived_input = self.perceive(user_input)
        
        # Step 2: Think (using LLM)
        response = self.think(perceived_input)
        
        # Step 3: Act
        final_output = self.act(response)
        
        return final_output
    
    def get_conversation_history(self):
        """Get the entire conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history (start fresh)."""
        self.conversation_history = []
        print("✓ Conversation history cleared!")
    
    def set_system_prompt(self, new_prompt):
        """
        Change the system prompt to modify agent behavior.
        
        Args:
            new_prompt: The new system prompt
        """
        self.system_prompt = new_prompt
        print(f"✓ System prompt updated!")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create an LLM-powered agent
    try:
        agent = LLMAgent(
            name="IntelligentBot",
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Multi-turn conversation
        print("\n" + "="*60)
        print("MULTI-TURN CONVERSATION WITH LLM")
        print("="*60)
        
        # Turn 1
        agent.run("What is artificial intelligence?")
        
        # Turn 2 - Agent remembers context
        agent.run("Can you give me a simple example?")
        
        # Turn 3
        agent.run("How do large language models work?")
        
        # Display conversation history
        print("\n" + "="*60)
        print("CONVERSATION HISTORY")
        print("="*60)
        for i, msg in enumerate(agent.get_conversation_history(), 1):
            print(f"\n{i}. {msg['role'].upper()}:")
            print(f"   {msg['content'][:100]}...")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nSetup Instructions:")
        print("1. Install: pip install openai python-dotenv")
        print("2. Get API key: https://platform.openai.com/api-keys")
        print("3. Create .env file with: OPENAI_API_KEY=your_key_here")

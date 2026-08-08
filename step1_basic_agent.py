"""
STEP 1: Basic Agent Structure
This is the foundation of any AI agent.
An agent is a program that:
1. Perceives its environment (input)
2. Processes information (reasoning)
3. Takes action (output)
"""

class SimpleAgent:
    """A very basic agent that responds to user input."""
    
    def __init__(self, name):
        """
        Initialize the agent.
        
        Args:
            name: The name of the agent
        """
        self.name = name
        self.is_active = True
        self.conversation_history = []
        print(f"Agent '{self.name}' initialized!")
    
    def perceive(self, user_input):
        """
        Step 1: PERCEIVE - Receive input from the user
        
        Args:
            user_input: What the user says/asks
        """
        print(f"\n[PERCEIVE] User input: '{user_input}'")
        self.conversation_history.append({"role": "user", "content": user_input})
        return user_input
    
    def think(self, user_input):
        """
        Step 2: THINK - Process the input and decide what to do
        
        Args:
            user_input: The perceived input
            
        Returns:
            A response based on the input
        """
        print(f"[THINK] Processing input...")
        
        # Simple logic: Just echo back
        response = f"You said: {user_input}"
        return response
    
    def act(self, response):
        """
        Step 3: ACT - Take action (output the response)
        
        Args:
            response: The response to give to the user
        """
        print(f"[ACT] Agent response: '{response}'")
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def run(self, user_input):
        """
        Complete agent cycle: Perceive -> Think -> Act
        
        Args:
            user_input: Input from the user
        """
        print(f"\n{'='*50}")
        print(f"Agent '{self.name}' Processing Request")
        print(f"{'='*50}")
        
        # Step 1: Perceive
        perceived_input = self.perceive(user_input)
        
        # Step 2: Think
        response = self.think(perceived_input)
        
        # Step 3: Act
        final_output = self.act(response)
        
        return final_output
    
    def get_conversation_history(self):
        """Get the conversation history."""
        return self.conversation_history


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create an agent
    agent = SimpleAgent("BasicBot")
    
    # Test the agent with different inputs
    agent.run("Hello!")
    agent.run("What is your name?")
    agent.run("Tell me a joke")
    
    # Display conversation history
    print("\n" + "="*50)
    print("CONVERSATION HISTORY")
    print("="*50)
    for msg in agent.get_conversation_history():
        print(f"{msg['role'].upper()}: {msg['content']}")

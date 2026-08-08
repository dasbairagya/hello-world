"""
STEP 2: Agent with Memory Management
An agent needs to remember past interactions to be smarter.
This step adds memory to store conversation history and context.
"""

class MemoryAgent:
    """An agent with memory capabilities."""
    
    def __init__(self, name, max_memory_size=10):
        """
        Initialize the agent with memory.
        
        Args:
            name: The name of the agent
            max_memory_size: Maximum number of messages to remember
        """
        self.name = name
        self.max_memory_size = max_memory_size
        self.short_term_memory = []  # Recent conversation history
        self.long_term_memory = {}   # Important facts/knowledge
        print(f"Agent '{self.name}' initialized with memory!")
    
    def store_short_term_memory(self, role, content):
        """
        Store conversation in short-term memory.
        
        Args:
            role: "user" or "assistant"
            content: The message content
        """
        self.short_term_memory.append({
            "role": role,
            "content": content
        })
        
        # Keep only recent messages
        if len(self.short_term_memory) > self.max_memory_size:
            self.short_term_memory.pop(0)
        
        print(f"[MEMORY] Stored: {role}: {content[:50]}...")
    
    def store_long_term_memory(self, key, value):
        """
        Store important facts in long-term memory.
        
        Args:
            key: The key for this fact
            value: The fact to remember
        """
        self.long_term_memory[key] = value
        print(f"[MEMORY] Stored fact: {key} = {value}")
    
    def recall_short_term_memory(self):
        """Recall recent conversation history."""
        return self.short_term_memory
    
    def recall_long_term_memory(self, key=None):
        """
        Recall a specific fact or all facts.
        
        Args:
            key: Optional specific key to recall
        """
        if key:
            return self.long_term_memory.get(key, None)
        return self.long_term_memory
    
    def get_context(self):
        """Get context from memory for current decision."""
        context = {
            "recent_conversation": self.short_term_memory[-3:],  # Last 3 messages
            "known_facts": self.long_term_memory
        }
        return context
    
    def perceive(self, user_input):
        """Perceive and store in memory."""
        print(f"\n[PERCEIVE] User: {user_input}")
        self.store_short_term_memory("user", user_input)
        return user_input
    
    def think(self, user_input):
        """Think using memory context."""
        print(f"[THINK] Accessing memory...")
        context = self.get_context()
        
        # Check if we know something relevant from long-term memory
        if "user_name" in self.long_term_memory:
            response = f"Hello {self.long_term_memory['user_name']}, you said: {user_input}"
        else:
            response = f"You said: {user_input}"
        
        return response
    
    def act(self, response):
        """Act and store response in memory."""
        print(f"[ACT] Agent: {response}")
        self.store_short_term_memory("assistant", response)
        return response
    
    def run(self, user_input):
        """Run the agent with memory cycle."""
        perceived = self.perceive(user_input)
        response = self.think(perceived)
        final = self.act(response)
        return final


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create an agent with memory
    agent = MemoryAgent("MemoryBot", max_memory_size=5)
    
    # Conversation 1
    print("\n" + "="*60)
    print("CONVERSATION WITH MEMORY")
    print("="*60)
    
    agent.run("Hi, my name is Alice")
    agent.store_long_term_memory("user_name", "Alice")
    
    agent.run("What's your purpose?")
    agent.run("Can you remember me?")
    
    # Display memory status
    print("\n" + "="*60)
    print("AGENT MEMORY STATUS")
    print("="*60)
    print("\nShort-term Memory (Recent Conversation):")
    for msg in agent.recall_short_term_memory():
        print(f"  {msg['role'].upper()}: {msg['content']}")
    
    print("\nLong-term Memory (Known Facts):")
    for key, value in agent.recall_long_term_memory().items():
        print(f"  {key}: {value}")

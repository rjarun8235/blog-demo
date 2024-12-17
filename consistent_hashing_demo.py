class SimpleConsistentHash:
    def __init__(self, nodes=None):
        """Initialize the hash ring with an optional list of nodes."""
        self.nodes = set()  # Physical nodes
        self.hash_ring = {}  # Hash positions mapped to nodes
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key: str) -> int:
        """Simple hash function for demonstration."""
        # Use Python's built-in hash function modulo 1000 for clarity
        return hash(key) % 1000
    
    def add_node(self, node: str) -> None:
        """Add a node and its virtual nodes to the hash ring."""
        print(f"\nAdding node '{node}'...")
        for i in range(3):  # 3 virtual nodes
            hash_key = self._hash(f"{node}:{i}")  # Hash virtual node
            self.hash_ring[hash_key] = node
            print(f"Virtual node: {node}:{i} -> Hash: {hash_key}")
        self.nodes.add(node)
        print("Hash ring updated.\n")
        
    def remove_node(self, node: str) -> None:
        """Remove a node and its virtual nodes from the hash ring."""
        print(f"\nRemoving node '{node}'...")
        for i in range(3):
            hash_key = self._hash(f"{node}:{i}")
            self.hash_ring.pop(hash_key, None)
            print(f"Removed virtual node: {node}:{i} -> Hash: {hash_key}")
        self.nodes.remove(node)
        print("Hash ring updated.\n")
    
    def get_node(self, key: str) -> str:
        """Get the node responsible for a given key."""
        if not self.hash_ring:
            return None
        
        hash_key = self._hash(key)
        sorted_positions = sorted(self.hash_ring.keys())
        
        # Find the first node clockwise (greater hash value)
        for pos in sorted_positions:
            if hash_key <= pos:
                return self.hash_ring[pos]
        
        # Wrap around: return the first node if hash_key > all positions
        return self.hash_ring[sorted_positions[0]]

# Example usage
if __name__ == "__main__":
    print("Initializing Consistent Hash Ring with nodes: node1, node2\n")
    ch = SimpleConsistentHash(["node1", "node2"])
    
    # Test key distribution
    print("Initial distribution:")
    for key in ["key1", "key2", "key3", "key4"]:
        print(f"{key} (hash: {hash(key) % 1000}) -> {ch.get_node(key)}")
        
    # Add a new node
    print("\nAfter adding 'node3':")
    ch.add_node("node3")
    for key in ["key1", "key2", "key3", "key4"]:
        print(f"{key} (hash: {hash(key) % 1000}) -> {ch.get_node(key)}")

    # Remove a node
    print("\nAfter removing 'node2':")
    ch.remove_node("node2")
    for key in ["key1", "key2", "key3", "key4"]:
        print(f"{key} (hash: {hash(key) % 1000}) -> {ch.get_node(key)}")
        
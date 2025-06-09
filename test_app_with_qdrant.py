"""
Test the knowledge base with Qdrant cloud
"""
from app.knowledge_base import KnowledgeBase
import sys

# Initialize the knowledge base
kb = KnowledgeBase()

try:
    # Test processing a simple webpage
    print("Testing website processing...")
    result = kb.process_website(
        url="https://en.wikipedia.org/wiki/Artificial_intelligence",
        depth=1,  # Just process the main page
        parse_js=False
    )
    
    print(f"Website processing complete:")
    print(f"  - Pages processed: {result['pages_processed']}")
    print(f"  - Chunks created: {result['chunks_created']}")
    print(f"  - Vectors stored: {result['vectors_stored']}")
    
    # Test searching the processed content
    if result['vectors_stored'] > 0:
        print("\nTesting search functionality...")
        search_results = kb.search(
            query="What is artificial intelligence?",
            limit=2
        )
        
        print(f"Search results: {len(search_results)} found")
        for i, result in enumerate(search_results):
            print(f"\nResult {i+1} (score: {result['score']:.4f}):")
            print(f"Text: {result['text'][:200]}...")
            print(f"URL: {result['url']}")
        
        # Test deleting the processed content
        print("\nTesting deletion functionality...")
        deletion = kb.delete_website("https://en.wikipedia.org/wiki/Artificial_intelligence")
        print(f"Deleted {deletion['deleted_vectors']} vectors")
    
    print("\n✅ All tests completed successfully!")
    
except Exception as e:
    print(f"❌ Error during testing: {str(e)}")
    sys.exit(1)
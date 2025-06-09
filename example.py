"""
Example script demonstrating the end-to-end knowledge base workflow.
"""
import argparse
import sys
from app.knowledge_base import KnowledgeBase

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base Demo")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Process website command
    process_parser = subparsers.add_parser("process", help="Process a website into the knowledge base")
    process_parser.add_argument("url", help="Website URL to process")
    process_parser.add_argument("--depth", type=int, default=1, help="Crawling depth")
    process_parser.add_argument("--parse-js", action="store_true", help="Parse JavaScript")
    process_parser.add_argument("--chunking", choices=["paragraph", "sentence", "token"], 
                               help="Chunking strategy")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Max results")
    search_parser.add_argument("--url-filter", help="Filter by URL")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete website data")
    delete_parser.add_argument("url", help="Website URL to delete")
    
    args = parser.parse_args()
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    if args.command == "process":
        print(f"Processing website: {args.url}")
        result = kb.process_website(
            url=args.url,
            depth=args.depth,
            parse_js=args.parse_js,
            chunking_strategy=args.chunking
        )
        print("Processing complete:")
        print(f"  Pages processed: {result['pages_processed']}")
        print(f"  Chunks created: {result['chunks_created']}")
        print(f"  Vectors stored: {result['vectors_stored']}")
        
    elif args.command == "search":
        print(f"Searching for: {args.query}")
        results = kb.search(
            query=args.query,
            limit=args.limit,
            url_filter=args.url_filter
        )
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (Score: {result['score']:.4f}):")
            print(f"URL: {result['url']}")
            print(f"Text: {result['text'][:200]}...")
            
    elif args.command == "delete":
        print(f"Deleting website data: {args.url}")
        result = kb.delete_website(args.url)
        print(f"Deleted {result['deleted_vectors']} vectors")
        
    else:
        parser.print_help()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
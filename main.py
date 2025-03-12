from core.api_client import XNETAPIClient
from core.llm import get_llm_client
from core.rag_engine import RagEngine
from core.state_machine import XNETStateMachine
from data.store import DocumentStore
from interfaces.terminal import run_terminal_interface
from utils.logger import logger

def main():
    logger.info("Initializing XNET Converse...")
    
    # Setup LLM
    llm = get_llm_client()
    
    # Setup document store and RAG
    store = DocumentStore()
    store.load_documents()
    rag = RagEngine(llm, store)
    
    # Setup API client and state machine
    api_client = XNETAPIClient()
    state_machine = XNETStateMachine(api_client, rag)
    
    # Run terminal interface
    run_terminal_interface(state_machine)

if __name__ == "__main__":
    main()

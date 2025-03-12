# xnetquery
conversational interface for querying the [XNET](https://xnet.company) api

## overview
This is a simple python framework for querying the [XNET API](https://docs.xnet.company/tech/api/documentation/) using an LLM-powered conversational interface.  
The interface implements a RAG (retrieval augmented generation) feature with the goal of being able to answer
basic questions about the XNET API and the XNET project based on a cache of indexed documents. 

## goals
The intial goal is to assist the XNET team with API testing. The ultimate goal is to turn this framework into
a set of bots for Telegram, Discord, and X that will provide useful answers to questions about the project and
will allow XNET Operators to retrieve information about the state of their deployments

## dependencies
The current implementation is an early prototype. It requires a local installation of [ollama](https://ollama.com/), Python 3.11, and the packages specified in [requrements.txt](./requirements.txt)  You will also need to set up a `.env` file with appropriate configuration information.  It should look like the following:
  ``` bash
API_BASE_URL=https://services.api-platform.staging.xnetcore.net
LLM_PROVIDER=ollama
#LLM_MODEL=mistral-7b-instruct
LLM_MODEL=mistral
LLM_LOCAL_ENDPOINT=http://localhost:11434
TERMINAL_TIMEOUT=3600
REFRESH_WINDOW=300  # 5 minutes
```


from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict

memory_store = {} # store session conversation memory

def get_memory(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferMemory(
            return_messages=True, memory_key="chat_history"
        )
    return memory_store[session_id]

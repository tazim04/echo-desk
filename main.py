from contextlib import asynccontextmanager
from app.db import engine
from app.models import Base, Appointment
from app.agent.tools import create_appointment
from fastapi import FastAPI, Request
from app.agent.agent import get_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    Base.metadata.create_all(bind=engine) # init db
    yield
    # shut down

app = FastAPI(lifespan=lifespan)

@app.post("/test")
async def test():
    result = create_appointment.invoke({
        "patient_name": "Test User",
        "patient_phone_number": "613-111-1111",
        "appointment_time": "2024-05-24T09:10:00",
        "reason": "Test run"
    })
    print(result)
    return {"result": result}


@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        session_id = body.get("session_id")
        message = body.get("message")

        print(f"\n=== DEBUG INFO ===")
        print(f"Received message: {message}")
        print(f"Session ID: {session_id}")

        agent = get_agent(session_id)
        print(f"Agent created successfully: {type(agent)}")
        
        # Check memory state
        from app.agent.memory import memory_store
        if session_id in memory_store:
            memory = memory_store[session_id]
            chat_history = memory.chat_memory.messages
            print(f"Chat history length: {len(chat_history)}")
            for i, msg in enumerate(chat_history):
                print(f"  Message {i}: {type(msg).__name__} - {msg.content[:100]}...")
        else:
            print("No existing memory for this session")
        
        print("Attempting to invoke agent...")
        result = agent.invoke({"input": message})
        print(f"Agent invoke result type: {type(result)}")
        print(f"Agent invoke result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        response = result.get("output", result.get("response", ""))

        print(f"Final response: '{response}'")
        print(f"Response length: {len(str(response))}")
        print("=== END DEBUG ===\n")
        
        # Ensure we return a non-empty response
        if not response or str(response).strip() == "":
            response = "I apologize, but I didn't generate a response. Could you please try again?"
            
        return {"response": str(response)}

    except Exception as e:
        import traceback
        print("Exception occurred in /chat endpoint:")
        traceback.print_exc()
        return {"response": f"Internal server error: {str(e)}"}
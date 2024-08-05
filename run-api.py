from fastapi import FastAPI, Request, status, Query
from fastapi.responses import JSONResponse
from pydantic.types import Json

import ollama

app = FastAPI()

# Whitelisted IPs, add here to limit the domains/IPs that have access to the API
WHITELISTED_IPS = []

# Model name
model_name = 'llama3'
#model_name = 'bramvanroy/geitje-7b-ultra:Q3_K_M'

# Load model in memory
ollama.generate(model=model_name, keep_alive='15m', prompt='Tell me a short joke')

@app.middleware('http')
async def validate_ip(request: Request, call_next):
  # Get client IP
  ip = str(request.client.host)

  # Check if IP is allowed
  if len(WHITELISTED_IPS) > 0 and ip not in WHITELISTED_IPS:
    data = {
      'message': f'{ip} is not allowed to access this resource.'
    }
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

  # Proceed if IP is allowed
  return await call_next(request)

@app.get("/get-response")
async def get_response(q: Json = Query()):
  print(q)
  response = ollama.chat(model=model_name, keep_alive='15m', messages = q['messages']) 
  return {"response": response['message']['content']}

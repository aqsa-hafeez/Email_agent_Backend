# # import sys
# # import os
# # from fastapi import FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from app.routes.gmail_routes import router 
# # import uvicorn
# # import time

# # # Path configuration
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # sys.path.insert(0, current_dir)

# # app = FastAPI(title="AI Email Assistant")

# # # --- Optimized CORS Settings ---
# # # Humne allow_origins ko specific bhi rakha hai aur "*" bhi handle kiya hai
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# #     expose_headers=["*"]
# # )

# # # --- Debugging Middleware (Zaroori) ---
# # # Ye terminal mein har request ka rasta bataye ga
# # @app.middleware("http")
# # async def log_requests(request: Request, call_next):
# #     start_time = time.time()
# #     response = await call_next(request)
# #     process_time = (time.time() - start_time) * 1000
# #     print(f"Method: {request.method} | Path: {request.url.path} | Time: {process_time:.2f}ms")
# #     return response

# # app.include_router(router, prefix="/api")

# # @app.get("/")
# # def home():
# #     return {"message": "Email Agent is Online", "status": "active"}

# # if __name__ == "__main__":
# #     # Host ko "0.0.0.0" hi rehne den taake external access mil sakay
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






# import sys
# import os
# import logging
# import time
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes.gmail_routes import router 
# import uvicorn

# # --- Central Logging Configuration ---
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler(sys.stdout)]
# )
# logger = logging.getLogger("main")

# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)

# app = FastAPI(title="AI Email Assistant")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = (time.time() - start_time) * 1000
#     # Detailed API Request Logging
#     logger.info(f"Incoming Request | Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | Duration: {process_time:.2f}ms")
#     return response

# app.include_router(router, prefix="/api")

# @app.get("/")
# def home():
#     return {"message": "Email Agent is Online", "status": "active"}

# if __name__ == "__main__":
#     logger.info("Starting AI Email Agent Server on port 8000...")
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)





















import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.gmail_routes import router
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
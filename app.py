
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from service import get_stock_analysis
from pydantic import BaseModel
from service import get_current_stock_details

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StockRequest(BaseModel):
    stock_name: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/stock-analysis")
def read_stock_analysis(req : StockRequest):
    stock_name = req.stock_name
    return JSONResponse(get_stock_analysis(stock_name))

@app.post("/stock")
def read_stock(req : StockRequest):
    stock_name = req.stock_name
    return JSONResponse(get_current_stock_details(stock_name))

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect_number(n: int) -> bool:
    if n <= 0:  # 0 and negative numbers are NOT perfect
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n: int) -> bool:
    digits = [int(digit) for digit in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def get_number_properties(n: int):
    properties = []
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    if is_prime(n):
        properties.append("prime")
    if is_perfect_number(n):
        properties.append("perfect")
    if is_armstrong(n):
        properties.append("armstrong")
    return properties

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="Number to classify")):
    try:
        n = float(number) if "." in number else int(number)  # Support integers and floats
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "number": number,  # Include the invalid input in the response
                "error": "Invalid input. Must be a valid number."
            }
        )

    properties = get_number_properties(int(n))  # Convert to int for property checks
    fun_fact_response = requests.get(f"http://numbersapi.com/{n}")
    fun_fact = fun_fact_response.text if fun_fact_response.status_code == 
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import math

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 1:
        return False
    return sum(i for i in range(1, n)) == n

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="Enter a valid number")):
    # Ensure number is a valid numeric value
    if not number.lstrip('-').replace('.', '', 1).isdigit():
        raise HTTPException(
            status_code=400,
            detail={"number": number, "error": "Invalid input. Must be a number."}
        )

    n = float(number)
    if n.is_integer():
        n = int(n)

    properties = []
    if is_prime(n):
        properties.append("prime")
    if is_perfect(n):
        properties.append("perfect")
    if is_armstrong(n):
        properties.append("armstrong")

    properties.append("odd" if n % 2 != 0 else "even")

    # Fetching fun fact
    try:
        fun_fact = requests.get(f"http://numbersapi.com/{n}").text
    except:
        fun_fact = "No fun fact available"

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum(map(int, str(abs(int(n))))),
        "fun_fact": fun_fact
    }

from fastapi import FastAPI, HTTPException
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

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect (sum of divisors excluding itself equals the number)."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(digit) for digit in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def get_fun_fact(n: int) -> str:
    """Fetch a fun fact from numbersapi.com."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}")
        return response.text if response.status_code == 200 else "No fun fact available."
    except:
        return "Fun fact service unavailable."

@app.get("/api/classify-number")
async def classify_number(number: float):
    """Classify a number and return its mathematical properties."""
    try:
        n = int(number)  # Convert to int if it's a float
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input, must be a number.")

    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    result = {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(n))),
        "fun_fact": get_fun_fact(n)
    }

    return result

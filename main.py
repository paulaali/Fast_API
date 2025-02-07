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
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect_number(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n <= 0:  # 0 and negative numbers are NOT perfect
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(digit) for digit in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def get_number_properties(n: int):
    """Get properties of a number (even/odd, prime, perfect, Armstrong)."""
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
    """
    Classify a number and return its properties and a fun fact.
    """
    try:
        # Ensure the input is a valid integer
        n = int(number)
    except ValueError:
        # Return 400 Bad Request for invalid input
        return {
            "number": number,  # Include the invalid input exactly as provided
            "error": True
        }

    # Get number properties
    properties = get_number_properties(n)

    # Fetch fun fact from numbersapi.com
    fun_fact_response = requests.get(f"http://numbersapi.com/{n}/math")
    fun_fact = fun_fact_response.text if fun_fact_response.status_code == 200 else "No fact available."

    # Calculate the sum of digits
    digit_sum = sum(int(digit) for digit in str(abs(n)))

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect_number(n),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact,
    }
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="Number to classify")):
    try:
        num = float(number)  # Convert to float (supports integers & decimals)
    except ValueError:
        # If conversion fails, return 400 with the invalid input
        raise HTTPException(
            status_code=400,
            detail={"number": number, "error": "Invalid input. Must be a valid number."}
        )

    # Determine properties
    is_prime = check_prime(int(num))
    is_perfect = check_perfect(int(num))
    properties = ["odd" if int(num) % 2 != 0 else "even"]
    digit_sum = sum(int(digit) for digit in str(abs(int(num))))  # Sum of digits
    fun_fact = get_fun_fact(int(num))

    # Response structure
    response = {
        "number": num,
        "is_prime": is_prime,
        "is_perfect": is_perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return response


def check_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def check_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n


def get_fun_fact(n: int) -> str:
    """Fetch a fun fact about the number (basic example)."""
    if n == 371:
        return "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371."
    return f"{n} is an interesting number!"


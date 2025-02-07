from fastapi import FastAPI, Query
import requests

app = FastAPI()

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Number to classify")):
    if not isinstance(number, int):
        return {"number": str(number), "error": True}

    properties = ["odd"] if number % 2 else ["even"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")

    fun_fact = requests.get(f"http://numbersapi.com/{number}/math").text

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(map(int, str(number))),
        "fun_fact": fun_fact
    }

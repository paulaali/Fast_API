from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def classify_number(number):
    properties = []
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if is_armstrong(number):
        properties.append("armstrong")
    return properties

app = FastAPI()

@app.get("/api/classify-number")
def classify_number_api(number: str):
    if not number.replace(".", "").replace("-", "").isdigit():
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": "Invalid input. Must be a valid number."}
        )
    
    number = float(number)
    if number.is_integer():
        number = int(number)
    
    properties = classify_number(number)
    digit_sum = sum(int(digit) for digit in str(abs(number)) if digit.isdigit())
    fun_fact = requests.get(f"http://numbersapi.com/{number}").text
    
    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

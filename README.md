
# Number Classification API

This API classifies numbers based on mathematical properties and provides a fun fact.

## Features
- Identifies if a number is **prime**, **perfect**, or **Armstrong**.
- Determines if the number is **odd** or **even**.
- Computes the **digit sum**.
- Fetches a **fun fact** from the Numbers API.

## API Specification

### **Endpoint**
`GET /api/classify-number?number=371`

### **Response Format (200 OK)**
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

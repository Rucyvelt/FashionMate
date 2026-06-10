from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="FashionMate AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OutfitRequest(BaseModel):
    event: str
    weather: str
    wardrobe: list[str]

class OutfitResponse(BaseModel):
    suggested_items: list[str]
    complete_outfit: str
    reasoning: str

@app.post("/get-outfit", response_model=OutfitResponse)
async def get_outfit(request: OutfitRequest):
    # Smart outfit recommendations based on event and weather
    suggestions = []
    complete_outfit = ""
    reasoning = ""
    
    # Event-based suggestions
    if "wedding" in request.event.lower():
        if "hot" in request.weather.lower() or "warm" in request.weather.lower():
            suggestions = ["Light blue blazer", "Brown leather shoes", "Silk tie", "Pocket square"]
            complete_outfit = "A light blue blazer over your white shirt and black trousers, with brown leather shoes and a silk tie."
            reasoning = "For warm weather weddings, lightweight fabrics keep you cool while looking formal. Brown shoes complement black trousers."
        else:
            suggestions = ["Navy blazer", "Black leather shoes", "Burgundy tie", "Formal watch"]
            complete_outfit = "Navy blazer with your white shirt and black trousers, black leather shoes, and burgundy tie."
            reasoning = "Navy and black create a classic formal look. The burgundy tie adds a touch of elegance."
    
    elif "office" in request.event.lower() or "work" in request.event.lower():
        if "cold" in request.weather.lower():
            suggestions = ["Grey cardigan", "Black leather shoes", "Silver watch"]
            complete_outfit = "Add a grey cardigan for warmth, black leather shoes, and a simple silver watch."
            reasoning = "The cardigan keeps you warm while maintaining professionalism. Simple accessories work best."
        else:
            suggestions = ["Black leather shoes", "Leather belt", "Minimal watch"]
            complete_outfit = "Your white shirt and black trousers with black leather shoes and matching belt."
            reasoning = "Keep it clean and professional. A matching belt and shoes pull the outfit together."
    
    elif "date" in request.event.lower():
        suggestions = ["Brown suede shoes", "Leather jacket", "Cologne"]
        complete_outfit = "White shirt with black trousers, brown suede shoes, and a leather jacket."
        reasoning = "The leather jacket adds edge while staying classy. Brown shoes are more approachable than black."
    
    elif "party" in request.event.lower():
        suggestions = ["Statement watch", "Bold pocket square", "Chelsea boots"]
        complete_outfit = "White shirt with black trousers, Chelsea boots, and a colorful pocket square."
        reasoning = "The pocket square adds personality. Chelsea boots are stylish and comfortable for dancing."
    
    elif "funeral" in request.event.lower():
        suggestions = ["Black tie", "Black shoes", "Dark overcoat"]
        complete_outfit = "Add a black tie, black polished shoes, and a dark overcoat if needed."
        reasoning = "Keep everything muted and respectful. All-black accessories are appropriate."
    
    else:
        # Default recommendations
        suggestions = ["Brown leather shoes", "Matching belt", "Simple watch"]
        complete_outfit = "Your white shirt and black trousers with brown leather accessories."
        reasoning = "These classic pieces work for most casual and semi-formal events."
    
    # Override for weather extremes
    if "rain" in request.weather.lower():
        suggestions.append("Umbrella")
        reasoning += " Don't forget an umbrella for the rain!"
    elif "very cold" in request.weather.lower() or "freezing" in request.weather.lower():
        suggestions.append("Heavy winter coat")
        reasoning += " A heavy coat is essential in this weather."
    
    return OutfitResponse(
        suggested_items=suggestions,
        complete_outfit=complete_outfit,
        reasoning=reasoning
    )

@app.get("/")
def root():
    return {"message": "FashionMate AI is running! (Mock mode - no API needed)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.models import FeedbackRequest, FeedbackResponse

# Load environment variables
load_dotenv()

# Initialize the client securely
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_feedback(request: FeedbackRequest) -> FeedbackResponse:
    # Notice the square brackets [ ] around the two { } dictionaries below!
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": f"You are a helpful language tutor. Analyze the {request.target_language} sentence provided by the user. If it is incorrect, you MUST write the 'explanation' strictly in {request.native_language}. Do not explain in {request.target_language}."
            },
            {
                "role": "user", 
                "content": request.sentence
            }
        ],
        response_format=FeedbackResponse,
    )
    
    return response.choices[0].message.parsed
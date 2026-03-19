import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.models import FeedbackRequest, FeedbackResponse

# Load environment variables
load_dotenv()

# Initialize the client securely
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_feedback(request: FeedbackRequest) -> FeedbackResponse:
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": (
                    f"You are a helpful language tutor. Analyze the {request.target_language} sentence provided by the user. "
                    f"If it is incorrect, you MUST write the 'explanation' strictly in {request.native_language}. Do not explain in {request.target_language}.\n\n"
                    "IMPORTANT SCHEMA RULES:\n"
                    "- 'error_type' MUST be exactly one of: grammar, spelling, word_choice, punctuation, word_order, missing_word, extra_word, conjugation, gender_agreement, number_agreement, tone_register, other.\n"
                    "- 'difficulty' MUST be exactly one of: A1, A2, B1, B2, C1, C2."
                )
            },
            {
                "role": "user", 
                "content": request.sentence
            }
        ],
        response_format=FeedbackResponse,
    )
    
    return response.choices[0].message.parsed
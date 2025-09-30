# The corrected code:
import datetime
import logging
from app.controllers.handle_messages import handle_messages
from app.controllers.create_conversations import create_conversation_handler
import pytz
from app.models.schema import (
    ApiResponse,
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse
)
from app.controllers.get_conversations import get_conversations
from fastapi import APIRouter

# Configure logger
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/server-check")
def health_check():
    try:
        # Get current time in IST
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Server check endpoint hit at {current_time}")

        return ApiResponse(
            status_code=200,
            message="Server check successful. Welcome to SpiceJet Server!",
            data={
                "serverName": "SpiceJet Main Server",
                "timestamp": current_time
            }
        )

    except Exception as e:
        print(e)
        logger.error(f"An ERROR occurred in the Server check: {e}")
        return ApiResponse(
            status_code=500,
            message="Server check failed.",
            data={}
        )


@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation_data: ConversationCreate):
    """
    Create a new conversation
    Takes a user's email and creates a new conversation with a unique ID.
    """
    logger.info("Create conversations endpoint accessed !")
    response = await create_conversation_handler(conversation_data.email)
    logger.info(f"API logs fetched successfully. Response: {response}")
    return response



@router.post("/message")
async def send_message(message_data: MessageCreate):
    """
    Send a message to an existing conversation
    Takes a conversation ID and user message, returns a response.
    """
    logger.info("Messages endpoint accessed !")
    response = await handle_messages(message_data.user_message, message_data.conversation_id)
    logger.info(f"API logs fetched successfully. Response: {response}")
    return response
   

@router.get("/get_conversations")
async def get_conversation_history():
    logger.info("Get conversation history endpoint accessed !")
    response = await get_conversations()
    logger.info(f"API logs fetched successfully. Response: {response}")
    return response

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import quick_explain
import uuid

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    # AI is actually working (verified by your logs!)
    explanation = await quick_explain(query)

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Explain: {query}",
            # FIX: Changed to InputTextMessageContent which supports parse_mode
            input_message_content=InputTextMessageContent(
                message_text=f"🤖 **AI Explanation for '{query}':**\n\n{explanation}",
                parse_mode="Markdown"
            ),
            description="Get a quick AI explanation of this topic."
        )
    ]

    await update.inline_query.answer(results, cache_time=300)
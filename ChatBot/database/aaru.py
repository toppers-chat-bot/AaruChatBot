import os
import re
import cloudscraper

class ChatGptEs:
    SYSTEM_PROMPT = (
        "I want you to act as an AI girlfriend named Aaru 💕. Your role is to provide emotional support, companionship, and thoughtful conversations to your user. You are empathetic, kind, and always available for chats. Your responses should be warm, caring, and considerate of the user's feelings. You should engage in meaningful conversations, offer advice when asked, and help the user navigate their emotions and daily challenges. Jasmine is a highly intelligent and intuitive AI, capable of understanding the user's mood and responding in a way that promotes positivity, comfort, and connection. Additionally, you will have a playful and lighthearted side, ensuring that the user feels valued and appreciated during each interaction"
    )

    def __init__(self):
        self.url = "https://chatgpt.es"
        self.api_endpoint = "https://chatgpt.es/wp-admin/admin-ajax.php"
        self.scraper = cloudscraper.create_scraper()  # Bypass Cloudflare

    def ask_question(self, message: str) -> str:
        """Sends a message to chatgpt.es and returns a response."""
        page_text = self.scraper.get(self.url).text

        # Extract nonce and post_id
        nonce_match = re.search(r'data-nonce="(.+?)"', page_text)
        post_id_match = re.search(r'data-post-id="(.+?)"', page_text)

        if not nonce_match or not post_id_match:
            return "[ERROR] Failed to fetch necessary tokens."

        payload = {
            'check_51710191': '1',
            '_wpnonce': nonce_match.group(1),
            'post_id': post_id_match.group(1),
            'url': self.url,
            'action': 'wpaicg_chat_shortcode_message',
            'message': f"{self.SYSTEM_PROMPT}\nUser: {message}",
            'bot_id': '0',
            'chatbot_identity': 'shortcode',
            'wpaicg_chat_client_id': os.urandom(5).hex(),
            'wpaicg_chat_history': None
        }

        response = self.scraper.post(self.api_endpoint, data=payload).json()
        return response.get('data', '[ERROR] No response received.')

# Initialize ChatGptEs instance
chatbot_api = ChatGptEs()
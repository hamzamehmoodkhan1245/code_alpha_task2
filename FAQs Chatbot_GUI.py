import customtkinter as ctk
import nltk
from nltk.tokenize import word_tokenize
import os

# Ensure NLTK data path is set correctly
nltk_data_path = r"C:/Users/Hamza/Desktop/MY ROBOT/MY INETRSHIP PROJECTS/nltk_data"
nltk.data.path.append(nltk_data_path)

# Ensure 'punkt' is downloaded in the given directory
try:
    word_tokenize("test")  # Try using it to ensure it's working
except LookupError:
    print("[ERROR] 'punkt' tokenizer not found. Ensure it's available at:", nltk_data_path)

# FAQ knowledge base
faq_data = {
    "how do i track my order": "You can track your order by logging into your account and clicking on 'My Orders'.",
    "what is your return policy": "You can return any item within 30 days of purchase.",
    "how can i contact support": "You can contact support through our Contact Us page or by calling 123-456-7890.",
    "what payment methods are accepted": "We accept credit/debit cards, PayPal, and bank transfers.",
    "do you offer international shipping": "Yes, we ship internationally. Shipping charges may apply.",
    "how to cancel my order": "To cancel your order, go to 'My Orders' and click on 'Cancel Order'.",
    "can i change my delivery address": "Yes, you can change the delivery address before the order is shipped.",
    "how do i apply a promo code": "You can apply the promo code at checkout in the 'Promo Code' field.",
    "where is my refund": "Refunds are processed within 5-7 business days after return approval.",
    "is cash on delivery available": "Yes, cash on delivery is available in select cities."
}

# Helper: Tokenize safely
def safe_tokenize(text):
    try:
        return set(word_tokenize(text.lower()))
    except Exception as e:
        print("[Tokenizer Error]:", e)
        return set(text.lower().split())

# Response logic
def get_response(user_input):
    user_words = safe_tokenize(user_input)
    max_match = 0
    best_response = None

    for question, answer in faq_data.items():
        question_words = safe_tokenize(question)
        match_count = len(user_words.intersection(question_words))

        if match_count > max_match:
            max_match = match_count
            best_response = answer

    if max_match > 1:  # Only answer if meaningful match
        return best_response
    return "Sorry, I couldn't understand your question. Please try rephrasing."

# Send user message and get bot response
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    chatbox.configure(state="normal")
    chatbox.insert("end", f"You: {user_input}\n")
    response = get_response(user_input)
    chatbox.insert("end", f"Bot: {response}\n\n")
    chatbox.configure(state="disabled")
    chatbox.yview("end")
    entry.delete(0, "end")

# Clear chat history
def clear_chat():
    chatbox.configure(state="normal")
    chatbox.delete("1.0", "end")
    chatbox.configure(state="disabled")
    entry.delete(0, "end")
    entry.focus()

# Setup GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Online Market FAQ Chatbot")
app.geometry("620x620")
app.minsize(500, 500)

frame = ctk.CTkFrame(master=app, corner_radius=15)
frame.pack(padx=20, pady=20, fill="both", expand=True)

title = ctk.CTkLabel(master=frame, text="📦 Online Market FAQ Chatbot", font=("Arial Black", 22))
title.pack(pady=(15, 5))

chatbox = ctk.CTkTextbox(master=frame, height=400, wrap="word", font=("Consolas", 14), corner_radius=10)
chatbox.configure(state="disabled")
chatbox.pack(padx=15, pady=10, fill="both", expand=True)

entry = ctk.CTkEntry(master=frame, font=("Arial", 14), placeholder_text="Ask something like 'how do I track my order'...")
entry.pack(padx=15, pady=(0, 10), fill="x")

button_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
button_frame.pack(pady=(0, 15))

send_btn = ctk.CTkButton(master=button_frame, text="Send", font=("Arial", 14), command=send_message, corner_radius=10)
send_btn.grid(row=0, column=0, padx=10)

clear_btn = ctk.CTkButton(master=button_frame, text="Clear Chat", font=("Arial", 14), command=clear_chat, corner_radius=10, fg_color="red")
clear_btn.grid(row=0, column=1, padx=10)

app.mainloop()

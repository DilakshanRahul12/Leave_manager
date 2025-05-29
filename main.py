from database import load_employees, save_employees
from ai import process_user_input
from utils import clear_screen

def print_chat(messages):
    """Prints the chat history in a chat-like format."""
    for msg in messages:
        if msg["role"] == "user":
            print(f"You: {msg['content']}")
        elif msg["role"] == "assistant":
            print(f"AI: {msg['content']}")
        # Optionally show system messages
        # elif msg["role"] == "system":
        #     print(f"(system): {msg['content']}")

def main():
    employees = load_employees()
    clear_screen()  # Clear only once at start
    print("Welcome to the Leave Management System (AI-powered)!")
    username = input("Enter your name: ").strip()
    if username not in employees:
        print("User not found. Exiting.")
        return
    messages = []
    while True:
        #clear_screen()  # Optional: comment/remove for a true chat scroll feel
        print_chat(messages)
        print(f"\nType your request (or 'quit' to exit):")
        user_input = input("> ")
        if user_input.lower() in ["quit", "exit"]:
            save_employees(employees)
            print("Goodbye!")
            break
        # Store user message for chat display
        messages.append({"role": "user", "content": user_input})
        response, employees, messages = process_user_input(user_input, username, employees, messages)
        # Store AI response for chat display
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
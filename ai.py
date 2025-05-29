import google.generativeai as genai
from utils import extract_dates, parse_int_from_text

# Set your Gemini API key
genai.configure(api_key="AIzaSyDOCgD0PZajv4XRfaGeUV5GGQLkUsPQQgg")

def process_user_input(user_input, username, employees, messages=None):
    """
    Process user input using Gemini API to extract intent and entities,
    then perform the corresponding action and return a response.
    """
    if messages is None:
        messages = []
    # Add system prompt if first message
    if not messages:
        system_prompt = (
            "You are an HR assistant for leave management. "
            "Extract the user's intent (check balance, request leave, cancel leave, view history) "
            "and relevant entities such as leave type, number of days, and start date. "
            "Respond in a short, clear way for the terminal."
        )
        messages.append({"role": "system", "content": system_prompt})

    # Add user's message
    messages.append({"role": "user", "content": user_input})

    # Gemini expects a single string, so combine the conversation
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"{msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"


    # Call Gemini to get the AI's interpretation
    model = genai.GenerativeModel("gemini-2.0-flash")
    result = model.generate_content(prompt)
    ai_text = result.text.strip().lower()
    
    # Add assistant's reply to memory
    messages.append({"role": "assistant", "content": ai_text})

    # Simple intent/entity matching (expand for robustness)
    if "balance" in ai_text:
        leave_type = None
        for t in employees[username].leave_balance.balances:
            if t.lower() in user_input.lower():
                leave_type = t
                break
        if leave_type:
            days = employees[username].leave_balance.get(leave_type)
            return f"You have {days} {leave_type} left.", employees, messages
        else:
            return "Specify which leave type you want to check.", employees, messages

    elif any(x in ai_text for x in ["request", "apply", "take"]):
        leave_type = None
        for t in employees[username].leave_balance.balances:
            if t.lower() in user_input.lower():
                leave_type = t
                break
        dates = extract_dates(user_input)
        days = parse_int_from_text(user_input)
        if not leave_type or not days or not dates:
            return "Please specify leave type, number of days, and start date.", employees, messages
        # Check balance and date validity inside Employee
        success, msg = employees[username].request_leave(leave_type, days, dates[0])
        return msg, employees, messages

    elif "cancel" in ai_text:
        leave_type = None
        for t in employees[username].leave_balance.balances:
            if t.lower() in user_input.lower():
                leave_type = t
                break
        dates = extract_dates(user_input)
        if not leave_type or not dates:
            return "Specify the leave type and start date to cancel.", employees, messages
        success, msg = employees[username].cancel_leave(leave_type, dates[0])
        return msg, employees, messages

    elif "history" in ai_text:
        history = employees[username].leave_history
        if not history:
            return "No leave history found.", employees, messages
        msg = "Your leave history:\n"
        for req in history:
            msg += f"{req.leave_type}: {req.days} days from {req.start_date} [{req.status}]\n"
        return msg, employees, messages

    else:
        return "Sorry, I didn't understand that. Please rephrase.", employees, messages
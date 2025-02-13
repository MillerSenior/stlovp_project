import datetime

def log_stage(title: str, message: str = None, result=None):
    """
    Prints a formatted log message with an appropriate emoji.

    Args:
        title (str): The main title for the log stage.
        message (str, optional): Additional information about what is happening.
        result (any, optional): The result of the function (if applicable).
    """
    # Define section separator
    separator = "=" * 50

    # Print the formatted log message
    print(f"\n{separator}")
    print(f"{title}")
    
    # Print optional message
    if message:
        print(f"   ➝ {message}")

    # Print function return result if provided
    if result is not None:
        print(f"   ✅ Result: {result}")

    print(f"{separator}\n")

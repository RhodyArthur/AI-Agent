import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--verbose"]

    if len(args) != 1:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = args[0]

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(20):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(final_response)
                break
        except Exception as e:
            print(f'Error: {e}')


def generate_content(client, messages, verbose):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Rate limit exceeded. Please try again in a few minutes.")
            sys.exit(1)
        else:
            raise e

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        if response.text and response.text.strip():
            return response.text
        else:
            return None

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        # Print the actual function output for the tests
        function_response = function_call_result.parts[0].function_response.response
        if "result" in function_response:
            print(function_response["result"])
        elif "error" in function_response:
            print(f"Error: {function_response['error']}")
            
        function_responses.append(function_call_result.parts[0])


    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    function_response_message = types.Content(role="user", parts=function_responses)
    messages.append(function_response_message)

    return None


if __name__ == "__main__":
    main()
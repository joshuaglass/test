import os
from livekit import api
from dotenv import load_dotenv
import argparse

load_dotenv()

LIVEKIT_URL = os.environ.get("LIVEKIT_URL")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET")

def main():
    if not all([LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET]):
        print("Error: Missing LiveKit environment variables in .env file.")
        print("Please ensure LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET are set.")
        exit(1)

    parser = argparse.ArgumentParser(description="Generate a LiveKit access token.")
    parser.add_argument("--room", type=str, default="task-manager-room", help="The LiveKit room name.")
    parser.add_argument("--identity", type=str, default="user", help="The participant identity.")
    args = parser.parse_args()

    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) \
        .with_identity(args.identity) \
        .with_name("Task Manager User") \
        .with_grants(api.VideoGrant(room_join=True, room=args.room)) \
        .to_jwt()

    print(f"LiveKit URL: {LIVEKIT_URL}")
    print(f"Room Name: {args.room}")
    print(f"Token: {token}")

if __name__ == "__main__":
    main()
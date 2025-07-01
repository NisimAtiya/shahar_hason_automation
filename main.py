from checker.checker import get_shows
from notify.notify import send_event_to_same_email

def main():
    """
    Main entry point: fetch shows and send them by email.
    """
    artist = "שחר חסון"
    
    print(f"🎭 Fetching shows for {artist}...")
    events = get_shows(artist)
    
    if not events:
        print("⚠️ No events found.")
        return
    
    print(f"📧 Sending email with {len(events)} events...")
    recipient_email = "n207302027@gmail.com"
    send_event_to_same_email(artist, events, recipient_email)
    
    print("✅ Done.")

if __name__ == "__main__":
    main()


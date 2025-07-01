from checker.checker import get_shows
from notify.notify import send_event_to_same_email
from notify.notify import no_events_found

def main():
    """
    Main entry point: fetch shows and send them by email.
    """
    artist = "ניסים עטייה"
    recipient_email = "n207302027@gmail.com"

    
    print(f"🎭 Fetching shows for {artist[::-1]}...")
    events = get_shows(artist)
    
    if not events:
        print("⚠️ No events found.")
        no_events_found(artist,recipient_email)
        return
    
    print(f"📧 Sending email with {len(events)} events...")
    send_event_to_same_email(artist, events, recipient_email)
    
    print("✅ Done.")

if __name__ == "__main__":
    main()


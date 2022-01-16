from typing import List
from twilio.rest import Client
import __init__
from data.Fleet import Fleet
import os
from consts import StatusCode

CLIENT = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))

'''
Sends the message to the phone
'''
def send_message(text):
    try:
        CLIENT.messages.create(to=os.getenv("NOTIF_PH"), 
                        from_=os.getenv("TWILIO_PH"), 
                        body=text)
    except Exception as e:
        print(f"\nAn error occured: {e}")
        return False

    print("Message was sent successfully!")
    return True

'''
Takes any data given to it and formats it into the proper message
to send via text.
'''
def format_message(status_code, data: List[Fleet]):
    if status_code == StatusCode.ENEMY:
        # Edge case where you are truly fucked and receiving pincer attacks
        if len(data) == 1:
            single_enemy: Fleet = data[0]
            send_message(f"(NP) ALERT: {single_enemy.strength} ships have entered scanning range from {single_enemy.get_owner_name()}")
        elif len(data) > 1:
            initial: str = "(NP) ALERT: Multiple fleets have entered scanning range. Details are as follows\n"
            for e in data:
                initial += f"{e.strength} ships - {e.get_owner_name()}\n"
            initial += "Good luck out there. I'll be surprised if anyone ever gets this text. Let me know."
            send_message(initial)

    elif status_code == StatusCode.FLEET_SHIPS:
        pass
    elif status_code == StatusCode.FLEET_WATCH:
        pass
    else:
        raise Exception(f'Unknown status code: {status_code}')
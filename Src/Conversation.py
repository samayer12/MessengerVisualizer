class Conversation:

    participants = ""
    messages = []
    title = ""
    is_still_participant = False
    thread_type = ""
    thread_path = ""


    def __init__(self, conversation_source):
        print("Processing conversation")
        self.participants = conversation_source["participants"]
        self.messages = conversation_source["messages"]
        self.title = conversation_source["title"]
        self.is_still_participant = conversation_source["is_still_participant"]
        self.thread_type = conversation_source["thread_type"]
        self.thread_path = conversation_source["thread_path" ]


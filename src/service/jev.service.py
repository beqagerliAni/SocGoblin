from typesafe_sdk import TypeSafeClient
class JevService:
    client: TypeSafeClient
    def __init__(self):
        self.client = TypeSafeClient(model="jev-latest")
        pass
    
    def extractPersonInformation(self, state:str):
        # in hear we will extract information
        response = self.client.system_one(
            state,
        )
        pass
    pass
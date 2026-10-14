from typesafe_sdk import TypeSafeClient
from src.config import JEV_KEY
from src.model import FacebookPostModel, ScarapperModel
class JevService:
    client: TypeSafeClient
    def __init__(self):
        self.client = TypeSafeClient(api_key=JEV_KEY, model="jev-latest")
        pass
    
    # define state modal
    def extractPostData(self, state:FacebookPostModel):
        #so in hear we will extract information of the post
        # and use jev model so we could ask some questions
        # like dose this person wonts to buy a car or similar
        pass
    pass
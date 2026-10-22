from pydantic import BaseModel

from src.modules.analitics.model.commentComplaints import CommentComplaintsModel
from src.modules.analitics.model.postTopicModel import PostTopicModel



class AnaliticsModel(BaseModel):
    postTopic: PostTopicModel
    commentComplaints: CommentComplaintsModel

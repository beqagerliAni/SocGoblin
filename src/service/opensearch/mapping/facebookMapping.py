facebookMapping = {
    "mappings": {
        "dynamic": False,
        "properties": {
            "contentType": {"type": "keyword"},
            "postUrl": {"type": "keyword"},
            "postId": {"type": "keyword"},
            "postedAt": {"type": "date"},
            "text": {"type": "text"},
            "reactions": {"type": "long"},
            "comments": {"type": "long"},
            "shares": {"type": "long"},
            "views": {"type": "long"},
            "videoDuration": {"type": "float"},
            "reactionBreakdown": {"type": "object", "enabled": False},
            "author": {
                "properties": {
                    "id": {"type": "keyword"},
                    "url": {"type": "keyword"},
                    "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "avatar": {"type": "keyword", "index": False},
                },
            },
            "source": {
                "properties": {
                    "url": {"type": "keyword"},
                    "name": {"type": "keyword"},
                },
            },
            "media": {
                "properties": {
                    "url": {"type": "keyword", "index": False},
                    "type": {"type": "keyword"},
                    "imageOcr": {"type": "text"},
                    "videoUrl": {"type": "keyword", "index": False},
                    "thumbnailUrl": {"type": "keyword", "index": False},
                },
            },
            "linkPreview": {"type": "object", "enabled": False},
            "mentions": {"type": "object", "enabled": False},
            "collaborators": {"type": "object", "enabled": False},
            "topComments": {
                "properties": {
                    "url": {"type": "keyword"},
                    "date": {"type": "date"},
                    "text": {"type": "text"},
                    "likes": {"type": "long"},
                    "author": {"type": "keyword"},
                },
            },
            "hashtags": {"type": "keyword"},
        },
    },
}

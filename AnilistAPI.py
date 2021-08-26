import json
import requests

from typing import Union
from requests.models import Response
from enum import Enum, auto

URL = "https://graphql.anilist.co"

# DOCS: https://github.com/AniList/ApiV2-GraphQL-Docs

# ENUMS
class MediaType(Enum):
    ANIME = "ANIME"
    MANGA = "MANGA"


class MediaListStatus(Enum):
    CURRENT = "CURRENT"
    PLANNING = "PLANNING"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"
    PAUSED = "PAUSED"
    REPEATING = "REPEATING"


# GENERAL
class User:
    def __init__(self, identifier: Union[int, str]) -> None:
        if type(identifier) is int:
            self.userId = identifier

            query = "query($userId: Int){User(id:$userId){name}}"
            variables = {"userId": self.userId}

            response = Query(query, variables).response()
            json_object = json.loads(response.text)
            self.userName = json_object["data"]["User"]["name"]

        elif type(identifier) is str:
            self.userName = identifier

            query = "query($userName: String){User(name:$userName){id}}"
            variables = {"userName": self.userName}

            response = Query(query, variables).response()
            json_object = json.loads(response.text)
            self.userId = json_object["data"]["User"]["id"]
        else:
            raise TypeError(f"The parameter identifier cannot be {type(identifier)}.")


# QUERIES
class Query:
    def __init__(self, query: str = None, variables: dict = None):
        self.query = query
        self.variables = variables

    def response(self) -> Response:
        return requests.post(
            URL, json={"query": self.query, "variables": self.variables}
        )

    def display(self, indentation: int = None) -> None:
        response = self.response()
        json_object = json.loads(response.text)
        print(
            json.dumps(json_object, ensure_ascii=False, indent=indentation)
            .encode("utf8")
            .decode()
        )

    def save_as_json(self, file_name: str, indentation: int = None) -> None:
        response = self.response()
        json_object = json.loads(response.text)
        with open(f"{file_name}.json", "w", encoding="utf8") as f:
            json.dump(json_object, f, ensure_ascii=False, indent=indentation)


class MediaQuery(Query):
    def __init__(self, mediaId: int, mediaType: MediaType = MediaType.ANIME):
        self.query = """
        query ($mediaId: Int, $mediaType: MediaType) {
            Media (id: $mediaId, type: $mediaType) {
                type
                format
                genres
                title {
                    english
                }
            }
        }"""
        self.variables = {"mediaId": mediaId, "mediaType": mediaType.name}


class UserQuery(Query):
    def __init__(self, user: User):
        self.query = """
        query ($userId: Int) {
            User (id: $userId) {
                id
                name
            }
        }"""
        self.variables = {"userId": user.userId}


class MediaListCollectionQuery(Query):
    def __init__(self, user: User, mediaType: MediaType = MediaType.ANIME):
        self.query = """
        query ($userId: Int, $mediaType: MediaType) {
            MediaListCollection(userId: $userId, type: $mediaType) {
                lists {
                    name
                    status
                    entries {
                        mediaId
                        media {
                            title {
                                english
                                native
                            }
                        }
                    }
                }
            }
        }"""
        self.variables = {"userId": user.userId, "mediaType": mediaType.name}

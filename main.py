from AnilistAPI import *

# DOCS: https://github.com/AniList/ApiV2-GraphQL-Docs

# MediaQuery(431).display(2)
# UserQuery("Alpe").display(2)
# MediaListCollectionQuery(User("NomisDJ")).display()


def get_media_list(
    user: User,
    mediaType: MediaType = MediaType.ANIME,
    mediaListStatus: MediaListStatus = MediaListStatus.PLANNING,
):
    response = MediaListCollectionQuery(user, mediaType).response()
    json_object = json.loads(response.text)
    lists = json_object["data"]["MediaListCollection"]["lists"]

    planning_list = []
    for lst in lists:
        if lst["status"] == mediaListStatus.name:
            for entry in lst["entries"]:
                planning_list.append(entry["mediaId"])
            break

    print(planning_list)


# print(MediaQuery(218372636).display())
alpe = User("Alpe")
get_media_list(alpe, mediaListStatus=MediaListStatus.COMPLETED)
# MediaQuery(128545).display(2)


# INTERSECTING MEDIA LISTS OF MULTIPLE USERS

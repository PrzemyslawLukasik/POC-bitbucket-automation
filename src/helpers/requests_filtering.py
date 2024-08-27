from requests.models import Response


def filter_repository_names(list_of_repositories: Response) -> list[str]:
    list_of_repository_names = []
    for item in list_of_repositories.json()["values"]:
        list_of_repository_names.append(item["name"])
    return list_of_repository_names


def verify_repository_name_in_response(resp: Response, rep_slug: str) -> bool:
    list_of_names = filter_repository_names(resp)
    return True if rep_slug in list_of_names else False

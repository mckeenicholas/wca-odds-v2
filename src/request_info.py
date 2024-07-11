from requests import get
from requests.exceptions import HTTPError


def get_pb_rank(person, event):
    """
    Gets the global ranking of the competitor in the given event.

    Parameters
    ----------
    person : dict
        A person object from the WCIF.
    event : str
        The event to query.

    Returns
    -------
    int or None
        Competitor's rank in the event, or None if not found.
    """
    for result in person["personalBests"]:
        if result["eventId"] == event and result["type"] == "average":
            return result["worldRanking"]


def get_competitors(compId: str, event, num: int = 16):
    """
    Retrieves competitors from a competition based on specified criteria.

    Parameters
    ----------
    compId : str
        The competition ID.
    event : str
        The event to filter competitors by.
    num : int, optional
        Number of top competitors to return. Defaults to 16.

    Returns
    -------
    list
        A list of dictionaries containing competitor IDs and names,
        sorted by their ranking in the specified event.

    Raises
    ------
    HTTPError
        If the competition with the specified ID is not found.
    """
    url = f"https://api.worldcubeassociation.org/competitions/{compId}/wcif/public"
    response = get(url)
    data = response.json()

    if response.status_code != 200:
        raise HTTPError(
            f"Error {response.status_code}: Competition with id {compId} not found."
        )

    competitors = data["persons"]
    competitors_in_event = []

    for competitor in competitors:
        if (
            competitor["registration"] is not None
            and event in competitor["registration"]["eventIds"]
        ):
            rank = get_pb_rank(competitor, event)
            if rank is not None:
                competitors_in_event.append(
                    {
                        "id": competitor["wcaId"],
                        "name": competitor["name"],
                        "rank": rank,
                    }
                )

    competitors_in_event.sort(key=lambda x: x["rank"])

    return [{"id": i["id"], "name": i["name"]} for i in competitors_in_event[:num]]

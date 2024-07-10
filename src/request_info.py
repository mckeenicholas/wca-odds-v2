from requests import get
from collections import namedtuple


def get_pb_rank(person, event):
    for result in person["personalBests"]:
        if result["eventId"] == event and result["type"] == "average":
            return result["worldRanking"]


def get_competitors(compId: str, event, num: int = 16):
    url = f"https://api.worldcubeassociation.org/competitions/{compId}/wcif/public"
    data = get(url).json()

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

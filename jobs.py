from urllib.parse import parse_qs, urlparse

import aiohttp

URL = "https://yandex.ru/jobs/api/publications"

PARAMS = {
    "cities": "minsk",
    "work_modes": "remote",
    "pro_levels": ["intern", "junior"],
    "page_size": 20,
}

HEADERS = {"User-Agent": "Mozilla/5.0"}


async def get_jobs():

    jobs = []
    params = PARAMS.copy()

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            async with session.get(URL, params=params) as response:
                data = await response.json()

            for job in data["results"]:
                jobs.append(
                    {
                        "id": job["id"],
                        "title": job["title"],
                        "url": f"https://yandex.ru/jobs/vacancies/{job['publication_slug_url']}",
                    }
                )

            next_url = data["next"]

            if not next_url:
                break

            parsed = urlparse(next_url)
            cursor = parse_qs(parsed.query)["cursor"][0]

            params["cursor"] = cursor

    return jobs

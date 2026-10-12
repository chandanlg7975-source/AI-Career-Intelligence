import requests
from urllib.parse import quote

REMOTIVE_API = "https://remotive.com/api/remote-jobs"


def search_jobs(query, limit=8):
    """
    Search remote jobs using the Remotive public jobs API.
    """

    query = query.strip()

    if not query:
        return []

    try:
        url = f"{REMOTIVE_API}?search={quote(query)}"

        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get("jobs", [])

        results = []

        for job in jobs[:limit]:

            results.append(
                {
                    "title": job.get(
                        "title",
                        "Unknown Job"
                    ),

                    "company": job.get(
                        "company_name",
                        "Unknown Company"
                    ),

                    "location": job.get(
                        "candidate_required_location",
                        "Remote"
                    ),

                    "job_type": job.get(
                        "job_type",
                        "Not specified"
                    ),

                    "category": job.get(
                        "category",
                        "Not specified"
                    ),

                    "salary": job.get(
                        "salary",
                        "Not specified"
                    ),

                    "url": job.get(
                        "url",
                        ""
                    ),

                    "description": job.get(
                        "description",
                        ""
                    ),

                    "publication_date": job.get(
                        "publication_date",
                        ""
                    )
                }
            )

        return results

    except requests.RequestException:
        return []


def format_jobs(jobs, query):
    """
    Convert job results into a readable Career Assistant response.
    """

    if not jobs:

        return (
            f"🔎 **No matching jobs found for "
            f"`{query}` right now.**\n\n"
            "Try another job title such as "
            "`AI Engineer`, `Machine Learning Engineer`, "
            "`Python Developer`, or `Data Scientist`."
        )

    response = []

    response.append(
        f"## 🔎 Job Opportunities for: {query}"
    )

    response.append(
        f"Found **{len(jobs)} matching remote opportunities**."
    )

    response.append(
        "> ℹ️ Job listings are provided through Remotive."
    )

    for index, job in enumerate(jobs, start=1):

        title = job["title"]
        company = job["company"]
        location = job["location"]
        job_type = job["job_type"]
        salary = job["salary"]
        url = job["url"]

        text = f"""
### {index}. 💼 {title}

**🏢 Company:** {company}

**📍 Location:** {location}

**💼 Type:** {job_type}

**💰 Salary:** {salary}
"""

        if url:

            text += (
                f"\n**🔗 [View & Apply]({url})**\n"
            )

        response.append(text)

    response.append(
        "\n💡 **Tip:** Always check the original "
        "job listing for eligibility, location, "
        "experience requirements and application details."
    )

    return "\n".join(response)


if __name__ == "__main__":

    query = input(
        "Enter job title to search: "
    )

    jobs = search_jobs(query)

    print(
        format_jobs(
            jobs,
            query
        )
    )
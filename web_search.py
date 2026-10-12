import os
from dotenv import load_dotenv
from tavily import TavilyClient


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")

if not API_KEY:
    raise ValueError(
        "TAVILY_API_KEY not found in .env file"
    )

client = TavilyClient(
    api_key=API_KEY
)


# ============================================================
# BUILD SMART JOB SEARCH QUERY
# ============================================================

def build_job_query(query):

    query = query.strip()

    if not query:
        return ""

    query_lower = query.lower()

    extra_terms = []

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    if any(
        word in query_lower
        for word in [
            "fresher",
            "freshers",
            "fresh graduate",
            "entry level",
            "entry-level",
            "0 years",
            "no experience"
        ]
    ):

        extra_terms.extend([
            "fresher",
            "entry level",
            "0-2 years experience"
        ])

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    if "india" in query_lower:

        extra_terms.append(
            "India"
        )

    if any(
        city in query_lower
        for city in [
            "bangalore",
            "bengaluru",
            "chennai",
            "hyderabad",
            "pune",
            "mumbai",
            "delhi",
            "noida",
            "gurgaon",
            "gurugram"
        ]
    ):

        extra_terms.append(
            "jobs"
        )

    # --------------------------------------------------------
    # REMOTE
    # --------------------------------------------------------

    if any(
        word in query_lower
        for word in [
            "remote",
            "work from home",
            "wfh"
        ]
    ):

        extra_terms.extend([
            "remote",
            "work from home"
        ])

    # --------------------------------------------------------
    # JOB SEARCH INTENT
    # --------------------------------------------------------

    if any(
        word in query_lower
        for word in [
            "job",
            "jobs",
            "opening",
            "openings",
            "vacancy",
            "vacancies",
            "hiring",
            "position",
            "positions"
        ]
    ):

        extra_terms.append(
            "current job openings"
        )

    # --------------------------------------------------------
    # FINAL QUERY
    # --------------------------------------------------------

    final_query = query

    if extra_terms:

        final_query += " " + " ".join(
            dict.fromkeys(extra_terms)
        )

    return final_query


# ============================================================
# WEB SEARCH
# ============================================================

def search_web(
    query,
    max_results=8
):

    search_query = build_job_query(
        query
    )

    if not search_query:
        return []

    try:

        response = client.search(
            query=search_query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=False
        )

        results = []

        for item in response.get(
            "results",
            []
        ):

            results.append(
                {
                    "title": item.get(
                        "title",
                        "Untitled"
                    ),

                    "url": item.get(
                        "url",
                        ""
                    ),

                    "content": item.get(
                        "content",
                        ""
                    ),

                    "score": item.get(
                        "score",
                        0
                    )
                }
            )

        return results

    except Exception as e:

        print(
            "Web search error:",
            e
        )

        return []


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    print(
        "======================================"
    )

    print(
        " AI Career Intelligence Web Search"
    )

    print(
        "======================================"
    )

    query = input(
        "\nEnter job search: "
    )

    smart_query = build_job_query(
        query
    )

    print(
        f"\n🔎 Smart Search Query:"
    )

    print(
        smart_query
    )

    results = search_web(
        query
    )

    print(
        "\n🌐 WEB RESULTS"
    )

    print(
        "=============="
    )

    if not results:

        print(
            "No results found."
        )

    else:

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{result['title']}"
            )

            print(
                f"URL: {result['url']}"
            )

            print(
                f"Score: "
                f"{result['score']}"
            )

            content = result.get(
                "content",
                ""
            )

            if len(content) > 250:

                content = (
                    content[:250]
                    + "..."
                )

            print(
                f"Description: {content}"
            )
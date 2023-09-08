"""
Functions to fetch the defi explore data for makerdao
"""
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def fetch_defiexplore_data(
    page_num: int = 1,
) -> dict:
    """
    Function to fetch the makerdao vaults data
    """
    request_url = f"https://defiexplore.com/api/topcdps?pageNumber={page_num}\
&pageSize=20&order=DESC&sortBy=debt&filters="

    return requests.get(request_url, headers=HEADERS, timeout=10).json()


def get_defiexplore_data_total_num(
    response: dict,
) -> int:
    """
    Function to get the total number of pages
    """

    return response["total"]


def get_defiexplore_page_number(
    response: dict,
) -> int:
    """
    Function to get the page number of pages
    """

    return int(response["pageNumber"])


if __name__ == "__main__":
    print(
        fetch_defiexplore_data(
            page_num=1534,
        )
    )

# from github import Github
# import streamlit as st
# from ratelimit import limits, sleep_and_retry
import requests
from crawl import crawl_latest_update
# @sleep_and_retry
# @limits(calls=RATE_LIMIT, period=1)
def search_github_code(query, token, queries_per_page=5):
    # Define the base URL for GitHub code search API
    base_url = 'https://api.github.com/search/code'

    # Define parameters for the search query
    params = {
        'q': query,
        'per_page': queries_per_page  # Number of results per page
    }

    # Define headers with Authorization using the token
    headers = {
        'Authorization': f'token {token}'
    }

    try:
        # Make a GET request to GitHub API
        response = requests.get(base_url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            for item in data['items']:
                item['last_modified_time']=crawl_latest_update(item['html_url'])

            # Sort the list of dictionaries by the 'last_modified_time' key
            sorted_data = sorted(data['items'], key=lambda x: x['last_modified_time'], reverse=True)

            # Extract and print search results
            for item in sorted_data:
                print('Repository:', item['repository']['full_name'])
                print('File:', item['path'])
                print('URL:', item['html_url'])
                print('Latest modified time:', item['last_modified_time'])
                print('Score:', item['score'])
                print('-' * 50)
        else:
            # Print error message if request was not successful
            print('Failed to retrieve data from GitHub. Status Code:', response.status_code)
    except Exception as e:
        # Print any exception that occurs during the process
        print('An error occurred:', str(e))
if __name__ == "__main__":
    # YOUR_GITHUB_TOKEN = "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"
    # YOUR_GITHUB_TOKEN = "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"
    YOUR_GITHUB_TOKEN = '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'
    search_query = input("Enter a search query for repositories: ")
    max_results = 10 # search for only first 10 results
    # search_github_repositories(search_query, YOUR_GITHUB_TOKEN, max_results)
    search_github_code(search_query, YOUR_GITHUB_TOKEN, max_results)

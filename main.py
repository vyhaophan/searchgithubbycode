import streamlit as st
from github import Github
import requests
from crawl import crawl_latest_update
import hmac

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

def search_github_code(query, token, queries_per_page=5, sort_desc = True):
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
                item['last_modified_time'], item['text_modified_time']  =crawl_latest_update(item['html_url'])

            # Sort the list of dictionaries by the 'last_modified_time' key
            if sort_desc: sorted_data = sorted(data['items'], key=lambda x: x['last_modified_time'], reverse=True)
            else: sorted_data = sorted(data['items'], key=lambda x: x['last_modified_time'])

            # Extract and print search results
            for item in sorted_data:
                with st.expander(f"Repository: {item['repository']['full_name']}"):
                    st.write('File:', item['path'])
                    st.write('URL:', item['html_url'])
                    st.write('Latest modified time:', item['text_modified_time'])
                    # print('-' * 50)
        else:
            # Print error message if request was not successful
            print('Failed to retrieve data from GitHub. Status Code:', response.status_code)
    except Exception as e:
        # Print any exception that occurs during the process
        print('An error occurred:', str(e))

# Streamlit UI
def main():
    st.title("GitHub Code Search")

    # Input for search query
    search_query = st.text_input("Enter a search query for code")
    # input for the password

    # search_query = st.text_input("Enter a search query for code")
    YOUR_GITHUB_TOKEN = "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"
    queries_per_page = st.slider('Number of search results:', 0, 100, 5)
    sort = st.checkbox('Sort descendingly', value=True)

    # Search button
    if st.button("Search"):
        if search_query:
            search_github_code(search_query, YOUR_GITHUB_TOKEN, queries_per_page, sort)
        else:
            st.warning("Please enter a search query.")

if __name__ == "__main__":
    if not check_password():
        st.stop()
    main()

import os
import platform
import requests

class Update:
    """
    A class to check for updates of a GitHub repository.
    Attributes:
        releases_url (str): The URL of the GitHub releases page.
        api_url (str): The API URL for the latest release.
        app_directory (str): The directory where the application is installed.
    """

    def __init__(self, releases_url, app_directory):
        self.releases_url = releases_url.rstrip('/')
        self.api_url = f"{self.releases_url.replace('https://github.com', 'https://api.github.com/repos').replace('/releases', '')}/releases/latest"
        self.app_directory = app_directory




    def check_for_updates(self) -> tuple:
        """
        Check for updates by querying the GitHub API for the latest release.
        Returns:
            tuple: A tuple containing the latest version tag and the asset URL for the current platform.
        """
        # Check if the releases URL is valid
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            latest_release = response.json()

            # Filter assets based on the current platform
            current_platform = platform.system().lower()
            assets = latest_release.get("assets", [])
            if current_platform == "windows":
                filtered_assets = [asset for asset in assets if asset["name"].endswith(".exe")]
            elif current_platform == "darwin":
                filtered_assets = [asset for asset in assets if asset["name"].endswith(".app") or asset["name"].endswith(".dmg")]
            elif current_platform == "linux":
                filtered_assets = [asset for asset in assets if asset["name"].endswith(".tar.gz")]
            else:
                print(f"Unsupported platform: {current_platform}")
                return None, None

            if not filtered_assets:
                print(f"No compatible assets found for platform: {current_platform}")
                return None, None

            # Check if there is enough disk space for the update
            total_size = sum(asset.get("size", 0) for asset in filtered_assets)
            statvfs = os.statvfs(self.app_directory)
            free_space = statvfs.f_frsize * statvfs.f_bavail

            if total_size > free_space:
                print("Not enough disk space for the update.")
                return None, None

            return latest_release.get("tag_name"), filtered_assets[0]

        except requests.RequestException as e:
            # Handle network errors
            print(f"Error checking for updates: {e}")
            return None, None

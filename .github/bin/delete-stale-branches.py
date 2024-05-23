import os
from datetime import datetime, timedelta
from github import Github

# Authenticate with GitHub
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# Define the threshold for branch staleness
stale_threshold = datetime.utcnow() - timedelta(hours=4)

# Iterate over all branches
for branch in repo.get_branches():
    if branch.name == 'master':
        continue

    # Get the last commit on the branch
    last_commit = repo.get_commits(sha=branch.name)[0]

    # Check the date of the last commit
    if last_commit.commit.author.date < stale_threshold:
        ref = f'refs/heads/{branch.name}'
        print(f'Deleting branch: {branch.name}')
        repo.get_git_ref(ref).delete()

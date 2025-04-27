async function fetchGitHubRepos(username) {
    const response = await fetch(`https://api.github.com/users/${username}/repos`);
    const repos = await response.json();
    console.log(repos);
  }
  
  fetchGitHubRepos('octocat');  // Replace 'octocat' with your GitHub username
  
function displayRepos(repos) {
    const repoList = document.getElementById('repo-list');
    repoList.innerHTML = '';
  
    repos.forEach(repo => {
      const listItem = document.createElement('li');
      listItem.textContent = `${repo.name} ⭐ ${repo.stargazers_count}`;
      repoList.appendChild(listItem);
    });
  }
  
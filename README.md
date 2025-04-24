# Jira & GitHub Health Chat Agent

A web-based chat application that lets you query the status of your Jira tickets and GitHub pull requests through a simple conversational interface.

## Features

- Check status of specific Jira tickets
- View GitHub PR reviewers and comments
- List all open pull requests
- Find blocked Jira tickets
- Simple, intuitive chat interface

## Getting Started

### Prerequisites

- Python 3.6+
- Jira account with API access
- GitHub account with personal access token

### Installation

1. Clone the repository:

```bash
   git clone https://github.com/your-username/jira-github-health-agent.git
   cd jira-github-health-agent
  
 ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
  
   ```bash
   JIRA_API_TOKEN=your_jira_api_token
   JIRA_EMAIL=your_jira_email@example.com
   JIRA_BASE_URL=https://your-domain.atlassian.net
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_OWNER=your_github_username_or_org
   GITHUB_REPO=your_repo_name
   ```

### Running the Application

Start the Flask server:

```bash
python app.py
```

Then open your browser and navigate to http://127.0.0.1:5000/

## Usage Examples

- **Check a Jira ticket:** "What is the status of PROJ-123?"
- **Check PR reviewers:** "Who is reviewing PR #45?"
- **View PR comments:** "What are the comments on PR #45?"
- **List open PRs:** "Show me open pull requests"
- **Find blocked tickets:** "Are there any blocked tickets?"

## Development

### Project Structure

```bash

jira-github-health-agent/
├── .github/
│   └── workflows/     # GitHub Actions workflows
├── templates/         # HTML templates
│   └── index.html     # Main UI template
├── .env               # Environment variables (not tracked by git)
├── agent.py           # Jira & GitHub API interaction logic
├── app.py             # Flask application
├── darkmode.css       # Dark mode stylesheet
├── darkmode.js        # Dark mode toggle script
├── requirements.txt   # Project dependencies
└── README.md          # This file
```

## Testing

Run tests with:

```bash
pytest
```

## Deployment

This project includes GitHub Actions for CI/CD. See the `.github/workflows` directory for configuration.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your branch to your forked repository.
5. Open a Pull Request with a detailed description of your changes.

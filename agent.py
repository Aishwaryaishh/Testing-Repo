import re
import os
import requests
from typing import Dict, List, Optional, Union
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")  # e.g., https://your-domain.atlassian.net
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")  # e.g., organization or username
GITHUB_REPO = os.getenv("GITHUB_REPO")

class JiraGitHubAgent:
    def __init__(self):
        self.jira_auth = (JIRA_EMAIL, JIRA_API_TOKEN)
        self.github_headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        
    def process_query(self, query: str) -> str:
        """Process the user query and route to appropriate handler"""
        query = query.lower().strip()
        
        # Check for Jira ticket status
        jira_ticket_match = re.search(r'status of ([a-zA-Z]+-\d+)', query)
        if jira_ticket_match:
            ticket_id = jira_ticket_match.group(1).upper()
            return self.get_jira_ticket_status(ticket_id)
        
        # Check for PR reviews
        pr_review_match = re.search(r'who is reviewing (pr|pull request) #?(\d+)', query)
        if pr_review_match:
            pr_number = pr_review_match.group(2)
            return self.get_pr_reviewers(pr_number)
        
        # Check for PR comments
        pr_comments_match = re.search(r'(comments|feedback) on (pr|pull request) #?(\d+)', query)
        if pr_comments_match:
            pr_number = pr_comments_match.group(3)
            return self.get_pr_comments(pr_number)
        
        # Check for open PRs
        if "open pull requests" in query or "open prs" in query:
            return self.get_open_prs()
        
        # Check for blocked tickets
        if "blocked tickets" in query or "blocking issues" in query:
            return self.get_blocked_tickets()
        
        return "I'm not sure how to help with that query. You can ask about the status of a Jira ticket, who's reviewing a PR, comments on a PR, open PRs, or blocked tickets."
    
    def get_jira_ticket_status(self, ticket_id: str) -> str:
        """Get status information for a Jira ticket"""
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{ticket_id}"
        
        try:
            response = requests.get(url, auth=self.jira_auth)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant information
            title = data.get("fields", {}).get("summary", "No title")
            description = data.get("fields", {}).get("description", "No description")
            status = data.get("fields", {}).get("status", {}).get("name", "Unknown")
            assignee = data.get("fields", {}).get("assignee", {}).get("displayName", "Unassigned")
            
            # Truncate description if too long
            if description and len(description) > 150:
                description = description[:147] + "..."
            
            return f"Ticket: {ticket_id}\nTitle: {title}\nDescription: {description}\nStatus: {status}\nAssignee: {assignee}"
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching Jira ticket {ticket_id}: {str(e)}"
    
    def get_pr_reviewers(self, pr_number: str) -> str:
        """Get reviewers for a GitHub pull request"""
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls/{pr_number}/reviews"
        
        try:
            response = requests.get(url, headers=self.github_headers)
            response.raise_for_status()
            reviews = response.json()
            
            # Get PR details
            pr_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls/{pr_number}"
            pr_response = requests.get(pr_url, headers=self.github_headers)
            pr_response.raise_for_status()
            pr_data = pr_response.json()
            
            title = pr_data.get("title", "Unknown PR")
            
            # Process reviewers
            if not reviews:
                return f"PR #{pr_number} ({title}) has no reviews yet."
            
            reviewer_states = {}
            for review in reviews:
                reviewer = review.get("user", {}).get("login", "Unknown")
                state = review.get("state", "Unknown")
                reviewer_states[reviewer] = state
            
            result = f"PR #{pr_number} ({title}) reviews:\n"
            for reviewer, state in reviewer_states.items():
                result += f"- {reviewer}: {state}\n"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching PR #{pr_number} reviewers: {str(e)}"
    
    def get_pr_comments(self, pr_number: str) -> str:
        """Get comments on a GitHub pull request"""
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls/{pr_number}/comments"
        
        try:
            response = requests.get(url, headers=self.github_headers)
            response.raise_for_status()
            comments = response.json()
            
            # Get PR details
            pr_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls/{pr_number}"
            pr_response = requests.get(pr_url, headers=self.github_headers)
            pr_response.raise_for_status()
            pr_data = pr_response.json()
            
            title = pr_data.get("title", "Unknown PR")
            
            if not comments:
                return f"PR #{pr_number} ({title}) has no review comments yet."
            
            result = f"PR #{pr_number} ({title}) comments:\n"
            for comment in comments[:5]:  # Limit to 5 comments to avoid too long responses
                user = comment.get("user", {}).get("login", "Unknown")
                body = comment.get("body", "No content")
                # Truncate comment if too long
                if len(body) > 100:
                    body = body[:97] + "..."
                result += f"- {user}: {body}\n"
            
            if len(comments) > 5:
                result += f"... and {len(comments) - 5} more comments"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching PR #{pr_number} comments: {str(e)}"
    
    def get_open_prs(self) -> str:
        """Get list of open pull requests"""
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls?state=open"
        
        try:
            response = requests.get(url, headers=self.github_headers)
            response.raise_for_status()
            prs = response.json()
            
            if not prs:
                return "There are no open pull requests."
            
            result = f"Open Pull Requests ({len(prs)}):\n"
            for pr in prs[:10]:  # Limit to 10 PRs
                number = pr.get("number", "?")
                title = pr.get("title", "Unknown PR")
                user = pr.get("user", {}).get("login", "Unknown")
                result += f"- PR #{number} by {user}: {title}\n"
            
            if len(prs) > 10:
                result += f"... and {len(prs) - 10} more open PRs"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching open PRs: {str(e)}"
    
    def get_blocked_tickets(self) -> str:
        """Get list of blocked Jira tickets"""
        jql = "status = Blocked OR labels = blocked"
        url = f"{JIRA_BASE_URL}/rest/api/3/search"
        params = {"jql": jql, "maxResults": 10}
        
        try:
            response = requests.get(url, auth=self.jira_auth, params=params)
            response.raise_for_status()
            data = response.json()
            
            issues = data.get("issues", [])
            
            if not issues:
                return "There are no blocked tickets."
            
            result = f"Blocked Tickets ({data.get('total', 0)}):\n"
            for issue in issues:
                key = issue.get("key", "?")
                title = issue.get("fields", {}).get("summary", "Unknown ticket")
                status = issue.get("fields", {}).get("status", {}).get("name", "Unknown")
                result += f"- {key}: {title} (Status: {status})\n"
            
            if data.get("total", 0) > 10:
                result += f"... and {data.get('total') - 10} more blocked tickets"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching blocked tickets: {str(e)}"

# Example usage
def main():
    agent = JiraGitHubAgent()
    
    print("Jira & GitHub Health Chat Agent (type 'exit' to quit)")
    print("----------------------------------------------------")
    print("Example queries:")
    print("- What is the status of PROJ-123?")
    print("- Who is reviewing PR #45?")
    print("- What are the comments on PR #45?")
    print("- Show me open pull requests")
    print("- Are there any blocked tickets?")
    
    while True:
        query = input("\nYour query: ")
        if query.lower() == "exit":
            break
        
        response = agent.process_query(query)
        print("\n" + response)

if __name__ == "__main__":
    main()
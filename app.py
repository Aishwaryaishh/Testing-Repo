# app.py
from flask import Flask, render_template, request, jsonify
from agent import JiraGitHubAgent

app = Flask(__name__)
agent = JiraGitHubAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query', '')
    response = agent.process_query(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from utils import search_articles, fetch_article_content, concatenate_content, generate_answer

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        print("Received query:", user_query)

        print("Step 1: Searching articles...")
        articles = search_articles(user_query)
        if not articles:
            return jsonify({'answer': 'No relevant articles found.'}), 200

        print("Step 2: Fetching and concatenating content...")
        for article in articles:
            article['content'] = fetch_article_content(article['url'])

        full_content = concatenate_content(articles)

        print("Step 3: Generating answer...")
        answer = generate_answer(full_content, user_query)

        return jsonify({'answer': answer}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500

if __name__ == '__main__':  # Corrected the typo from '_main_' to '__main__'
    app.run(host='localhost', port=5001)

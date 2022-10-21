# install environment
`pipenv install -r requirements.txt; pipenv install -d -r requirements-dev.txt`


# start local instance
 `FLASK_APP=app.py flask run -p 8080`

# curl local instance
`curl http://127.0.0.1:8080/chat --data-urlencode "Body=My pants are one fire"`


# todos
- improve logging
- circular buffer prefix to 2048: openai.error.InvalidRequestError: This model's maximum context length is 2049 tokens, however you requested 2068 tokens (1812 in your prompt; 256 for the completion). Please reduce your prompt; or completion length.  32 question/answer pairs.
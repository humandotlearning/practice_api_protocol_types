# API Patterns

Note: for fastapi implementation you can watch the API docs at http://localhost:8000/docs
and the interactive API at http://localhost:8000/redoc

### SSE



```
uv run -m http.server 5500

uv run uvicorn sse:app --reload

# goto and check console to see SSE running: 
# http://localhost:5500/client_sse.html
```


### rest API

```
uv run uvicorn rest:app --reload


```




### WebSocket

requirements install
```
uv add "uvicorn[standard]" websockets fastapi
```

run server
```
uv run uvicorn websocket:app --reload


# in different terminal
uv run -m http.server 5500

# goto and check console to see WebSocket running: 
# http://localhost:5500/client_websocket.html
```

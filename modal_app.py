import modal

# Define the Modal app
app = modal.App("api-practice-websocket-stt")

# Define the container image with required dependencies
image = (
    modal.Image.debian_slim()
    .pip_install(
        "fastapi==0.116.1",
        "uvicorn[standard]==0.35.0",
        "websockets==15.0.1",
    )
    # Include local Python source so the container can import it
    .add_local_python_source("websocket_transcribe")
)

app_kwargs = {"image": image}


@app.function(**app_kwargs)
@modal.asgi_app(label="stt-ws")
def fastapi_app():
    # Import inside the function so it runs in the container
    from websocket_transcribe import app as fastapi_app

    return fastapi_app

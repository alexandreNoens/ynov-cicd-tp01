from fastapi import FastAPI

app = FastAPI(title="ynov-cicd-tp01")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

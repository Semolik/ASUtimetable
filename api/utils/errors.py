from fastapi.responses import JSONResponse


def ErrorMessage(message, status_code=404):
    return JSONResponse(content={"message": message}, status_code=status_code)

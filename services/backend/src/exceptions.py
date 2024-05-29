from fastapi.responses import JSONResponse


def sqlalchemy_exception_handler(_, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred.", "error": str(exc)},
    )


def sqlalchemy_integrity_error_handler(_, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Integrity error occurred.", "error": str(exc)},
    )


def sqlalchemy_data_error_handler(_, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Data error occurred.", "error": str(exc)},
    )


def sqlalchemy_database_error_handler(_, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Database error occurred.", "error": str(exc)},
    )

from fastapi import APIRouter, HTTPException

from app.face_enrollment import CSV_HEADERS, csv_template_rows, validate_identity_assignment


router = APIRouter(
    prefix="/faces/enrollment",
    tags=["Face Enrollment"],
)


@router.get("/template")
def face_enrollment_template():
    return {
        "status": "ok",
        "backend": "opencv_lbph",
        "local_only": True,
        "headers": CSV_HEADERS,
        "example_rows": csv_template_rows(),
        "privacy_note": (
            "Use only approved local reference images. Do not commit real enrollment CSVs, "
            "face images, embeddings, model files, or identity data."
        ),
    }


@router.post("/identity-assignment")
def face_identity_assignment(payload: dict):
    try:
        assignment = validate_identity_assignment(payload)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "status": "ok",
        "assignment": assignment,
        "local_only": True,
    }

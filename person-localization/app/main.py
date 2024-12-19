from fastapi import FastAPI, HTTPException
from kafka import send_to_kafka
from detect import detect_persons
import json

# Initialize FastAPI app
app = FastAPI()

@app.post("/process-image/")
async def process_image(data: dict):
    """
    Receives an image URL, processes it, detects persons, and sends the results to Kafka.
    """
    try:
        # Extract image path from request
        image_path = data.get("image_path")
        if not image_path:
            raise HTTPException(status_code=400, detail="Image path not provided")

        # Detect persons in the image
        persons = detect_persons(image_path)

        # If no persons are detected, return an error
        if not persons:
            raise HTTPException(status_code=404, detail="No persons detected in the image")

        # Send each detected person's cropped image and ID to Kafka
        for person in persons:
            message = {
                "person_id": person["id"],
                "bbox": person["bbox"],
                "image_data": person["cropped_image"].tolist()  # Convert numpy array to list for JSON serialization
            }
            send_to_kafka("person-localization-topic", message)

        return {"status": "success", "message": "Persons detected and sent to Kafka."}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

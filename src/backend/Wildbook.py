from typing import List, Tuple
import requests

base_url = "http://localhost:84"


class Wildbook:
    def __init__(self) -> None:
        pass

    # Method to check if WildBook API is properly running
    def is_running(self) -> bool:
        endpoint = f"{base_url}/api/test/helloworld/"
        response = requests.get(endpoint).json()
        response_obj = response.json()

        status = response_obj["status"]
        if status:
            return status.get("success")
        return False

    # Method to upload an image in WildBook's Database
    def upload_image(self, image_path: str) -> str:
        endpoint = f"{base_url}/api/upload/image/"
        files = {"image": open(image_path, "rb")}
        response = requests.post(endpoint, files=files)
        response_json = response.json()
        status = response_json.get("status")

        if status.get("success", None):
            image_id = response_json.get("response")
            return image_id
        else:
            return status.get("message")

    # Method to manually create WildBook annotations from a list of uploaded images
    def create_annotation(
        self, image_uuid_list: List[str], box_list: List[Tuple[int]]
    ) -> str:
        endpoint = f"{base_url}/api/annot/json/"
        annotation = {
            "image_uuid_list": image_uuid_list,
            "annot_bbox_list": box_list,
            "annot_theta_list": [0] * len(image_uuid_list),
        }

        response = requests.post(endpoint, json=annotation)

        wildbook_response = response.json()["response"][0]
        annot_uuid = wildbook_response["__UUID__"]
        return annot_uuid

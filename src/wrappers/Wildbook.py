from typing import List, Tuple
from antidote import injectable
import requests


@injectable
class Wildbook:
    def __init__(self) -> None:
        self.base_url = "http://localhost:84"

    # Method to check if WildBook API is properly running
    def is_running(self) -> bool:
        endpoint = f"{self.base_url}/api/test/helloworld/"
        response = requests.get(endpoint).json()
        response_obj = response.json()

        status = response_obj["status"]
        if status:
            return status.get("success")
        return False

    # Method to upload an image in WildBook's Database
    def upload_image(self, image_path: str) -> str:
        endpoint = f"{self.base_url}/api/upload/image/"
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
    ) -> List[str]:
        endpoint = f"{self.base_url}/api/annot/json/"
        annotation = {
            "image_uuid_list": image_uuid_list,
            "annot_bbox_list": box_list,
            "annot_theta_list": [0] * len(image_uuid_list),
        }

        response = requests.post(endpoint, json=annotation)
        response_json = response.json()

        status = response_json.get("status")
        annotation_uuids = []
        if status.get("success", None):
            uuids = response_json["response"]
            annotation_uuids = [uuid["__UUID__"] for uuid in uuids]

        return annotation_uuids

    # Method to create an annotation automatically by CNN Detection
    def detect_seal(self, image_id_list: List[str], cnn_algorithm="yolo") -> List[str]:
        endpoint = f"{self.base_url}/api/detect/{cnn_algorithm}/"
        payload = {"gid_list": image_id_list}

        response = requests.post(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")
        gid_list = []
        if status.get("success", None):
            gids = response_json["response"]
            gid_list = [gid[0] for gid in gids]

        return gid_list

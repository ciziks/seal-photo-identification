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

        if not status.get("success", None):
            return Exception(status.get("message"))

        image_id = response_json.get("response")
        return image_id

    # Method to get Image's UUID through its ID
    def list_image_ids(self):
        endpoint = f"{self.base_url}/api/image/"

        response = requests.get(endpoint)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return Exception(status.get("message"))

        return response_json["response"]

    # Method to get Image's UUID through its ID
    def get_image_uuids(self, image_id_list: List[str]) -> List[str]:
        endpoint = f"{self.base_url}/api/image/uuid/"
        payload = {"gid_list": image_id_list}

        response = requests.get(endpoint, params=payload)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return Exception(status.get("message"))

        return [uuid["__UUID__"] for uuid in response_json["response"]]

    # Method to get Image's height through its ID
    def get_image_height(self, image_id_list: List[str]):
        endpoint = f"{self.base_url}/api/image/height/"
        payload = {"gid_list": image_id_list}

        response = requests.get(endpoint, params=payload)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return Exception(status.get("message"))

        return response_json["response"]
    
    # Method to get Image's width through its ID
    def get_image_height(self, image_id_list: List[str]):
        endpoint = f"{self.base_url}/api/image/width/"
        payload = {"gid_list": image_id_list}

        response = requests.get(endpoint, params=payload)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return Exception(status.get("message"))

        return response_json["response"]

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
        if not status.get("success", None):
            return Exception(status.get("message"))

        annotation_uuids = [uuid["__UUID__"] for uuid in response_json["response"]]
        return annotation_uuids

    # Method to create an annotation automatically by CNN Detection
    def detect_seal(self, image_id_list: List[str], cnn_algorithm="yolo") -> List[str]:
        # Check if selected CNN Algorithm is valid
        valid_cnn = {"yolo", "lightnet"}
        if cnn_algorithm not in valid_cnn:
            return ValueError(f"CNN Algorithms need to be {valid_cnn}")

        endpoint = f"{self.base_url}/api/detect/{cnn_algorithm}/"
        payload = {"gid_list": image_id_list}

        response = requests.post(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return Exception(status.get("message"))

        gid_list = [gid[0] for gid in response_json["response"]]
        return gid_list

    # Method to rename the animals in Annotations
    def rename_annotations(
        self, annot_id_list: List[str], name_list: List[str]
    ) -> None:
        endpoint = f"{self.base_url}/api/annot/name/"
        payload = {"aid_list": annot_id_list, "name_list": name_list}

        response = requests.post(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return Exception(status.get("message"))

        return

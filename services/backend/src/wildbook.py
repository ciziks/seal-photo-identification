from typing import List, Optional
import requests


class Wildbook:
    def __init__(self, url: str = "http://wildbook:5000") -> None:
        self.base_url = url

    # Method to check if WildBook API is properly running
    def is_running(self) -> bool:
        endpoint = f"{self.base_url}/api/test/helloworld/"
        try:
            response = requests.get(endpoint)
            response_obj = response.json()

            status = response_obj["status"]
            return status.get("success")
        except Exception as e:
            print(e)
            return False

    # Method to upload an image in WildBook's Database
    def upload_image(self, image_path: str) -> str:
        endpoint = f"{self.base_url}/api/upload/image/"
        files = {"image": open(image_path, "rb")}
        response = requests.post(endpoint, files=files)
        response_json = response.json()
        status = response_json.get("status")

        if not status.get("success", None):
            return status.get("message")

        image_id = response_json.get("response")
        return image_id

    # Method to remove image from DB
    def remove_image(self, image_uuid_list: List[str]) -> bool:
        endpoint = f"{self.base_url}/api/image/json/"
        payload = {"image_uuid_list": image_uuid_list}

        response = requests.delete(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")

        return bool(status.get("success", None))

    # Method to get all Image's ID in DB
    def list_images_id(self):
        endpoint = f"{self.base_url}/api/image/"

        response = requests.get(endpoint)
        response_json = response.json()

        return response_json.get("response", None)

    # Method to get Image's UUID through its ID
    def get_images_uuids(self, image_id_list: List[str]) -> List[str]:
        endpoint = f"{self.base_url}/api/image/uuid/"
        payload = {"gid_list": image_id_list}

        response = requests.get(endpoint, params=payload)
        response_json = response.json()

        return [uuid["__UUID__"] for uuid in response_json.get("response", None)]

    # Method to get Image's height and width through its ID
    def get_images_size(self, image_id_list: List[str]):
        endpoint_height = f"{self.base_url}/api/image/height/"
        endpoint_width = f"{self.base_url}/api/image/width/"
        payload = {"gid_list": ",".join(map(str, image_id_list))}

        response_height = requests.get(endpoint_height, data=payload)
        response_height_json = response_height.json()
        response_width = requests.get(endpoint_width, params=payload)
        response_width_json = response_width.json()

        status_height = not response_height_json.get("status", None)
        status_width = not response_width_json.get("status", None)

        if status_height or status_width:
            return []

        return list(
            zip(
                response_width_json.get("response"),
                response_height_json.get("response"),
            )
        )

    # Method to manually create WildBook annotation
    def create_annotations(
        self,
        image_id_list: List[str],
        box_list: List[List[str]],
        name_list: Optional[List[str]] = None,
    ) -> List[str]:
        endpoint = f"{self.base_url}/api/annot/"
        annotation = {
            "gid_list": image_id_list,
            "bbox_list": box_list,
            "theta_list": [0] * len(image_id_list),
        }

        if name_list:
            annotation["name_list"] = name_list

        response = requests.post(endpoint, json=annotation)
        response_json = response.json()

        status = response_json.get("status")
        if not status.get("success", None):
            return []

        annotation_ids = response_json["response"]

        return annotation_ids

    # Method to get Annotation ID through its UUID
    def get_annotation_id(self, uuid_list: List[str]):
        endpoint = f"{self.base_url}/api/annot/rowid/uuid"
        payload = {"uuid_list": uuid_list}

        response = requests.get(endpoint, json=payload)
        response_json = response.json()

        return response_json.get("response", None)

    # Method to list names
    def list_names_id(self):
        endpoint = f"{self.base_url}/api/name/"

        response = requests.get(endpoint)
        response_json = response.json()

        return response_json.get("response", None)

    # Method to list Annotations for each Name
    def list_annotation_from_names(self, names_list: List[str]):
        endpoint = f"{self.base_url}/api/name/annot/rowid/"

        response = requests.get(endpoint, json={"nid_list": names_list})
        response_json = response.json()

        annotations_id = []
        for aid in response_json.get("response", None):
            if aid:

                annotations_id.append(int(aid[-1]))

        return annotations_id

    # Method to list Annotation ID
    def list_annotations_id(self):
        endpoint = f"{self.base_url}/api/annot/json/"

        response = requests.get(endpoint)
        response_json = response.json()

        annotations_uuid = [
            uuid["__UUID__"] for uuid in response_json.get("response", None)
        ]

        annotations_id = self.get_annotation_id(annotations_uuid)

        return annotations_id

    # Method to return Annotation's Name
    def get_annotation_name(self, annot_id: str):
        endpoint = f"{self.base_url}/api/annot/name/text/"
        payload = {"aid_list": [annot_id]}

        response = requests.get(endpoint, json=payload)
        response_json = response.json()

        seal_name: str = response_json["response"][0]

        return seal_name

    # Method to return Annotation's Image URL
    def get_annotation_image(self, annot_id: str):
        endpoint = f"{self.base_url}/api/annot/{annot_id}/"

        response = requests.get(endpoint)
        response_json = response.json()

        image_url = response_json["response"]

        return image_url

    # Method to create an annotation automatically by CNN Detection
    def detect_seal(self, image_id_list: List[int], cnn_algorithm="yolo") -> List[str]:
        # Check if selected CNN Algorithm is valid
        valid_cnn = {"yolo", "lightnet"}
        if cnn_algorithm not in valid_cnn:
            raise ValueError(f"CNN Algorithms need to be {valid_cnn}")

        endpoint = f"{self.base_url}/api/detect/cnn/yolo/"
        payload = {"gid_list": image_id_list}

        response = requests.put(endpoint, json=payload)
        response_json = response.json()

        return response_json.get("response")[0] if response_json.get("response") else []

    # Method to rename the animals in Annotations
    def rename_annotations(
        self, annot_id_list: List[str], name_list: List[str]
    ) -> bool:
        endpoint = f"{self.base_url}/api/annot/name/"
        payload = {"aid_list": annot_id_list, "name_list": name_list}

        response = requests.put(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")

        return bool(status.get("success", None))


    # Method to mark annotation as Exemplar
    def mark_as_exemplar(self, annot_id_list: List[str]) -> bool:
        endpoint = f"{self.base_url}/api/annot/exemplar/"
        payload = {"aid_list": annot_id_list, "flag_list": [1] * len(annot_id_list)}

        response = requests.put(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")

        return bool(status.get("success", None))

    # Method to remove Annotation from database
    def remove_annotation(self, annot_uuid_list: List[str]) -> bool:
        endpoint = f"{self.base_url}/api/image/json/"
        payload = {"annot_uuid_list": annot_uuid_list}

        response = requests.delete(endpoint, json=payload)
        response_json = response.json()

        status = response_json.get("status")
        return bool(status.get("success", None))

    # Method to perform seal matching with specific annotations
    def seal_matching(
        self, annotation_ids: List[str], comparison_list: List[str]
    ) -> dict:
        endpoint = f"{self.base_url}/api/query/chip/dict/simple"

        payload = {"qaid_list": comparison_list, "daid_list": annotation_ids}

        response = requests.get(endpoint, json=payload)
        response_json = response.json()

        comparison_scores = {annotation: {} for annotation in annotation_ids}
        for comparison in response_json["response"]:
            compared_aid = comparison["qaid"]
            scores = comparison["score_list"] if comparison["score_list"] else 1

            for index, annotation in enumerate(annotation_ids):
                comparison_scores[annotation][
                    self.get_annotation_name(compared_aid)
                ] = {
                    "score": scores[index],
                    "image": self.get_annotation_image(compared_aid),
                }

        for annotation_key in comparison_scores:
            # Sort comparisons by score
            sorted_scores = sorted(
                comparison_scores[annotation_key].items(),
                key=lambda item: item[1]["score"],
                reverse=True,
            )[:5]
            comparison_scores[annotation_key] = dict(sorted_scores)

        return comparison_scores

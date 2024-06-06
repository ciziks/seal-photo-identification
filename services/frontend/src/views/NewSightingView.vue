<template>
  <div class="new-sighting-view">
    <loading-screen :isLoading="isLoading" />
    <h1>New Sighting</h1>
    <div v-if="!showCroppedImages">
      <form @submit.prevent="prepareCroppedImagesStep">
        <div>
          <label for="date">Date:</label>
          <input type="date" v-model="date" id="date" required />
        </div>
        <div>
          <label for="location">Location:</label>
          <select v-model="location" id="location" required>
            <option value="field">Field</option>
            <option value="centre">Centre</option>
          </select>
        </div>
        <div
          class="drop-area"
          @dragover.prevent
          @drop="handleDrop"
          @click="triggerFileInput"
          style="border: 2px dashed #0077be; padding: 20px; text-align: center; margin-top: 20px;"
        >
          Drop files here or click to upload
        </div>
        <input type="file" @change="handleFileChange" ref="fileInput" style="display: none;" multiple />
      </form>

      <div v-if="files.length" style="margin-top: 20px;">
        <h2>Selected Images</h2>
        <ul>
          <li v-for="(file, index) in files" :key="index">{{ file.name }}</li>
        </ul>
      </div>

      <div v-if="currentImageSrc" style="margin-top: 20px;">
        <h2>Crop Image</h2>
        <vue-cropper
          ref="cropper"
          :src="currentImageSrc"
          alt="Seal to be cropped"
          :view-mode="1"
          :guides="true"
          :aspect-ratio="NaN"
          style="margin-top: 20px;"
        />
        <button @click="getCroppedImage" :disabled="isCropping">Crop Image</button>
        <button v-if="currentIndex < files.length - 1" @click="nextImage" :disabled="!isCropped">Next Image</button>
        <button v-else @click="prepareCroppedImagesStep" :disabled="!isCropped">Add Sighting</button>
      </div>

      <div v-if="croppedImages.length" style="margin-top: 20px;">
        <h2>Cropped Images</h2>
        <div v-for="(imageGroup, index) in croppedImages" :key="index">
          <h3>Images from file {{ index + 1 }}</h3>
          <div class="cropped-images-container">
            <div v-for="(image, imgIndex) in imageGroup" :key="imgIndex" class="preview">
              <img :src="image" :alt="'Cropped Seal ' + imgIndex" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="cropped-images-step">
      <h2>Process Cropped Images</h2>
      <div v-if="croppedImages[currentCroppedImageIndex]">
        <img class="cropped-image" :src="croppedImages[currentCroppedImageIndex][currentSubImageIndex]" :alt="'Cropped Seal ' + currentSubImageIndex" />
        <div class="buttons">
          <button @click="detectImage">Detect</button>
          <button v-if="!isLastImage" @click="skipImage">Skip</button>
        </div>
        <div v-if="detectionResults.length" class="detection-results">
          <h3>Detection Results</h3>
          <div v-for="(result, index) in detectionResults" :key="index" class="result">
            <p>Seal ID: {{ result.id }}</p>
            <p>Score: {{ result.score }}</p>
            <img
              :src="result.image"
              :alt="'Detected Seal ' + index"
              class="detected-image"
              @click="openModal(result.image, croppedImages[currentCroppedImageIndex][currentSubImageIndex])"
            />
            <button @click="createEncounter(result.id)">Select</button>
          </div>
          <button @click="openNewSealModal">New Seal</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-if="success" class="success-message">
      Sighting and encounter added successfully!
    </div>

    <!-- New Seal Modal -->
    <div v-if="showNewSealModal" class="modal">
      <div class="modal-content">
        <span class="close-button" @click="closeNewSealModal">&times;</span>
        <h2>Add New Seal</h2>
        <form @submit.prevent="submitNewSeal">
          <div class="form-group">
            <label for="newSealID">ID/Name</label>
            <input v-model="newSeal.ID" type="text" id="newSealID" required />
          </div>
          <div class="form-group">
            <label for="newSealAge">Age</label>
            <input v-model="newSeal.age" type="text" id="newSealAge" required />
          </div>
          <div class="form-group">
            <label for="newSealComments">Comments</label>
            <textarea v-model="newSeal.comments" id="newSealComments"></textarea>
          </div>
          <div class="form-group">
            <label for="newSealGender">Gender</label>
            <select v-model="newSeal.gender" id="newSealGender">
              <option value="">Select Gender</option>
              <option value="m">Male</option>
              <option value="f">Female</option>
              <option value="u">Unknown</option>
            </select>
          </div>
          <div class="form-group">
            <label for="newSealIsPregnant">Is Pregnant</label>
            <select v-model="newSeal.isPregnant" id="newSealIsPregnant">
              <option value="">Select Option</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="Unknown">Unknown</option>
            </select>
          </div>
          <button type="submit">Add Seal</button>
        </form>
        <div v-if="newSealError" class="error-message">
          {{ newSealError }}
        </div>
        <div v-if="newSealSuccess" class="success-message">
          Seal added successfully!
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close-button" @click="closeModal">&times;</span>
        <div class="modal-images">
          <div class="modal-image-container">
            <img :src="currentImage.left" :alt="'Initial Cropped Seal ' + currentImage.left" class="modal-image" />
          </div>
          <div class="modal-image-container">
            <img :src="currentImage.right" :alt="'Detected Seal ' + currentImage.right" class="modal-image" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import axios from 'axios';
import LoadingScreen from '@/components/LoadingScreen.vue';

export default {
  components: {
    VueCropper,
    LoadingScreen,
  },
  data() {
    return {
      date: '',
      location: 'field', // default value
      files: [],
      croppedImages: [], // Array of arrays to hold multiple crops per file
      currentImageSrc: null,
      isCropping: false,
      isCropped: false,
      currentIndex: 0,
      sightingId: null,
      error: null,
      success: false,
      showCroppedImages: false,
      currentCroppedImageIndex: 0,
      currentSubImageIndex: 0,
      detectionResults: [], // Array to hold detection results
      currentWildbookId: null, // Store the current wildbook_id from detection
      showNewSealModal: false, // Show/Hide New Seal Modal
      newSeal: {
        ID: '',
        age: '',
        comments: '',
        gender: '',
        isPregnant: '',
      },
      newSealError: null,
      newSealSuccess: false,
      showModal: false,
      currentImage: null,
      isLoading: false, // For loading screen
    };
  },
  computed: {
    isLastImage() {
      return (
        this.currentCroppedImageIndex === this.croppedImages.length - 1 &&
        this.currentSubImageIndex === this.croppedImages[this.currentCroppedImageIndex].length - 1
      );
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      this.files = Array.from(event.target.files);
      this.croppedImages = Array(this.files.length).fill(null).map(() => []); // Initialize with empty arrays
      this.currentIndex = 0;
      this.isCropped = false;
      this.setCurrentImage();
    },
    handleDrop(event) {
      this.files = Array.from(event.dataTransfer.files);
      this.croppedImages = Array(this.files.length).fill(null).map(() => []); // Initialize with empty arrays
      this.currentIndex = 0;
      this.isCropped = false;
      this.setCurrentImage();
    },
    setCurrentImage() {
      if (this.files.length > 0 && this.currentIndex < this.files.length) {
        const file = this.files[this.currentIndex];
        this.currentImageSrc = URL.createObjectURL(file);
      } else {
        this.currentImageSrc = null;
      }
    },
    getCroppedImage() {
      this.isCropping = true;
      const canvas = this.$refs.cropper.getCroppedCanvas();
      canvas.toBlob((blob) => {
        const croppedImageUrl = URL.createObjectURL(blob);
        this.croppedImages[this.currentIndex].push(croppedImageUrl); // Add cropped image to current file's array
        this.isCropping = false;
        this.isCropped = true; // Enable the next button after cropping
      });
    },
    nextImage() {
      if (this.currentIndex < this.files.length - 1) {
        this.currentIndex++;
        this.isCropped = false; // Disable the next button until the next image is cropped
        this.currentImageSrc = null; // Clear current image to force re-render
        this.$nextTick(() => {
          this.setCurrentImage(); // Set next image after clearing the current one
        });
      }
    },
    async prepareCroppedImagesStep() {
      try {
        this.isLoading = true;
        this.error = null;
        this.success = false;

        const dateParts = this.date.split('-');
        const formattedDate = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
        const sightingData = {
          Date: formattedDate,
          Location: this.location,
        };

        console.log('Sending sighting data:', sightingData);
        const response = await axios.post('http://localhost:5001/sightings', sightingData);
        this.sightingId = response.data.SightingID;
        console.log('Sighting added:', response.data);

        this.showCroppedImagesStep();
      } catch (error) {
        this.error = error.response?.data?.detail || error.message;
      } finally {
        this.isLoading = false;
      }
    },
    showCroppedImagesStep() {
      this.showCroppedImages = true;
    },
    async detectImage() {
      try {
        this.isLoading = true;
        this.error = null;
        this.success = false;

        const croppedImageUrl = this.croppedImages[this.currentCroppedImageIndex][this.currentSubImageIndex];
        const response = await fetch(croppedImageUrl);
        const blob = await response.blob();
        const formData = new FormData();
        formData.append('images', blob, 'cropped_image.png');
        
        const detectResponse = await axios.post('http://localhost:5001/detect', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const scores = detectResponse.data;
        this.currentWildbookId = Object.keys(scores)[0]; // Store the first wildbook_id
        this.detectionResults = Object.entries(scores[this.currentWildbookId]).map(([key, value]) => ({
          id: key,
          score: value.score,
          image: value.image,
        }));

        console.log('Detection results:', this.detectionResults);

      } catch (error) {
        this.error = error.response?.data?.detail || error.message;
      } finally {
        this.isLoading = false;
      }
    },
    async createEncounter(sealId) {
      try {
        const encounterData = {
          SightingID: this.sightingId,
          SealID: sealId,
          WildBookID: this.currentWildbookId,
        };

        const response = await axios.post('http://localhost:5001/encounters', encounterData);
        console.log('Encounter created:', response.data);

        this.success = true;
      } catch (error) {
        this.error = error.response?.data?.detail || error.message;
      }
    },
    skipImage() {
      this.nextCroppedImage();
    },
    nextCroppedImage() {
      if (this.currentSubImageIndex < this.croppedImages[this.currentCroppedImageIndex].length - 1) {
        this.currentSubImageIndex++;
      } else if (this.currentCroppedImageIndex < this.croppedImages.length - 1) {
        this.currentCroppedImageIndex++;
        this.currentSubImageIndex = 0;
      } else {
        this.success = true; // All images processed
      }
      // Reset data for a new detection operation
      this.detectionResults = [];
      this.currentWildbookId = null;
    },
    openNewSealModal() {
      this.showNewSealModal = true;
    },
    closeNewSealModal() {
      this.showNewSealModal = false;
    },
    async submitNewSeal() {
      try {
        this.newSealError = null;
        this.newSealSuccess = false;

        const response = await axios.post('http://localhost:5001/seals', this.newSeal);
        console.log('New seal added:', response.data);

        const newSealId = response.data.ID;
        await this.createEncounter(newSealId);

        this.newSealSuccess = true;
        this.closeNewSealModal();
      } catch (error) {
        this.newSealError = error.response?.data?.detail || error.message;
      }
    },
    openModal(detectedImage, croppedImage) {
      this.currentImage = {
        left: croppedImage,
        right: detectedImage,
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.currentImage = null;
    },
  },
};
</script>

<style scoped>
.new-sighting-view form {
  margin-bottom: 20px;
}

.new-sighting-view .drop-area {
  cursor: pointer;
}

.new-sighting-view ul {
  list-style-type: none;
  padding: 0;
}

.new-sighting-view li {
  margin: 5px 0;
}

.cropped-images-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.preview img {
  max-width: 200px;
  max-height: 150px;
  object-fit: contain;
  border: 1px solid #ccc;
}

.cropped-images-step {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cropped-image {
  width: 300px;
  height: 300px;
  object-fit: contain;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  gap: 10px;
}

.buttons button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.buttons button:hover {
  background-color: #0056b3;
}

.detection-results {
  margin-top: 20px;
}

.result {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  text-align: center;
}

.detected-image {
  max-width: 100px;
  max-height: 100px;
  margin-top: 10px;
  cursor: pointer;
}

.error-message {
  color: red;
  margin-top: 20px;
}

.success-message {
  color: green;
  margin-top: 20px;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
}

.modal-content {
  position: relative;
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  max-width: 80%;
  max-height: 80%;
  text-align: center;
}

.modal-images {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-image-container {
  flex: 1;
  margin: 0 10px;
}

.modal-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 2em;
  cursor: pointer;
}

form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

label {
  margin: 10px 0 5px;
}

input[type="text"],
textarea,
select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

.data {
  color: #333;
}

.no-data {
  color: #888;
  font-style: italic;
}
</style>

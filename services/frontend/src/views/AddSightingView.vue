<template>
  <div class="add-sighting-view">
    <h1>Add Sighting</h1>
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
          alt="Source Image"
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
              <img :src="image" :alt="'Cropped Image ' + imgIndex" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="cropped-images-step">
      <h2>Process Cropped Images</h2>
      <div v-if="croppedImages[currentCroppedImageIndex]">
        <img class="cropped-image" :src="croppedImages[currentCroppedImageIndex][currentSubImageIndex]" alt="Cropped Image" />
        <div class="buttons">
          <button @click="detectImage">Detect</button>
          <button v-if="!isLastImage" @click="skipImage">Skip</button>
        </div>
        <div v-if="detectionResults.length" class="detection-results">
          <h3>Detection Results</h3>
          <div v-for="(result, index) in detectionResults" :key="index" class="result">
            <p>Seal ID: {{ result.id }}</p>
            <p>Score: {{ result.score }}</p>
            <img :src="result.image" :alt="'Detected Image ' + index" class="detected-image"/>
            <button @click="createEncounter(result.id)">Select</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-if="success" class="success-message">
      Sighting and encounter added successfully!
    </div>
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import axios from 'axios';

export default {
  components: {
    VueCropper,
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
      }
    },
    showCroppedImagesStep() {
      this.showCroppedImages = true;
    },
    async detectImage() {
      try {
        this.error = null;
        this.success = false;

        const croppedImageUrl = this.croppedImages[this.currentCroppedImageIndex][this.currentSubImageIndex];
        const response = await fetch(croppedImageUrl);
        const blob = await response.blob();
        const formData = new FormData();
        formData.append('image', blob, 'cropped_image.png');

        const detectResponse = await axios.post('http://localhost:5001/detect', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const scores = detectResponse.data;
        this.currentWildbookId = scores.wildbook_id; // Store the wildbook_id
        this.detectionResults = Object.keys(scores).slice(1).map(key => ({
          id: key,
          score: scores[key].score,
          image: scores[key].image,
        }));

        console.log('Detection results:', this.detectionResults);

      } catch (error) {
        this.error = error.response?.data?.detail || error.message;
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
  },
};
</script>

<style scoped>
.add-sighting-view form {
  margin-bottom: 20px;
}

.add-sighting-view .drop-area {
  cursor: pointer;
}

.add-sighting-view ul {
  list-style-type: none;
  padding: 0;
}

.add-sighting-view li {
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
}

.error-message {
  color: red;
  margin-top: 20px;
}

.success-message {
  color: green;
  margin-top: 20px;
}
</style>

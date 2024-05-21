<template>
    <div class="add-sighting-view">
      <h1>Add Sighting</h1>
      <form @submit.prevent="addSighting">
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
          style="border: 2px dashed #0077be; padding: 20px; text-align: center; margin-top: 20px;">
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
        <button v-else @click="addSighting" :disabled="!isCropped">Add Sighting</button>
      </div>
  
      <div v-if="croppedImages.length" style="margin-top: 20px;">
        <h2>Cropped Images</h2>
        <div v-for="(image, index) in croppedImages" :key="index" class="preview">
          <img :src="image" :alt="'Cropped Image ' + index" />
        </div>
      </div>
  
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        Sighting added successfully!
      </div>
    </div>
  </template>
  
  <script>
  import VueCropper from 'vue-cropperjs';
  import 'cropperjs/dist/cropper.css';
  import axios from 'axios';
  
  export default {
    components: {
      VueCropper
    },
    data() {
      return {
        date: '',
        location: 'field', // default value
        files: [],
        croppedImages: [],
        currentImageSrc: null,
        isCropping: false,
        isCropped: false,
        currentIndex: 0,
        sightingId: null,
        error: null,
        success: false
      };
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      handleFileChange(event) {
        this.files = Array.from(event.target.files);
        this.croppedImages = Array(this.files.length).fill(null);
        this.currentIndex = 0;
        this.isCropped = false;
        this.setCurrentImage();
      },
      handleDrop(event) {
        this.files = Array.from(event.dataTransfer.files);
        this.croppedImages = Array(this.files.length).fill(null);
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
        canvas.toBlob(blob => {
          const croppedImageUrl = URL.createObjectURL(blob);
          this.croppedImages.splice(this.currentIndex, 1, croppedImageUrl); // Directly update the array
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
      async addSighting() {
        try {
          this.error = null;
          this.success = false;
  
          const dateParts = this.date.split('-');
          const formattedDate = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
          const sightingData = {
            Date: formattedDate,
            Location: this.location
          };
          
          console.log('Sending sighting data:', sightingData);
          const response = await axios.post('/sightings', sightingData);
          this.sightingId = response.data.SightingID;
          console.log('Sighting added:', response.data);
          
          this.success = true;
          // Optionally reset form fields after success
          this.date = '';
          this.location = 'field';
          this.files = [];
          this.croppedImages = [];
          this.currentImageSrc = null;
          this.isCropping = false;
          this.isCropped = false;
          this.currentIndex = 0;
        } catch (error) {
          this.error = error.response?.data?.detail || error.message;
        }
      }
    }
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
  
  .preview img {
    max-width: 200px;
    max-height: 150px;
    object-fit: contain;
    border: 1px solid #ccc;
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
  
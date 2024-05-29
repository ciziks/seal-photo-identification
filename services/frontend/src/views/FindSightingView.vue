<template>
  <div class="find-sighting-view">
    <h1>Find Sighting</h1>
    <div class="input-container">
      <form @submit.prevent="fetchSighting">
        <div>
          <label for="date">Date:</label>
          <input type="date" v-model="sightingDate" id="date" required />
        </div>
        <div>
          <label for="location">Location:</label>
          <select v-model="sightingLocation" id="location" required>
            <option value="" disabled>Select Location</option>
            <option value="field">Field</option>
            <option value="centre">Centre</option>
          </select>
        </div>
        <button type="submit">Find Sighting</button>
      </form>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <div v-if="sighting">
      <h2>Sighting Information</h2>
      <p>Date: {{ sighting.Date }}</p>
      <p>Location: {{ sighting.Location }}</p>
      <div v-for="(encounter, index) in uniqueEncounters" :key="index" class="seal">
        <div class="seal-header">
          <h2 @click="goToSealDetails(encounter.SealID)" class="seal-name">{{ encounter.SealID }}</h2>
          <button v-if="getEncounterImages(index).length > 3" @click="nextImages(index)" class="next-button">
            <img src="@/assets/images/right_arrow.png" />
          </button>
        </div>
        <div class="seal-images">
          <img
            v-for="(image, imgIndex) in getCurrentImages(index)"
            :key="imgIndex"
            :src="image"
            :alt="`Image of ${encounter.SealID}`"
            @click="openModal(image)"
          />
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close-button" @click="closeModal">&times;</span>
        <img :src="currentImage" alt="Seal Image" class="modal-image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';

export default {
  data() {
    return {
      sightingDate: '',
      sightingLocation: '',
      sighting: null,
      seal: null,
      imageIndices: {}, // Track current index for each encounter
      errorMessage: '',
      uniqueEncounters: [],
      showModal: false,
      currentImage: null,
    };
  },
  setup() {
    const isLoading = inject('isLoading');
    const setLoading = inject('setLoading');
    return { isLoading, setLoading };
  },
  methods: {
    async fetchSighting() {
      try {
        this.setLoading(true);
        const formattedDate = this.sightingDate.split('-').reverse().join('-'); // Convert date to dd-mm-yyyy format
        const response = await axios.get('http://localhost:5001/sightings/search/', {
          params: {
            date: formattedDate,
            location: this.sightingLocation,
          },
        });
        this.sighting = response.data[0]; // Assume the first result for now
        this.imageIndices = {}; // Reset image indices

        // Filter out duplicate encounters based on SealID
        const encounteredSeals = new Set();
        this.uniqueEncounters = this.sighting.encounters.filter(encounter => {
          if (!encounteredSeals.has(encounter.SealID)) {
            encounteredSeals.add(encounter.SealID);
            return true;
          }
          return false;
        });

        // Initialize imageIndices for each unique encounter
        this.uniqueEncounters.forEach((_, index) => {
          this.imageIndices[index] = 0;
        });

        this.errorMessage = ''; // Clear error message if successful
      } catch (error) {
        this.errorMessage = 'Sighting not found';
      } finally {
        this.setLoading(false);
      }
    },
    getEncounterImages(index) {
      const encounter = this.uniqueEncounters[index];
      const images = this.sighting.images;
      return images.filter((image, imgIndex) => this.sighting.encounters[imgIndex].SealID === encounter.SealID);
    },
    getCurrentImages(index) {
      const images = this.getEncounterImages(index);
      return images.slice(this.imageIndices[index], this.imageIndices[index] + 3);
    },
    nextImages(index) {
      const images = this.getEncounterImages(index);
      let nextIndex = this.imageIndices[index] + 3;
      if (nextIndex >= images.length) {
        nextIndex = 0; // Reset to the first three images if we reach the end
      }
      this.imageIndices[index] = nextIndex;
    },
    goToSealDetails(sealId) {
      this.$router.push({ name: 'SealDetails', params: { sealId } });
    },
    openModal(image) {
      this.currentImage = image;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.currentImage = null;
    },
  },
};
</script>

<style>
.find-sighting-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
  box-sizing: border-box; /* Ensure padding is included in element's total width and height */
}

h1 {
  margin-bottom: 20px;
  font-size: 2em;
  color: #333;
}

.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

input,
select {
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-bottom: 20px;
}

.seal {
  width: 100%; /* Full width of the container to use maximum space */
  border: 1px solid #ccc;
  margin: 20px 0; /* Vertical margin for separation */
  padding: 20px;
  box-sizing: border-box; /* Padding and border included in width calculation */
}

.seal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.seal-name {
  cursor: pointer;
  color: #007bff;
}

.seal-name:hover {
  text-decoration: underline;
}

.seal-images {
  display: flex;
  align-items: center;
  overflow-x: auto; /* Enables horizontal scrolling */
  width: 100%;
  margin-top: 10px; /* Space above the image row */
  padding-right: 20px; /* Right padding to ensure no image is cut off */
}

.seal-images img {
  height: 150px; /* Fixed height for all images */
  width: auto; /* Width auto to maintain aspect ratio */
  flex: 0 0 auto; /* Do not grow or shrink, use image's native size */
  object-fit: contain; /* Ensure full image is visible */
  margin-right: 10px; /* Space between images */
  cursor: pointer;
}

.next-button {
  background: none;
  border: none;
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

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 2em;
  cursor: pointer;
}

.modal-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}
</style>

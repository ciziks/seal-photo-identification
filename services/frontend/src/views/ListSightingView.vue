<template>
  <div class="list-sighting-view">
    <h1>List Sighting</h1>
    <div class="input-container">
      <input v-model="sightingId" placeholder="Enter Sighting ID" />
      <button @click="fetchSighting">Get Sighting</button>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <div v-if="sighting">
      <h2>Sighting Information</h2>
      <p>Date: {{ sighting.Date }}</p>
      <p>Location: {{ sighting.Location }}</p>
      <div v-for="(encounter, index) in uniqueEncounters" :key="index" class="seal">
        <div class="seal-header">
          <h2 @click="fetchSeal(encounter.SealID)">{{ encounter.SealID }}</h2>
          <button v-if="getEncounterImages(index).length > 3" @click="nextImages(index)" class="next-button">
            <img src="@/assets/images/right_arrow.png" />
          </button>
        </div>
        <div class="seal-images">
          <img v-for="(image, imgIndex) in getCurrentImages(index)" :key="imgIndex" :src="image" :alt="`Image of ${encounter.SealID}`" />
        </div>
      </div>
    </div>

    <div v-if="seal">
      <h2>Seal Information</h2>
      <p>ID: {{ seal.ID }}</p>
      <p>Age: {{ seal.age }}</p>
      <p>Gender: {{ seal.gender }}</p>
      <p v-if="seal.comments">Comments: {{ seal.comments }}</p>
      <p v-if="seal.isPregnant">Pregnant: {{ seal.isPregnant }}</p>
      <div class="seal-images">
        <img v-for="(image, index) in seal.images" :key="index" :src="image" alt="Seal Image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sightingId: '',
      sighting: null,
      seal: null,
      imageIndices: {}, // Track current index for each encounter
      errorMessage: '',
      uniqueEncounters: [],
    };
  },
  methods: {
    async fetchSighting() {
      try {
        const response = await axios.get(`http://localhost:5001/sightings/${this.sightingId}`);
        this.sighting = response.data;
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
    async fetchSeal(sealId) {
      try {
        const response = await axios.get(`http://localhost:5001/seals/${sealId}`);
        this.seal = response.data;
      } catch (error) {
        alert('Seal not found');
      }
    },
  },
};
</script>

<style>
.list-sighting-view {
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
  align-items: center;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
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
  cursor: pointer;
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
}

.next-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.next-button img {
  width: 50px; /* Adjust size as necessary */
  height: 50px;
}
</style>

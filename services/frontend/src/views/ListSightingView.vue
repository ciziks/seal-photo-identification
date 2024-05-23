<template>
  <div class="list-sighting-view">
    <h1>List Sighting</h1>
    <form @submit.prevent="fetchSighting">
      <div>
        <label for="sightingId">Sighting ID:</label>
        <input type="number" v-model="sightingId" id="sightingId" required />
      </div>
      <button type="submit">Get Sighting</button>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="sighting" class="sighting-details">
      <h2>Sighting Details</h2>
      <p><strong>ID:</strong> {{ sighting.SightingID }}</p>
      <p><strong>Date:</strong> {{ sighting.Date }}</p>
      <p><strong>Location:</strong> {{ sighting.Location }}</p>

      <div class="sighting-images">
        <img v-for="(image, index) in getCurrentImages()" :key="index" :src="image" alt="Sighting Image" />
      </div>
      <button v-if="sighting.images.length > 3" @click="nextImages" class="next-button">
        <img src="../assets/images/right_arrow.png" />
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sightingId: null,
      sighting: null,
      error: null,
      imageIndex: 0 // Track current index for sighting images
    };
  },
  methods: {
    async fetchSighting() {
      try {
        this.error = null;
        this.sighting = null;
        this.imageIndex = 0;

        const response = await axios.get(`http://localhost:5001/sightings/${this.sightingId}`);
        this.sighting = response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || error.message;
      }
    },
    getCurrentImages() {
      if (!this.sighting || !this.sighting.images) return [];
      return this.sighting.images.slice(this.imageIndex, this.imageIndex + 3);
    },
    nextImages() {
      this.imageIndex += 3;
      if (this.imageIndex >= this.sighting.images.length) {
        this.imageIndex = 0; // Reset to the first three images if we reach the end
      }
    }
  }
};
</script>

<style scoped>
.list-sighting-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

form {
  margin-bottom: 20px;
}

.error-message {
  color: red;
  margin-top: 20px;
}

.sighting-details {
  margin-top: 20px;
}

.sighting-images {
  display: flex;
  align-items: center;
  overflow-x: auto; /* Enables horizontal scrolling */
  width: 100%;
  margin-top: 10px; /* Space above the image row */
  padding-right: 20px; /* Right padding to ensure no image is cut off */
}

.sighting-images img {
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
  width: 125px; /* Adjust size as necessary */
  height: 125px;
}
</style>

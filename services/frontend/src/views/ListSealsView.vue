<template>
  <div class="list-seals-view">
    <div v-for="(images, name) in seals" :key="name" class="seal">
      <div class="seal-header">
        <h2>{{ name }}</h2>
        <button v-if="images.length > 3" @click="nextImages(name)" class="next-button">
          <img src="@/assets/images/right_arrow.png" />
        </button>
      </div>
      <div class="seal-images">
        <img v-for="(image, index) in getCurrentImages(name)" :key="index" :src="image" alt="Seal" />
      </div>
    </div>
    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      seals: {}, // Store all seals data from the backend
      imageIndices: {}, // Track current index for each seal
      totalSeals: 0,
      limit: 10,
      currentPage: 1,
      totalPages: 0
    };
  },
  mounted() {
    this.fetchSeals();
  },
  methods: {
    fetchSeals() {
      const offset = (this.currentPage - 1) * this.limit;
      axios.get(`http://localhost:5001/seals?limit=${this.limit}&offset=${offset}`)
        .then(response => {
          this.seals = response.data.data;
          this.totalSeals = response.data.total;
          this.totalPages = Math.ceil(this.totalSeals / this.limit);
          for (let name in this.seals) {
            this.imageIndices[name] = 0;  // Initialize index for each seal
          }
        })
        .catch(error => {
          console.error('Error fetching seals:', error);
        });
    },
    getCurrentImages(name) {
      const images = this.seals[name];
      return Array.isArray(images) ? images.slice(this.imageIndices[name], this.imageIndices[name] + 3) : [];
    },
    nextImages(name) {
      let nextIndex = this.imageIndices[name] + 3;
      if (nextIndex >= this.seals[name].length) {
        nextIndex = 0;  // Reset to the first three images if we reach the end
      }
      this.imageIndices[name] = nextIndex;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchSeals();
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchSeals();
      }
    }
  }
};
</script>

<style>
.list-seals-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 10px; /* Additional padding to ensure space around the items */
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
  width: 125px; /* Adjust size as necessary */
  height: 125px;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-controls button {
  margin: 0 10px;
  padding: 5px 10px;
}
</style>

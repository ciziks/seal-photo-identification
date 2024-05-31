<template>
  <div class="list-seals-view">
    <loading-screen :isLoading="isLoading" />
    <div v-for="(images, name) in seals" :key="name" class="seal">
      <div class="seal-header">
        <h2 @click="goToSealDetails(name)" class="seal-name">{{ name }}</h2>
        <button v-if="images.length > 3" @click="nextImages(name)" class="next-button">
          <img src="@/assets/images/right_arrow.png" alt="Next images arrow"/>
        </button>
      </div>
      <div class="seal-images">
        <img
          v-for="(image, index) in getCurrentImages(name)"
          :key="index"
          :src="image"
          :alt="`Seal ${name}`"
          @click="openModal(image)"
        />
      </div>
    </div>
    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>

    <!-- Image Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close-button" @click="closeModal">&times;</span>
        <img :src="currentImage" :alt="`Seal ${currentImage}`" class="modal-image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import LoadingScreen from '@/components/LoadingScreen.vue'; 

export default {
  components: {
    LoadingScreen,
  },
  data() {
    return {
      seals: {}, // Store all seals data from the backend
      imageIndices: {}, // Track current index for each seal
      totalSeals: 0,
      limit: 10,
      currentPage: 1,
      totalPages: 0,
      showModal: false,
      currentImage: null,
      isLoading: false,
    };
  },
  mounted() {
    this.fetchSeals();
  },
  methods: {
    fetchSeals() {
      this.isLoading = true;
      const offset = (this.currentPage - 1) * this.limit;
      axios.get(`http://localhost:5001/seals?limit=${this.limit}&offset=${offset}`)
        .then(response => {
          this.seals = response.data.data;
          this.totalSeals = response.data.total;
          this.totalPages = Math.ceil(this.totalSeals / this.limit);
          for (let name in this.seals) {
            this.imageIndices[name] = 0;  // Initialize index for each seal
          }
          this.isLoading = false;
        })
        .catch(error => {
          console.error('Error fetching seals:', error);
          this.isLoading = false;
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
    },
    openModal(image) {
      this.currentImage = image;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.currentImage = null;
    },
    goToSealDetails(sealId) {
      this.$router.push({ name: 'SealDetails', params: { sealId } });
    },
  },
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
  cursor: pointer; /* Make it clear that the image is clickable */
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

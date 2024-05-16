<template>
    <div class="list-seals-view">
      <div v-for="(images, name) in seals" :key="name" class="seal">
        <div class="seal-header">
          <h2>{{ name }}</h2>
          <button v-if="images.length > 3" @click="nextImages(name)">Next</button>
        </div>
        <div class="seal-images">
          <img v-for="(image, index) in visibleImages[name]" :key="index" :src="image" alt="Seal" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        seals: {},  // Store all seals data from the backend
        visibleImages: {}  // Store currently visible images for each seal
      };
    },
    mounted() {
      this.fetchSeals();
    },
    methods: {
      fetchSeals() {
        axios.get('http://localhost:5001/seals')  // Adjust URL as needed
          .then(response => {
            this.seals = response.data;
            for (let name in this.seals) {
              this.visibleImages[name] = this.seals[name].slice(0, 3);  // Initialize with the first three images
            }
          })
          .catch(error => {
            console.error('Error fetching seals:', error);
          });
      },
      nextImages(name) {
        const currentIndex = this.seals[name].indexOf(this.visibleImages[name][0]);
        const nextIndex = currentIndex + 3;
        if (nextIndex < this.seals[name].length) {
          this.visibleImages[name] = this.seals[name].slice(nextIndex, nextIndex + 3);
        } else {
          // Reset to the first three images if we reach the end
          this.visibleImages[name] = this.seals[name].slice(0, 3);
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


  </style>
  
  
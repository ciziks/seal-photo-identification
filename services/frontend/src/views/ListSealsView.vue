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
  width: 100%; /* Ensure the main container takes full width */
}

.seal {
  border: 1px solid #ccc;
  padding: 20px;
  margin: 20px;
  width: 90%; /* Use most of the screen width while leaving some margin */
  box-sizing: border-box; /* Include padding and border in the width calculation */
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
  justify-content: flex-start;
  gap: 10px;
  overflow-x: auto; /* Allows horizontal scrolling if needed */
  width: calc(100% - 40px); /* Adjust for padding */
  padding-right: 20px; /* Add padding to ensure space for the scrollbar or the edge of the container */
}

.seal-images img {
  flex: 0 0 auto; /* Allow images to grow or shrink based on their content size */
  max-height: 200px; /* Larger display height */
  object-fit: contain; /* Ensure images are fully visible without cropping */
  margin-right: 10px; /* Space between images */
}

  </style>
  
  
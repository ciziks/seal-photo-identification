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
  
        <div v-if="sighting.images.length" class="sighting-images">
          <h3>Images</h3>
          <div v-for="(image, index) in sighting.images" :key="index" class="image">
            <img :src="image" alt="Sighting Image" />
          </div>
        </div>
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
        error: null
      };
    },
    methods: {
      async fetchSighting() {
        try {
          this.error = null;
          this.sighting = null;
  
          const response = await axios.get(`http://localhost:5001/sightings/${this.sightingId}`);
          this.sighting = response.data;
        } catch (error) {
          this.error = error.response?.data?.detail || error.message;
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
    flex-wrap: wrap;
  }
  
  .image {
    margin-right: 10px;
    margin-bottom: 10px;
  }
  
  .image img {
    max-width: 150px;
    max-height: 150px;
    object-fit: contain;
    border: 1px solid #ccc;
  }
  </style>
  
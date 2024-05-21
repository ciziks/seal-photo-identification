<template>
    <div class="delete-sighting-view">
      <h1>Delete Sighting</h1>
      <form @submit.prevent="deleteSighting">
        <label for="sightingId">Enter Sighting ID:</label>
        <input type="number" v-model="sightingId" id="sightingId" required />
        <button type="submit">Delete</button>
      </form>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        Sighting deleted successfully!
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'DeleteSightingView',
    data() {
      return {
        sightingId: '',
        error: null,
        success: false,
      };
    },
    methods: {
      async deleteSighting() {
        try {
          this.error = null;
          this.success = false;
          await axios.delete(`http://localhost:5001/sightings/${this.sightingId}`);
          this.success = true;
          this.sightingId = '';
  
        } catch (error) {
          if (error.response && error.response.status === 404) {
            this.error = 'Sighting not found.';
          } else {
            this.error = 'An error occurred while deleting the sighting.';
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .delete-sighting-view {
    max-width: 400px;
    margin: 0 auto;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  input {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
    box-sizing: border-box;
  }
  
  button {
    padding: 0.5rem 1rem;
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
  
<template>
    <div class="detect-seal-view">
      <h1>Detect Seal</h1>
      <form @submit.prevent="uploadImage">
        <input type="file" @change="handleFileChange" />
        <button type="submit" :disabled="!file">Upload Image</button>
      </form>
      <div v-if="result">
        <h2>Results</h2>
        <div v-if="result.initial_image">
          <h3>Uploaded Image</h3>
          <img :src="'data:image/jpeg;base64,' + result.initial_image" alt="Initial Seal"/>
        </div>
        <div v-if="result.matched_image">
          <h3>Matched Image</h3>
          <img :src="'data:image/jpeg;base64,' + result.matched_image" alt="Matched Seal"/>
          <p>Name: {{ result.match_name }}</p>
          <p>Score: {{ result.match_score }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        file: null,
        result: null
      };
    },
    methods: {
      handleFileChange(event) {
        this.file = event.target.files[0];
      },
      async uploadImage() {
        const formData = new FormData();
        formData.append('image', this.file);
  
        try {
          const response = await axios.post('http://localhost:5001/seal', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          this.result = response.data;
        } catch (error) {
          console.error('Error uploading image:', error);
          alert('Failed to upload image.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .detect-seal-view form {
    margin-bottom: 20px;
  }
  
  .detect-seal-view img {
    width: 200px;
    height: auto;
    margin: 10px;
  }
  </style>
  
<template>
    <div class="delete-seal-view">
      <h1>Delete Seal</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="ID">Seal ID</label>
          <input v-model="sealID" type="text" id="ID" required />
        </div>
        <button type="submit">Delete Seal</button>
      </form>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        Seal deleted successfully!
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        sealID: "",
        error: null,
        success: false
      };
    },
    methods: {
      async submitForm() {
        try {
          this.error = null;
          this.success = false;
          const response = await axios.delete(`http://localhost:5001/seals/${this.sealID}`);
          console.log('Seal deleted successfully:', response.data);
          this.success = true;
        } catch (error) {
          alert(error.toString());
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .delete-seal-view {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  .form-group {
    margin-bottom: 15px;
  }
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  .form-group input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  button {
    padding: 10px 20px;
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
  
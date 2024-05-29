<template>
    <div class="new-seal-view">
      <h1>New Seal</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="ID">ID/Name</label>
          <input v-model="seal.ID" type="text" id="ID" required />
        </div>
        <div class="form-group">
          <label for="age">Age</label>
          <input v-model="seal.age" type="text" id="age" required />
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea v-model="seal.description" id="description"></textarea>
        </div>
        <div class="form-group">
          <label for="gender">Gender</label>
          <select v-model="seal.gender" id="gender">
            <option value="">Select Gender</option>
            <option value="m">Male</option>
            <option value="f">Female</option>
            <option value="u">Unknown</option>
          </select>
        </div>
        <div class="form-group">
          <label for="isPregnant">Is Pregnant</label>
          <select v-model="seal.isPregnant" id="isPregnant">
            <option value="">Select Option</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
            <option value="Unknown">Unknown</option>
          </select>
        </div>
        <button type="submit">new Seal</button>
      </form>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        Seal added successfully!
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        seal: {
          ID: "",
          age: "",
          comments: "",
          gender: "",
          isPregnant: ""
        },
        error: null,
        success: false
      };
    },
    methods: {
      async submitForm() {
        try {
          this.error = null;
          this.success = false;
          const response = await axios.post('http://localhost:5001/seal', this.seal);
          console.log('Seal added successfully:', response.data);
          this.success = true;
          // Optionally reset form fields after success
          this.seal = {
            ID: "",
            age: "",
            comments: "",
            gender: "",
            isPregnant: ""
          };
        } catch (error) {
          this.error = error.response?.data?.detail || error.message;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .new-seal-view {
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
  .form-group input,
  .form-group select,
  .form-group textarea {
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
  
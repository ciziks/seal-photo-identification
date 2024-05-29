<template>
    <div class="new-seal-view">
      <h1>New Seal</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="ID">ID/Name</label>
          <input v-model="seal.ID" type="text" id="ID" required />
        </div>
        <div class="form-group">
          <label for="age">Age:</label>
          <select v-model="seal.age" id="age">
            <option value="pup">Pup</option>
            <option value="adult">Adult</option>
            <option value="juvenile">Juvenile</option>
            <option value="unknown">Unknown</option>
          </select>
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea v-model="seal.description" id="description"></textarea>
        </div>
        <div class="form-group">
          <label for="gender">Gender</label>
          <select v-model="seal.gender" id="gender">
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="unknwon">Unknown</option>
          </select>
        </div>
        <div class="form-group">
          <label for="isPregnant">Is Pregnant</label>
          <select v-model="seal.isPregnant" id="isPregnant">
            <option value="">Select Option</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
            <option value="unknown">Unknown</option>
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
          const response = await axios.post('http://localhost:5001/seals', this.seal);
          console.log('Seal added successfully:', response.data);
          this.success = true;
          this.$router.push({ name: 'SealDetails', params: { sealId: this.seal.ID } });
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
  
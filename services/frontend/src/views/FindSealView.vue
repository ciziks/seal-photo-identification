<template>
    <div class="find-seal-view">
      <h1>Find Seal</h1>
      <form @submit.prevent="goToSealDetails">
        <label for="sealId">Enter Seal ID:</label>
        <input type="text" v-model="sealId" id="sealId" required />
        <button type="submit">Find Seal</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sealId: '',
      };
    },
    methods: {
      goToSealDetails() {
        this.$router.push({ name: 'SealDetails', params: { sealId: this.sealId } });
      },
    },
  };
  </script>
  
  <style scoped>
  .find-seal-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
  }
  
  h1 {
    margin-bottom: 20px;
    font-size: 2em;
    color: #333;
  }
  
  form {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  
  label {
    margin: 10px 0 5px;
  }
  
  input[type="text"] {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button[type="submit"] {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"]:hover {
    background-color: #0056b3;
  }
  </style>
  
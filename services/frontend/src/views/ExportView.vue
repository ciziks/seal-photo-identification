<template>
    <div class="export-view">
      <h1>Export Data</h1>
      <button @click="exportData">Export to Excel</button>
      <div v-if="loading" class="loading">
        <p>Exporting data...</p>
        <img src="@/assets/images/loading.gif" alt="Loading" />
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        loading: false,
        error: null,
      };
    },
    methods: {
      async exportData() {
        this.loading = true;
        this.error = null;
        try {
          const response = await axios.get('http://localhost:5001/export', {
            responseType: 'blob',
          });
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'database_export.xlsx');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } catch (error) {
          this.error = 'An error occurred while exporting the data.';
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .export-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    text-align: center;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .loading {
    margin-top: 20px;
  }
  
  .loading img {
    width: 50px;
    height: 50px;
  }
  
  .error-message {
    color: red;
    margin-top: 20px;
  }
  </style>
  
<template>
    <div>
      <h1>Add Seal</h1>
      <div
        class="drop-area"
        @dragover.prevent
        @drop="handleDrop"
        @click="triggerFileInput"
        style="border: 2px dashed #0077be; padding: 20px; text-align: center;">
        Drop files here or click to upload
      </div>
      <input type="file" @change="handleFileUpload" ref="fileInput" style="display: none;">
      <input type="text" v-model="name" placeholder="Enter name" style="margin-top: 20px; width: 100%; padding: 8px 16px;">
      <button @click="uploadImage">Upload to Server</button>
      <div v-if="image" class="preview">
        <img :src="image" alt="Preview" />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        image: null,
        file: null,  // Store the file object
        name: ''    // Store the name entered by the user
      };
    },
    methods: {
      triggerFileInput() {
        this.$refs.fileInput.click();
      },
      handleFileUpload(event) {
        const file = event.target.files[0];
        this.file = file;
        this.image = URL.createObjectURL(file);
      },
      handleDrop(event) {
        const file = event.dataTransfer.files[0];
        this.handleFileUpload({ target: { files: [file] } });
      },
      uploadImage() {
        if (!this.file) {
          alert('Please select a file first.');
          return;
        }
        if (!this.name.trim()) {
          alert('Please enter a name.');
          return;
        }
  
        const formData = new FormData();
        formData.append('image', this.file);
        formData.append('name', this.name);  // Add the name to the FormData object
  
        axios.post('http://localhost:5001/seal/image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log('File uploaded successfully', response);
          alert('File uploaded successfully');
          this.$router.push('/');
        })
        .catch(error => {
          console.error('Error uploading the file', error);
          alert('Error uploading the file',error);
        });
      }
    }
  };
  </script>
  
  <style>
  .drop-area {
    cursor: pointer;
  }
  .preview img {
    width: 100%;
    max-width: 400px;
  }
  input[type="text"] {
    font-size: 16px; 
  }
  </style>
  
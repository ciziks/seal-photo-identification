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
    <button @click="uploadImage" :disabled="isLoading">Upload to Server</button>
    <div v-if="image" class="preview">
      <img :src="image" alt="Preview" />
    </div>
    <div v-if="isLoading">Uploading...</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      image: null,
      file: null,
      name: '',
      isLoading: false
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

      this.isLoading = true;
      const formData = new FormData();
      formData.append('image', this.file);
      formData.append('name', this.name);

      axios.post('http://localhost:5001/seal/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
       const { status, image_id } = response.data;
       console.log('Response status:', status);
       if (status === "success") {
         console.log('File uploaded successfully with image ID:', image_id);
          alert(`File uploaded successfully! Image ID: ${image_id}`);
          this.resetForm();
        } else {
          alert(`Upload failed with status: ${status}`);
        }
      })
      .catch(error => {
        console.error('Error uploading the file', error);
        alert('Error uploading the file');
        this.isLoading = false;
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

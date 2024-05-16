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

    <!-- Cropper Component -->
    <vue-cropper
      v-if="image"
      ref="cropper"
      :src="image"
      alt="Source Image"
      :view-mode="1"
      :guides="true"
      :aspect-ratio="16/9"
      style="margin-top: 20px;"
    />

    <button @click="getCroppedImage" :disabled="isLoading">Crop Image</button>
    <button @click="uploadImage" :disabled="isLoading || !croppedImage">Upload to Server</button>

    <div v-if="croppedImage" class="preview">
      <img :src="croppedImage" alt="Cropped Preview" />
    </div>
    <div v-if="isLoading">Uploading...</div>
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import axios from 'axios';

export default {
  components: {
    VueCropper
  },
  data() {
    return {
      image: null,
      croppedImage: null,
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
    getCroppedImage() {
      const canvas = this.$refs.cropper.getCroppedCanvas();
      canvas.toBlob(blob => {
        this.croppedImage = URL.createObjectURL(blob);
        this.file = blob; // Update the file to be uploaded
      });
    },
    uploadImage() {
      if (!this.file) {
        alert('Please crop the image first.');
        return;
      }
      if (!this.name.trim()) {
        alert('Please enter a name.');
        return;
      }

      this.isLoading = true;
      const formData = new FormData();
      formData.append('image', this.file, 'cropped-image.png');
      formData.append('name', this.name);

      axios.post('http://localhost:5001/seal/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        this.isLoading = false;
        alert('File uploaded successfully!');
        this.croppedImage = null; // Clear cropped image after uploading
      })
      .catch(error => {
        this.isLoading = false;
        alert(error.toString());
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

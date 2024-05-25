<template>
  <div class="seal-details-view">
    <h1>Seal Details</h1>
    <div v-if="seal">
      <button class="edit-button" @click="openEditModal">Edit</button>
      <p>ID: {{ seal.ID }}</p>
      <p>Age: {{ seal.age }}</p>
      <p>Gender: {{ seal.gender }}</p>
      <p>Comments: <span v-if="seal.comments" class="data">{{ seal.comments }}</span><span v-else class="no-data"><em>no data</em></span></p>
      <p>Pregnant: <span v-if="seal.isPregnant" class="data">{{ seal.isPregnant }}</span><span v-else class="no-data"><em>no data</em></span></p>
      <div class="seal-images-grid">
        <div v-for="(image, index) in seal.images" :key="index" class="image-container" @click="openModal(image)">
          <img :src="image" alt="Seal Image" />
        </div>
      </div>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- Image Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close-button" @click="closeModal">&times;</span>
        <img :src="currentImage" alt="Seal Image" class="modal-image" />
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <span class="close-button" @click="closeEditModal">&times;</span>
        <h2>Edit Seal Information</h2>
        <form @submit.prevent="updateSeal">
          <label for="age">Age:</label>
          <input type="text" v-model="editSeal.age" id="age" />

          <label for="gender">Gender:</label>
          <input type="text" v-model="editSeal.gender" id="gender" />

          <label for="comments">Comments:</label>
          <textarea v-model="editSeal.comments" id="comments"></textarea>

          <label for="isPregnant">Pregnant:</label>
          <input type="text" v-model="editSeal.isPregnant" id="isPregnant" />

          <button type="submit">Confirm</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';

export default {
  props: ['sealId'],
  data() {
    return {
      seal: null,
      errorMessage: '',
      showModal: false,
      currentImage: null,
      showEditModal: false,
      editSeal: {
        age: '',
        gender: '',
        comments: '',
        isPregnant: '',
      },
    };
  },
  setup() {
    const isLoading = inject('isLoading');
    const setLoading = inject('setLoading');
    return { isLoading, setLoading };
  },
  async created() {
    this.setLoading(true);
    await this.fetchSeal(this.sealId);
    this.setLoading(false);
  },
  methods: {
    async fetchSeal(sealId) {
      try {
        const response = await axios.get(`http://localhost:5001/seals/${sealId}`);
        this.seal = response.data;
        this.editSeal = { ...response.data }; // Initialize editSeal with current data
      } catch (error) {
        this.errorMessage = 'Seal not found';
      }
    },
    openModal(image) {
      this.currentImage = image;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.currentImage = null;
    },
    openEditModal() {
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    async updateSeal() {
      try {
        const response = await axios.put(`http://localhost:5001/seals/${this.sealId}`, this.editSeal);
        this.seal = response.data; // Update the displayed seal data
        this.closeEditModal();
        location.reload(); // Reload the page
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || error.message;
      }
    },
  },
};
</script>

<style scoped>
.seal-details-view {
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

.error-message {
  color: red;
  margin-top: 20px;
}

.seal-images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
  width: 100%;
}

.image-container img {
  width: 100%;
  height: auto;
  border: 1px solid #ccc;
  object-fit: contain;
  cursor: pointer;
}

.edit-button {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-button:hover {
  background-color: #0056b3;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
}

.modal-content {
  position: relative;
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  max-width: 80%;
  max-height: 80%;
  text-align: center;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 2em;
  cursor: pointer;
}

.modal-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}

form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

label {
  margin: 10px 0 5px;
}

input[type="text"],
textarea {
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

.data {
  color: #333;
}

.no-data {
  color: #888;
  font-style: italic;
}
</style>

<template>
  <div class="delete-sighting-view">
    <h1>Delete Sighting</h1>
    <form @submit.prevent="deleteSighting">
      <div>
        <label for="date">Date:</label>
        <input type="date" v-model="date" id="date" required />
      </div>
      <div>
        <label for="location">Location:</label>
        <select v-model="location" id="location" required>
          <option value="" disabled>Select Location</option>
          <option value="field">Field</option>
          <option value="centre">Centre</option>
        </select>
      </div>
      <button type="submit">Delete</button>
    </form>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-if="success" class="success-message">
      Sighting deleted successfully!
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeleteSightingView',
  data() {
    return {
      date: '',
      location: '',
      error: null,
      success: false,
    };
  },
  methods: {
    async deleteSighting() {
      try {
        this.error = null;
        this.success = false;

        // Format the date to dd-mm-yyyy
        const formattedDate = this.date.split('-').reverse().join('-');
        
        await axios.delete(`http://localhost:5001/sightings/${this.location}/${formattedDate}`);
        
        this.success = true;
        this.date = '';
        this.location = '';

      } catch (error) {
        if (error.response && error.response.status === 404) {
          this.error = 'Sighting not found.';
        } else {
          this.error = 'An error occurred while deleting the sighting.';
        }
      }
    }
  }
};
</script>

<style scoped>
.delete-sighting-view {
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input,
select {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  box-sizing: border-box;
}

button {
  padding: 0.5rem 1rem;
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

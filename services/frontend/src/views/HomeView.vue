<template>
  <div class="home-view">
    <header>
      <h1>Seal Photo Identification Project</h1>
    </header>
    <section class="intro">
      <p>Welcome to the Seal Photo Identification System.</p>
    </section>
    <section class="features">
      <div class="feature">
        <h2>Visualize Data</h2>
        <p>Analyze data through a user-friendly interface.</p>
      </div>
      <div class="feature">
        <h2>Add New Sightings</h2>
        <p>Easily add and categorize new seal sightings.</p>
      </div>
    </section>
    <section class="cta">
      <button @click="getStarted">Get Started</button>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    getStarted() {
      this.$router.push('/add-sighting');
    }
  }
};
</script>

<style scoped>
.home-view {
  font-family: 'Arial', sans-serif; 
  text-align: center;
  background-image: url('@/assets/images/background.jpeg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  min-height: 90vh; /* Ensures the background covers the full viewport height */
  width: 145%;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

header {
  background: rgba(0, 0, 0, 0.7);
  padding: 20px;
  color: #fff;
}

header h1 {
  color: #fff;
}

.intro {
  background: rgba(0, 0, 0, 0.6);
  margin: 20px auto; /* Centered horizontally */
  padding: 20px;
  border-radius: 10px;
  color: #fff;
  max-width: 80%; /* Ensures the background only extends where the text is */
}

.features {
  display: flex;
  justify-content: space-around;
  margin: 20px;
}

.feature {
  background: rgba(0, 0, 0, 0.6);
  padding: 20px;
  margin: 10px;
  border-radius: 10px;
  width: 30%;
  color: #fff;
}

.cta {
  margin: 20px;
}

button {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}
</style>

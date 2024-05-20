<template>
  <div id="app">
    <div class="sidebar">
      <router-link to="/">
        <img src="@/assets/images/logo_64x64.jpeg" alt="Logo" class="logo"/>
      </router-link>
      <router-link to="/add-seal" class="btn btn-primary">Add Seal</router-link>
      <router-link to="/delete-seal" class="btn btn-primary">Delete Seal</router-link>
      <router-link to="/upload-seal" class="btn btn-primary">Upload Sighting</router-link>
      <router-link to="/detect-seal" class="btn btn-primary">Detect seal</router-link>
      <router-link to="/list-seals" class="btn btn-primary">List seals</router-link>
    </div>
    <div class="content">
      <router-view/>
    </div>
  </div>
</template>

<style>
#app {
  display: flex;
  min-height: 100vh;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
.sidebar {
  width: 200px;
  background-color: #15467d; /* Marine blue */
  color: white;
  height: 100vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed; 
  left: 0; /* Ensures the sidebar is aligned to the left edge of the viewport */
  top: 0; /* Aligns the sidebar to the top of the viewport */
}

.logo {
  margin-top: 10px;
  width: 64px; /* Adjust size as needed */
}
.content {
  flex: 1;
  text-align: left;
  padding: 20px;
  margin-left: 220px; /* Adjust this value to match the sidebar's width plus any desired spacing */
}
.btn {
  margin-top: 20px;
  width: 100%; /* Full-width button */
}
.logo {
  cursor: pointer; /* Optional: changes cursor on hover to indicate clickability */
}
</style>

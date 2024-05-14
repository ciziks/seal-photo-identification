<template>
  <div id="app">
    <div class="sidebar">
      <router-link to="/">
        <img src="@/assets/images/logo_64x64.jpeg" alt="Logo" class="logo"/>
      </router-link>
      <router-link to="/upload-seal" class="btn btn-primary">Upload seal</router-link>
      <router-link to="/detect-seal" class="btn btn-primary">Detect seal</router-link>
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
}
.logo {
  margin-top: 10px;
  width: 64px; /* Adjust size as needed */
}
.content {
  flex: 1;
  text-align: left;
  padding: 20px;
}
.btn {
  margin-top: 20px;
  width: 100%; /* Full-width button */
}
.logo {
  cursor: pointer; /* Optional: changes cursor on hover to indicate clickability */
}
</style>

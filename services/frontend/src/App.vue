<template>
  <div id="app">
    <loading-screen :isLoading="isLoading" />
    <div class="sidebar">
      <router-link to="/">
        <img src="@/assets/images/logo_64x64.jpeg" alt="Logo" class="logo"/>
      </router-link>
      <router-link to="/new-sighting" class="btn btn-primary">New Sighting</router-link>
      <router-link to="/find-sighting" class="btn btn-primary">Find sighting</router-link>
      <router-link to="/new-seal" class="btn btn-primary">New Seal</router-link>
      <router-link to="/list-seals" class="btn btn-primary">List seals</router-link>
      <router-link to="/find-seal" class="btn btn-primary">Find Seal</router-link>
      <router-link to="/export" class="btn btn-primary">Export Database</router-link>

      <router-link to="/delete-sighting" class="btn btn-primary">Delete Sighting</router-link>
      
      
      <router-link to="/user-guide" class="btn btn-primary user-guide">User Guide</router-link> 
    </div>
    <div class="content">
      <router-view/>
    </div>
  </div>
</template>

<script>
import { ref, provide } from 'vue';
import LoadingScreen from './components/LoadingScreen.vue';

export default {
  components: {
    LoadingScreen,
  },
  setup() {
    const isLoading = ref(false);
    const setLoading = (state) => {
      isLoading.value = state;
    };

    provide('isLoading', isLoading);
    provide('setLoading', setLoading);

    return { isLoading, setLoading };
  },
};
</script>

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
.user-guide {
  margin-top: auto; /* Pushes the User Guide link to the bottom of the sidebar */
}
</style>

<template>
    <div v-if="isLoading" class="loading-screen">
      <div class="loading-content">
        <p>Loading...</p>
        <img src="@/assets/images/loading.gif" alt="Loading" />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isLoading: {
        type: Boolean,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .loading-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .loading-content {
    text-align: center;
    color: white;
  }
  
  .loading-content img {
    width: 350px;
    height: 350px;
  }
  </style>
  
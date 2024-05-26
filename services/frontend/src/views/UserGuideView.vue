<template>
    <div class="user-guide-view">
      <h1>User Guide</h1>
      <p>Welcome to the Seal Tracking Application user guide. Here you'll find instructions on how to use the app.</p>
      <h2>Navigation</h2>
      <p>Use the sidebar to navigate between different sections of the application:</p>
      <ul>
        <li><strong>Add Seal:</strong> Fill in the details of the new seal and click 'Add Seal' to save it.</li>
        <li><strong>Delete Seal:</strong> Enter the ID of the seal to delete and click 'Delete Seal' to remove it.</li>
        <li><strong>Find Seal:</strong> Enter the ID of the seal to find and click 'Find Seal' to view its details.</li>
        <li><strong>List Seals:</strong> View a paginated list of all seals in the database.</li>
        <li><strong>Add Sighting:</strong> Record a new sighting by uploading images and entering sighting details.</li>
        <li><strong>Delete Sighting:</strong> Enter the ID of the sighting to delete and click 'Delete Sighting' to remove it.</li>
        <li><strong>List Sighting:</strong> View a paginated list of all sightings in the database.</li>
      </ul>
      <h2>Functionality</h2>
      <p>Each section in the sidebar provides specific functionality:</p>
      <ul>
        <li><button @click="openModal('addSeal')">Add Seal</button></li>
        <li><button @click="openModal('deleteSeal')">Delete Seal</button></li>
        <li><button @click="openModal('findSeal')">Find Seal</button></li>
        <li><button @click="openModal('listSeals')">List Seals</button></li>
        <li><button @click="openModal('addSighting')">Add Sighting</button></li>
        <li><button @click="openModal('deleteSighting')">Delete Sighting</button></li>
        <li><button @click="openModal('listSighting')">List Sighting</button></li>
      </ul>
  
      <modal v-for="(content, modal) in modals" :key="modal" :title="content.title" :isVisible="activeModal === modal" @close="closeModal">
        <div v-html="content.body"></div>
      </modal>
    </div>
  </template>
  
  <script>
  import Modal from '@/components/Modal.vue';
  
  export default {
    components: {
      Modal,
    },
    data() {
      return {
        activeModal: null,
        modals: {
          addSeal: {
            title: 'Add Seal',
            body: `
              <p>The "Add Seal" functionality allows you to create a new seal in the database without pictures. Follow these steps to add a seal:</p>
              <ul>
                <li>Fill in the ID/Name of the seal.</li>
                <li>Provide the age of the seal.</li>
                <li>Add any comments regarding the seal. This field is optional.</li>
                <li>Select the gender of the seal. Options are Male, Female, or Unknown.</li>
                <li>Select whether the seal is pregnant. Options are Yes, No, or Unknown.</li>
                <li>Click the 'Add Seal' button to save the seal information.</li>
              </ul>
              <p>This functionality is specifically used for creating seals that do not have pictures associated with them.</p>
            `,
          },
          deleteSeal: {
            title: 'Delete Seal',
            body: `
              <p>The "Delete Seal" functionality allows you to remove an existing seal from the database along with all its encounters, but related sightings are not affected. Follow these steps to delete a seal:</p>
              <ul>
                <li>Enter the ID of the seal you wish to delete.</li>
                <li>Click the 'Delete Seal' button to remove the seal.</li>
              </ul>
              <p>Note: All seal encounters associated with the deleted seal are removed, but related sightings are not affected.</p>
            `,
          },
          findSeal: {
            title: 'Find Seal',
            body: `
              <p>The "Find Seal" functionality allows you to search for a seal in the database by its ID and view its details. Follow these steps to find a seal:</p>
              <ul>
                <li>Enter the ID of the seal you wish to find.</li>
                <li>Click the 'Find Seal' button to view the seal's details.</li>
                <li>You will be redirected to the seal's profile page, where you can see all the information about the seal.</li>
                <li>On the seal's profile page, you can click the 'Edit' button to modify the seal's information.</li>
              </ul>
            `,
          },
          listSeals: {
            title: 'List Seals',
            body: `
              <p>The "List Seals" functionality allows you to view a paginated list of all seals that are currently stored in the database. Follow these steps to navigate through the list of seals:</p>
              <ul>
                <li>The list displays the names of the seals. Clicking on a seal's name will redirect you to its profile page where you can view detailed information about the seal.</li>
                <li>Each seal entry shows up to three images. If there are more than three images, use the right arrow button to view the next set of images.</li>
                <li>You can navigate through the pages of seals using the 'Previous' and 'Next' buttons located at the bottom of the list.</li>
              </ul>
              <p>This functionality helps in browsing through the seals stored in the database and accessing their detailed profiles easily.</p>
            `,
          },
          addSighting: {
            title: 'Add Sighting',
            body: `
              <p>The "Add Sighting" functionality allows you to record a new sighting by uploading images and entering sighting details. Follow these steps to add a sighting:</p>
              <ul>
                <li>Fill in the date of the sighting.</li>
                <li>Select the location of the sighting (Field or Centre).</li>
                <li>Upload a batch of images by dropping files into the designated area or clicking to upload.</li>
                <li>Each image can be cropped multiple times to capture different parts of the image.</li>
                <li>After cropping an image, click 'Crop Image' to save the crop and proceed to the next one.</li>
                <li>Once all images are cropped, you can review each cropped image and choose to either detect the seal or skip to the next image.</li>
                <li>If you choose to detect, the program will run the detection algorithm and display the top 5 matches in descending order of probability.</li>
                <li>You can select one of the detected seals as a match by clicking 'Select', or create a new seal entry by clicking 'New Seal'.</li>
                <li>If you create a new seal, you will need to provide additional information about the seal.</li>
                <li>Continue with the next cropped image until all images are processed.</li>
              </ul>
              <p>This functionality ensures accurate tracking and recording of seal sightings by utilizing image cropping and seal detection capabilities.</p>
            `,
          },
          deleteSighting: {
             title: 'Delete Sighting',
             body: `
             <p>The "Delete Sighting" functionality allows you to remove an existing sighting from the database based on the date and location. Follow these steps to delete a sighting:</p>
             <ul>
                 <li>Select the date of the sighting you wish to delete using the date picker.</li>
                 <li>Choose the location of the sighting from the dropdown menu (either "Field" or "Centre").</li>
                 <li>Click the 'Delete' button to remove the sighting.</li>
             </ul>
             <p>Note: All related encounters are deleted from the database, but the seals from those encounters remain unaffected.</p>
            `,
            },

          listSighting: {
            title: 'List Sighting',
            body: `
              <p>The "List Sighting" functionality allows you to view a sighting based on a specific date and location. Follow these steps to view sightings:</p>
              <ul>
                <li>Enter the date of the sighting.</li>
                <li>Select the location of the sighting (Field or Centre).</li>
                <li>Click the 'Get Sighting' button to fetch the sighting.</li>
                <li>You will see the seals photographed during that sighting for the specified date and location.</li>
                <li>Click on a seal's name to view its detailed profile.</li>
              </ul>
              <p>This functionality helps in tracking and reviewing sightings based on specific dates and locations, providing an overview of all seals photographed during that sighting.</p>
            `,
          },
        },
      };
    },
    methods: {
      openModal(modal) {
        this.activeModal = modal;
      },
      closeModal() {
        this.activeModal = null;
      },
    },
  };
  </script>
  
  <style scoped>
  .user-guide-view {
    padding: 20px;
  }
  
  button {
    padding: 10px;
    margin: 5px 0;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  
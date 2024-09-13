const { defineConfig } = require("cypress");
const fs = require('fs');
const path = require('path');

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://127.0.0.1:5000/",
    viewportWidth: 1920,
    viewportHeight: 1080,
    downloadsFolder: 'cypress/downloads',  
    setupNodeEvents(on, config) {
      // Task to clear the downloads folder
      on('task', {
        clearDownloads() {
          const downloadsFolder = config.downloadsFolder;
          if (fs.existsSync(downloadsFolder)) {
            fs.readdirSync(downloadsFolder).forEach(file => {
              fs.unlinkSync(path.join(downloadsFolder, file));
            });
          }
          return null;
        }
      });
    },
  },
});

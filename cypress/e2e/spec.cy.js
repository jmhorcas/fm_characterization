import 'cypress-file-upload';


function fillFormAndSubmit({ name, description, author, year, reference, keywords, domain, fmFile, zipFile }) {
  if (name) cy.get("#inputName").type(name);
  if (description) cy.get("#inputDescription").type(description);
  if (author) cy.get("#inputAuthor").type(author);
  if (year) cy.get("#inputYear").type(year);
  if (reference) cy.get("#inputReference").type(reference);
  if (keywords) cy.get("#inputKeywords").type(keywords);
  if (domain) cy.get("#inputDomain").type(domain);
  if (fmFile) cy.get("#inputFM").attachFile(fmFile);
  if (zipFile) cy.get("#inputZipThreshold").attachFile(zipFile);
  cy.get("#submitButton").click();
}


function selectPizzasModelAndUploadZip() {
  cy.visit("/");
  cy.get("#inputExample").select("Pizzas");
  cy.get("#inputExample").should("have.value", "Pizzas");
  cy.get("#inputZipThreshold").attachFile("Modelos.zip");
  cy.get("#submitButton").click();
}


function uploadDatasetAndProceed() {
  cy.visit("/");
  cy.get("#upload-zip-tab").click();
  cy.get("#inputZip").attachFile("Modelos.zip");
  cy.get("#submitZipButton").click();
}

describe("Analyze a Feature Model", () => {
  
  before(() => {
    cy.task('clearDownloads');
  });

  it("Uploads and verifies feature model analysis", () => {
    cy.visit("/");
    fillFormAndSubmit({
      name: "Pizzas",
      description: "This feature model is about pizzas!",
      author: "Angela",
      year: "2024",
      reference: "https://fmfactlabel.adabyron.uma.es/",
      keywords: "Pizza, Italian, Food",
      domain: "Italian food",
      fmFile: "Pizzas.uvl",
      zipFile: "Modelos.zip"
    });
    cy.get('svg#FMFactLabelChart').should('exist');
  });

  it("Shows error when unsupported file type is uploaded", () => {
    cy.visit("/");
    fillFormAndSubmit({
      name: "Pizzas",
      description: "This feature model is about pizzas!",
      author: "Angela",
      year: "2024",
      reference: "https://fmfactlabel.adabyron.uma.es/",
      keywords: "Pizza, Italian, Food",
      domain: "Italian food",
      fmFile: "Texto.txt" 
    });
    cy.get('.alert.alert-danger').should('exist')
      .and('contain', 'Feature model format not supported.');
  });

  it("Shows error message when submitting empty form", () => {
    cy.visit("/");
    cy.get("#submitButton").click();
    cy.get('.alert.alert-danger').should('exist')
      .and('contain', 'Please upload a feature model or select one from the examples.');
    cy.get('svg#FMFactLabelChart').should('not.exist');
  });

  it("Shows error when uploading ZIP without UVL files in Threshold", () => {
    cy.visit("/");
    fillFormAndSubmit({
      name: "Pizzas",
      description: "This feature model is about pizzas!",
      author: "Angela",
      year: "2024",
      reference: "https://fmfactlabel.adabyron.uma.es/",
      keywords: "Pizza, Italian, Food",
      domain: "Italian food",
      fmFile: "Pizzas.uvl",
      zipFile: "Texto.zip" 
    });
    cy.get('.alert.alert-danger').should('exist')
      .and('contain', 'No valid UVL files found in the Threshold ZIP.');
  });

  it("Handles interactions with the feature model", () => {
    selectPizzasModelAndUploadZip();
    cy.get('svg#FMFactLabelChart').should('exist');
    cy.get("#collapseSubProperties").click();
    cy.get("#collapseSubProperties").click();
    cy.get("#collapseZeroValues").click();
    cy.get("#collapseZeroValues").click();
    cy.get("#toggle-chart").click();
    cy.get('svg#FMFactLabelChartLandscape').should('exist');
    cy.get("#toggle-chart").click();
  });

  context("File Download Verification", () => {

    beforeEach(() => {
      cy.task('clearDownloads'); 
      selectPizzasModelAndUploadZip(); 
    });

    it("Downloads SVG file", () => {
      cy.get("#dropdownMenuLink").click();
      cy.get("#saveSVG").click();
      cy.readFile('cypress/downloads/Pizzas.svg').should('exist');
    });

    it("Downloads PNG file", () => {
      cy.get("#dropdownMenuLink").click();
      cy.get("#savePNG").click();
      cy.readFile('cypress/downloads/Pizzas.png').should('exist');
    });

    it("Downloads PDF file", () => {
      cy.get("#dropdownMenuLink").click();
      cy.get("#savePDF").click();
      cy.readFile('cypress/downloads/Pizzas.pdf').should('exist');
    });

    it("Exports model to JSON", () => {
      cy.get("#dropdownMenuLink").click();
      cy.get("#saveJSON").click();
      cy.readFile('cypress/downloads/Pizzas.json').should('exist');
    });

    it("Exports model to TXT", () => {
      cy.get("#dropdownMenuLink").click();
      cy.get("#saveTXT").click();
      cy.readFile('cypress/downloads/Pizzas.txt').should('exist');
    });

    it("Downloads Landscape SVG file", () => {
      cy.get("#toggle-chart").click();
      cy.get("#dropdownMenuLinkLandscape").click();
      cy.get("#saveSVGLandscape").click();
      cy.readFile('cypress/downloads/Pizzas.svg').should('exist');
    });

    it("Downloads Landscape PNG file", () => {
      cy.get("#toggle-chart").click();
      cy.get("#dropdownMenuLinkLandscape").click();
      cy.get("#savePNGLandscape").click();
      cy.readFile('cypress/downloads/Pizzas.png').should('exist');
    });

    it("Downloads Landscape PDF file", () => {
      cy.get("#toggle-chart").click();
      cy.get("#dropdownMenuLinkLandscape").click();
      cy.get("#savePDFLandscape").click();
      cy.readFile('cypress/downloads/Pizzas.pdf').should('exist');
    });
  });
});

describe("Analyze Feature Model Dataset", () => {

  it("Uploads ZIP file successfully", () => {
    uploadDatasetAndProceed();
    cy.get('.alert.alert-danger').should('not.exist');
  });

  it("Shows error when ZIP without UVL files is uploaded", () => {
    cy.visit("/");
    cy.get("#upload-zip-tab").click();
    cy.get("#inputZip").attachFile("Texto.zip");  
    cy.get("#submitZipButton").click();
    cy.get('.alert.alert-danger').should('exist')
      .and('contain', 'No valid UVL files found in the ZIP.');
  });

  it("Handles collapse/expand and chart interactions", () => {
    uploadDatasetAndProceed();
    cy.get('svg#FMFactLabelDataSetChart').should('exist');
    cy.get("#collapseSubProperties").click();
    cy.get("#collapseSubProperties").click();
    cy.get("#collapseZeroValues").click();
    cy.get("#collapseZeroValues").click();
    cy.get("#toggle-chart-data-set").click();
    cy.get('svg#FMFactLabelDataSetChartLandscape').should('exist');
    cy.get("#toggle-chart-data-set").click();
  });

  context("File Download Verification", () => {

    beforeEach(() => {
      cy.task('clearDownloads');
    });

    it("Downloads SVG file", () => {
      uploadDatasetAndProceed();
      cy.get("#dropdownMenuLinkDataSet").click();
      cy.get("#saveSVGDataSet").click();
      cy.readFile('cypress/downloads/Modelos.svg').should('exist');
    });

    it("Downloads PNG file", () => {
      uploadDatasetAndProceed();
      cy.get("#dropdownMenuLinkDataSet").click();
      cy.get("#savePNGDataSet").click();
      cy.readFile('cypress/downloads/Modelos.png').should('exist');
    });

    it("Downloads PDF file", () => {
      uploadDatasetAndProceed();
      cy.get("#dropdownMenuLinkDataSet").click();
      cy.get("#savePDFDataSet").click();
      cy.readFile('cypress/downloads/Modelos.pdf').should('exist');
    });

    it("Downloads Landscape SVG file", () => {
      uploadDatasetAndProceed();
      cy.get("#toggle-chart-data-set").click();
      cy.get("#dropdownMenuLinkDataSetLandscape").click();
      cy.get("#saveSVGDataSetLandscape").click();
      cy.readFile('cypress/downloads/Modelos.svg').should('exist');
    });

    it("Downloads Landscape PNG file", () => {
      uploadDatasetAndProceed();
      cy.get("#toggle-chart-data-set").click();
      cy.get("#dropdownMenuLinkDataSetLandscape").click();
      cy.get("#savePNGDataSetLandscape").click();
      cy.readFile('cypress/downloads/Modelos.png').should('exist');
    });

    it("Downloads Landscape PDF file", () => {
      uploadDatasetAndProceed();
      cy.get("#toggle-chart-data-set").click();
      cy.get("#dropdownMenuLinkDataSetLandscape").click();
      cy.get("#savePDFDataSetLandscape").click();
      cy.readFile('cypress/downloads/Modelos.pdf').should('exist');
    });
  });
});

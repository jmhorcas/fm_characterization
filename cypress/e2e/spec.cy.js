import 'cypress-file-upload';

function selectPizzasModelAndUploadZip() {
  cy.visit("/");
  cy.get("#inputExample").select("Pizzas");
  cy.get("#inputExample").should("have.value", "Pizzas");
  cy.get("#inputZipThreshold").attachFile("Modelos.zip");
  cy.get("#submitButton").click();
}

describe("Feature Model Analysis", () => {

  before(() => {
    cy.task('clearDownloads');
  });

  it("Uploads and verifies feature model analysis", () => {
    cy.visit("/");
    cy.get("#inputName").type("Pizzas");
    cy.get("#inputDescription").type("This feature model is about pizzas!");
    cy.get("#inputAuthor").type("Angela");
    cy.get("#inputYear").type("2024");
    cy.get("#inputReference").type("https://fmfactlabel.adabyron.uma.es/");
    cy.get("#inputKeywords").type("Carbonara, eggs, parmesan");
    cy.get("#inputDomain").type("Italian food");
    cy.get("#inputFM").attachFile("Pizzas.uvl");
    cy.get("#inputZipThreshold").attachFile("Modelos.zip");
    cy.get("#submitButton").click();
    cy.get('svg#FMFactLabelChart').should('exist');
  });

  it("Shows error when unsupported file type is uploaded", () => {
    cy.visit("/");
    cy.get("#inputName").type("Pizzas");
    cy.get("#inputDescription").type("This feature model is about pizzas!");
    cy.get("#inputAuthor").type("Angela");
    cy.get("#inputYear").type("2024");
    cy.get("#inputReference").type("https://fmfactlabel.adabyron.uma.es/");
    cy.get("#inputKeywords").type("Carbonara, eggs, parmesan");
    cy.get("#inputDomain").type("Italian food");
    cy.get("#inputFM").attachFile("Texto.txt"); 
    cy.get("#submitButton").click();
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
    });

    it("Downloads SVG file", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#dropdownMenuLink").click();
      cy.get("#saveSVG").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.svg').should('exist');
    });

    it("Downloads PNG file", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#dropdownMenuLink").click();
      cy.get("#savePNG").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.png').should('exist');
    });

    it("Downloads PDF file", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#dropdownMenuLink").click();
      cy.get("#savePDF").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.pdf').should('exist');
    });

    it("Exports model to JSON", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#dropdownMenuLink").click();
      cy.get("#saveJSON").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.json').should('exist');
    });

    it("Exports model to TXT", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#dropdownMenuLink").click();
      cy.get("#saveTXT").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.txt').should('exist');
    });

    it("Downloads Landscape SVG file", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#toggle-chart").click();
      cy.get("#dropdownMenuLinkLandscape").click();
      cy.get("#saveSVGLandscape").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.svg').should('exist');
    });

    it("Downloads Landscape PNG file", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#toggle-chart").click();
      cy.get("#dropdownMenuLinkLandscape").click();
      cy.get("#savePNGLandscape").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.png').should('exist');
    });

    it("Downloads Landscape PDF file", () => {
      selectPizzasModelAndUploadZip();
      cy.get("#toggle-chart").click();
      cy.get("#dropdownMenuLinkLandscape").click();
      cy.get("#savePDFLandscape").click();
      cy.wait(1000);
      cy.readFile('cypress/downloads/Pizzas.pdf').should('exist');
    });
  });
});

describe("Feature Model Dataset Upload", () => {
  it("Uploads ZIP file successfully", () => {
    cy.visit("/");
    cy.get("#upload-zip-tab").click();
    cy.get("#inputZip").attachFile("Modelos.zip");
    cy.get("#submitZipButton").click();
  });
});

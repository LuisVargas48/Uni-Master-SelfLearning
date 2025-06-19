describe ("Conjunto de pruebas", () => {

  beforeEach(() => {
    cy.visit("https://opensource-demo.orangehrmlive.com/")
   })

   it("Prueba de logo", () => {
   
    cy.get(".orangehrm-login-branding").should("be.visible")


   })


   it("Campo Username visible", () => {
   
    cy.get(":nth-child(2) > .oxd-input-group > :nth-child(2) > .oxd-input").type("username")



   })

   it("Etiqueta con version de orange", () => {
   
    cy.get(".orangehrm-copyright-wrapper > :nth-child(1)").contains("OrangeHRM OS 5.6.1")


   })

   it("Botón Login Visible", () => {
   cy.get(".oxd-button").should("be.visible")



   })




})
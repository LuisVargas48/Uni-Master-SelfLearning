

describe ('Pruebas de validacion pagina de inicio', function (){
    beforeEach(() => {
        // runs before each test in the block
        cy.visit("https://opensource-demo.orangehrmlive.com")
      })

    it ('Validacion de logo superior', function (){
      cy.get('#divLogo > img').should('be.visible') 
    })

  it ('Validacion campo username existe', function (){
    cy.get('#txtUsername').should('be.visible')
  })
  it ('Validacion del texto del footer', function (){
    cy.get('#footer').contains('OrangeHRM')
  })
  it ('Validacion del boton login es visible', function (){
    cy.get('#btnLogin').should('be.visible')
  })
       
})
describe("Тестирование работоспособности страниц", () => {
  it("Проверка /", () => {
    cy.visit('http://localhost:81/');
  });
  it("Проверка /canvas", () => {
    cy.visit('http://localhost:81/canvas');
  });
  it("Проверка /result", () => {
    cy.visit('http://localhost:81/result');
  });
});
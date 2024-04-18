describe('Проверка холста', () => {
  beforeEach(() => {
    cy.visit('http://localhost:81/canvas');
    cy.get('canvas').as('canvas');
  });

  it('allows drawing on the canvas', () => {
    const drawLine = (line) => {
      cy.get('@canvas')
        .trigger('mousedown', {
          clientX: line.startX,
          clientY: line.startY,
          force: true
        })
        .trigger('mousemove', {
          clientX: line.endX,
          clientY: line.endY,
          force: true
        })
        .trigger('mouseup', { force: true });
    };

    drawLine({ startX: 10, startY: 10, endX: 100, endY: 100 });

  });

  it('clears the canvas', () => {
    cy.get('button#canvas-clear').click(); // Предполагается, что есть кнопка для очистки холста
  });

});


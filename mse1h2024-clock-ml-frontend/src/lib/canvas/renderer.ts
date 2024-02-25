export class Renderer {
	constructor(private ctx: CanvasRenderingContext2D) {}

	paint(e: MouseEvent, color: `#${string}` = "#000000", size: number) {
		this.ctx.beginPath();

		this.ctx.fillStyle = color; // Цвет линии
		this.ctx.arc(e.offsetX, e.offsetY, size, 0, Math.PI * 2);

		this.ctx.fill();
	}

	clear() {
		console.log("clear");
		this.ctx.beginPath();
		this.ctx.fillStyle = "#FFFFFF";
		this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);

		this.ctx.fill();
		this.ctx.closePath();
	}
}

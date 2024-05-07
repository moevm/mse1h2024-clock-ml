import { Point } from "./point";

export class Renderer {
	constructor(private ctx: CanvasRenderingContext2D) {}
	private lastPoint: Point | null = null;

	paint(e: MouseEvent, color: `#${string}` = "#000000", size: number) {
		if (this.lastPoint == null) this.lastPoint = new Point(e.offsetX, e.offsetY);
		this.ctx.beginPath();

		this.ctx.fillStyle = color; // Цвет линии
		this.ctx.arc(e.offsetX, e.offsetY, size, 0, Math.PI * 2);

		//? trace

		const trace = this.lastPoint.traceTo(new Point(e.offsetX, e.offsetY));
		let val = trace.next();

		while (!val.done) {
			this.ctx.arc(val.value.x, val.value.y, size, 0, Math.PI * 2);
			val = trace.next();
		}

		this.lastPoint = new Point(e.offsetX, e.offsetY);
		this.ctx.fill();
	}

	clear() {
		console.log("clear");

		this.ctx.fillStyle = "#FFF";

		this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	}

	stop() {
		this.lastPoint = null;
	}
}

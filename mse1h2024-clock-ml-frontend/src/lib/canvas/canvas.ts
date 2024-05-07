import { Renderer } from "./renderer";

export class CanvasAPI {
	private ctx: CanvasRenderingContext2D;
	private tool: "brush" | "eraser" = "brush";
	private size: number = 2;

	private isActive = false;

	private renderer: Renderer;

	constructor(elem: HTMLCanvasElement) {
		this.ctx = elem.getContext("2d")!;

		this.renderer = new Renderer(this.ctx);

		elem.addEventListener("mousedown", this.onDrawStart.bind(this));
		window.addEventListener("mouseup", this.onDrawEnd.bind(this));
		elem.addEventListener("mousemove", this.onDraw.bind(this));

		this.resize(elem);

		this.renderer.clear();
	}

	setTool(tool: "brush" | "eraser") {
		this.tool = tool;
	}

	setSize(size: number) {
		this.size = size;
	}

	clear() {
		this.renderer.clear();
	}

	private resize(elem: HTMLCanvasElement) {
		const { width, height } = elem.getBoundingClientRect();

		elem.width = width;
		elem.height = height;
		elem.style.width = `${width}px`;
		elem.style.height = `${height}px`;
	}

	private onDrawStart() {
		this.isActive = true;
	}
	private onDrawEnd() {
		this.isActive = false;
		this.renderer.stop();
	}
	private onDraw(e: MouseEvent) {
		if (!this.isActive) return;
		const color = this.tool === "brush" ? "#000000" : "#FFFFFF";

		this.renderer.paint(e, color, this.size);
	}
}

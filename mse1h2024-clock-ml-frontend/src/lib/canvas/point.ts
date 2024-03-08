export class Point {
	constructor(private _x: number, private _y: number) {}

	set coords(coords: [number, number]) {
		this._x = coords[0];
		this._y = coords[1];
	}

	get x() {
		return this._x;
	}

	get y() {
		return this._y;
	}

	*traceTo(to: Point) {
		const dx = to.x - this.x;
		const dy = this.y - to.y;

		const c = to.x * this.y - this.x * to.y;

		let lineFunc = (x: number) => (c - dy * x) / dx;

		if (dx === 0 && dy === 0) {
			return null;
		}

		if (dx === 0) {
			for (let i = 0; i < Math.abs(dy); i += 0.5) {
				yield new Point(c / dy, this.y + Math.sign(this.y) * i);
			}
		}

		for (let i = 0; i < Math.abs(dx); i += 0.5) {
			yield new Point(this.x + Math.sign(dx) * i, lineFunc(this.x + Math.sign(dx) * i));
		}
	}
}

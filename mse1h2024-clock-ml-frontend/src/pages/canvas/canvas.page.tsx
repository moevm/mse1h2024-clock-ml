import { useEffect, useRef, MouseEvent } from "react";
import { Canvas } from "../../components/canvas/canvas.component";
import { Toolbar } from "../../components/canvas/toolbar/toolbar.component";
import { Layout } from "../../components/layout/layout.component";
import { TToolbar } from "../../types";
import { Controls } from "../../components/canvas/contols/controls.component";
import { CanvasAPI } from "../../lib/canvas/canvas";

export const CanvasPage = () => {
	const canvasRef = useRef<HTMLCanvasElement>(null);
	const canvasAPIRef = useRef<CanvasAPI>();

	useEffect(() => {
		if (canvasRef.current && !canvasAPIRef.current) {
			canvasAPIRef.current = new CanvasAPI(canvasRef.current);
		}
	}, [canvasRef.current]);

	function onSelect(value: TToolbar) {
		if (canvasAPIRef.current) {
			canvasAPIRef.current.setTool(value.tool);
			canvasAPIRef.current.setSize(value.size);
		}
	}

	function onClear() {
		canvasAPIRef.current?.clear();
	}

	function onSubmit(e: MouseEvent) {
		canvasRef.current?.toBlob((blob) => {
			const form = new FormData();
			form.append("file", blob!, "img.png");

			form.append("broker", "true");

			fetch("http://localhost:54321/api/v1/get-estimation", {
				method: "POST",
				body: form,
			})
				.then((res) => res.text()) // TODO допилить, когда будет rabbit готов.
				.then(console.log, console.log); // todo  Пока что протестить вывод не получается
		});
	}

	return (
		<Layout linear>
			<Toolbar onSelect={onSelect} />
			<Canvas ref={canvasRef} />
			<Controls onClear={onClear} onSubmit={onSubmit} />
		</Layout>
	);
};

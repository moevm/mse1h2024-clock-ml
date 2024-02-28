import { useEffect, useRef } from "react";
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
	return (
		<Layout linear>
			<Toolbar onSelect={onSelect} />
			<Canvas ref={canvasRef} />
			<Controls onClear={onClear} />
		</Layout>
	);
};

import { useEffect, useRef, MouseEvent } from "react";
import { Canvas } from "../../components/canvas/canvas.component";
import { Toolbar } from "../../components/canvas/toolbar/toolbar.component";
import { Layout } from "../../components/layout/layout.component";
import { IEstimationResponse, TToolbar } from "../../types";
import { Controls } from "../../components/canvas/controls/controls.component";
import { CanvasAPI } from "../../lib/canvas/canvas";
import { useAtomValue, useSetAtom } from "jotai";
import { sendForm } from "../../api";

import { scoreAtom } from "../../atoms/score";
import { brokerAtom } from "../../atoms/broker";
import { useNavigate } from "react-router-dom";
import { imgAtom } from "../../atoms/image";
import { timeAtom } from "../../atoms/time";

export const CanvasPage = () => {
	const canvasRef = useRef<HTMLCanvasElement>(null);
	const canvasAPIRef = useRef<CanvasAPI>();

	const broker = useAtomValue(brokerAtom);
	const setScore = useSetAtom(scoreAtom);
	const setImage = useSetAtom(imgAtom);
	const time = useAtomValue(timeAtom);
	const navigate = useNavigate();

	useEffect(() => {
		if (canvasRef.current && !canvasAPIRef.current) {
			canvasAPIRef.current = new CanvasAPI(canvasRef.current);
		}
	}, [canvasRef.current]);

	function onSelect(value: TToolbar) {
		if (!canvasAPIRef.current) return;

		canvasAPIRef.current.setTool(value.tool);
		canvasAPIRef.current.setSize(value.size);
	}

	function onClear() {
		canvasAPIRef.current?.clear();
	}

	function onSubmit(_e: MouseEvent) {
		setScore(null);
		canvasRef.current?.toBlob((blob) => {
			const form = new FormData();
			form.append("file", blob!, "clock.png");
			form.append("broker", String(broker));
			form.append("hours", time[0]);
			form.append("minutes", time[1]);

			sendForm<IEstimationResponse>("/get-estimation", form).then((res) => {
				setScore(res.result);
			});

			navigate("/result");
			setImage(URL.createObjectURL(blob!));
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

import { forwardRef } from "react";
import css from "./canvas.module.css";

interface TCanvas {}

export const Canvas = forwardRef<HTMLCanvasElement, TCanvas>(({}, ref) => {
	return <canvas ref={ref} className={css.canvas} width="100%" height="100%"></canvas>;
});

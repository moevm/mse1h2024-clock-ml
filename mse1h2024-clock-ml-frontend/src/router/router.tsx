import { createBrowserRouter } from "react-router-dom";
import { Index } from "../pages/index/index.page";
import { CanvasPage } from "../pages/canvas/canvas.page";
import { ResultPage } from "../pages/result/result.page";

export const router = createBrowserRouter([
	{
		path: "/",
		element: <Index />,
	},
	{
		path: "/canvas",
		element: <CanvasPage />,
	},
	{
		path: "/result",
		element: <ResultPage />,
	},
]);
